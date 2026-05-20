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
    response = await fetcher(path, {
      ...options,
      headers: options.headers ?? {},
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
