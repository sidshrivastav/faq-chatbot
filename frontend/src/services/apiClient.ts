export type ErrorPayload = {
  code: string;
  message: string;
  details?: Record<string, unknown> | null;
};

export class ApiError extends Error {
  status: number;
  payload: ErrorPayload;

  constructor(status: number, payload: ErrorPayload) {
    super(payload.message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

type Fetcher = typeof fetch;

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
const LOCAL_AUTH_KEY = "faq-assistant-role";

type LocalRole = "admin" | "end_user";

function buildRequestUrl(path: string) {
  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }

  const normalizedBaseUrl = API_BASE_URL.replace(/\/$/, "");
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${normalizedBaseUrl}${normalizedPath}`;
}

function getLocalRole(): LocalRole | null {
  if (typeof localStorage === "undefined") {
    return null;
  }

  const role = localStorage.getItem(LOCAL_AUTH_KEY);
  if (role === "admin" || role === "end_user") {
    return role;
  }
  return null;
}

function buildHeaders(headers: HeadersInit = {}) {
  const mergedHeaders = new Headers(headers);
  const role = getLocalRole();

  if (role && !mergedHeaders.has("x-user-role")) {
    mergedHeaders.set("x-user-role", role);
    mergedHeaders.set("x-user-id", role === "admin" ? "admin-1" : "user-1");
    mergedHeaders.set("x-user-email", role === "admin" ? "admin@example.com" : "user@example.com");
    mergedHeaders.set("x-user-name", role === "admin" ? "Admin User" : "End User");
  }

  return Object.fromEntries(mergedHeaders.entries());
}

async function parseJson(response: Response): Promise<unknown> {
  const contentType = response.headers.get("Content-Type") ?? "";
  if (!contentType.includes("application/json")) {
    return null;
  }
  return response.json();
}

export async function requestJson<T>(
  path: string,
  options: RequestInit = {},
  fetcher: Fetcher = fetch,
): Promise<T> {
  let response: Response;
  try {
    response = await fetcher(buildRequestUrl(path), {
      ...options,
      headers: buildHeaders(options.headers),
    });
  } catch (error) {
    throw new ApiError(0, {
      code: "network_error",
      message: error instanceof Error ? error.message : "Network request failed",
      details: null,
    });
  }

  const payload = await parseJson(response);
  if (!response.ok) {
    const errorPayload = (payload ?? {
      code: "http_error",
      message: "Request failed",
      details: null,
    }) as ErrorPayload;
    throw new ApiError(response.status, errorPayload);
  }

  return payload as T;
}
