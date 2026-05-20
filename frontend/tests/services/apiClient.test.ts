import { describe, expect, it, vi } from "vitest";
import { ApiError, requestJson } from "../../src/services/apiClient";

describe("apiClient", () => {
  it("returns parsed JSON for successful responses", async () => {
    const fetcher = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ status: "ok" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await expect(requestJson<{ status: string }>("/health", {}, fetcher)).resolves.toEqual({
      status: "ok",
    });
    expect(fetcher).toHaveBeenCalledWith(
      "http://localhost:8000/health",
      expect.objectContaining({ headers: {} }),
    );
  });

  it("keeps absolute URLs unchanged", async () => {
    const fetcher = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ status: "ok" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await requestJson("https://example.test/health", {}, fetcher);

    expect(fetcher).toHaveBeenCalledWith(
      "https://example.test/health",
      expect.objectContaining({ headers: {} }),
    );
  });

  it("adds local development auth headers from the selected role", async () => {
    const storage = new Map<string, string>();
    vi.stubGlobal("localStorage", {
      getItem: (key: string) => storage.get(key) ?? null,
      setItem: (key: string, value: string) => storage.set(key, value),
      removeItem: (key: string) => storage.delete(key),
    });
    localStorage.setItem("faq-assistant-role", "admin");

    const fetcher = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ status: "ok" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await requestJson("/admin/faq-sources", {}, fetcher);

    expect(fetcher).toHaveBeenCalledWith(
      "http://localhost:8000/admin/faq-sources",
      expect.objectContaining({
        headers: expect.objectContaining({
          "x-user-id": "admin-1",
          "x-user-email": "admin@example.com",
          "x-user-role": "admin",
        }),
      }),
    );
    vi.unstubAllGlobals();
  });

  it("raises ApiError with stable error payload for failed responses", async () => {
    const fetcher = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ code: "forbidden", message: "Admin role required" }), {
        status: 403,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await expect(requestJson("/admin/faq-sources", {}, fetcher)).rejects.toMatchObject({
      status: 403,
      payload: { code: "forbidden", message: "Admin role required" },
    });
  });

  it("converts network failures into ApiError", async () => {
    const fetcher = vi.fn().mockRejectedValue(new Error("network down"));

    await expect(requestJson("/health", {}, fetcher)).rejects.toBeInstanceOf(ApiError);
  });
});
