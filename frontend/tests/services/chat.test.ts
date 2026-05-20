import { describe, expect, it, vi } from "vitest";
import * as chatService from "../../src/services/chat";
import * as useCasesService from "../../src/services/useCases";

describe("chat service", () => {
  it("posts chat questions to the contract path", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ "Content-Type": "application/json" }),
      json: async () => ({ answer_state: "answered" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await chatService.submitChatQuestion({
      use_case_id: "hr",
      question_text: "How do I request parental leave?",
    });

    expect(fetchMock).toHaveBeenCalledWith(
      "/chat/questions",
      expect.objectContaining({
        method: "POST",
      }),
    );
    vi.unstubAllGlobals();
  });

  it("lists use cases through the contract path", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ "Content-Type": "application/json" }),
      json: async () => ({ items: [] }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await useCasesService.listUseCases();

    expect(fetchMock).toHaveBeenCalledWith(
      "/use-cases",
      expect.objectContaining({
        method: "GET",
      }),
    );
    vi.unstubAllGlobals();
  });
});
