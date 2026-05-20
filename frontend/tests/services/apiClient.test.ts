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
    expect(fetcher).toHaveBeenCalledWith("/health", expect.objectContaining({ headers: {} }));
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
