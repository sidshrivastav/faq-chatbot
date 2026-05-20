import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { ChatPage } from "../src/pages/chat/ChatPage";

describe("ChatPage", () => {
  const useCase = {
    id: "hr",
    name: "HR",
    has_active_source: true,
    active_source_name: "HR handbook",
  };

  it("renders the use case chip and grounded answer state", () => {
    const markup = renderToStaticMarkup(
      <ChatPage
        useCase={useCase}
        messages={[
          { id: "q-1", role: "user", text: "How do I request parental leave?" },
          {
            id: "a-1",
            role: "assistant",
            text: "Submit the request in Workday.",
            answer_state: "answered",
            source_name: "HR handbook",
          },
        ]}
        composerValue="What is the process for parental leave?"
        state="ready"
      />,
    );

    expect(markup).toContain("HR");
    expect(markup).toContain("HR handbook");
    expect(markup).toContain("Submit the request in Workday.");
    expect(markup).toContain("Grounded answer");
    expect(markup).toContain("Ask a question");
  });

  it("renders loading state while waiting for an answer", () => {
    const markup = renderToStaticMarkup(
      <ChatPage
        useCase={useCase}
        messages={[]}
        composerValue="How do I request parental leave?"
        state="loading"
      />,
    );

    expect(markup).toContain("Generating answer");
    expect(markup).toContain("Loading grounded response");
  });

  it("renders unsupported answer state with text", () => {
    const markup = renderToStaticMarkup(
      <ChatPage
        useCase={useCase}
        messages={[
          {
            id: "a-1",
            role: "assistant",
            text: "I couldn't find an answer in the active FAQ source.",
            answer_state: "unsupported",
          },
        ]}
        composerValue=""
        state="ready"
      />,
    );

    expect(markup).toContain("Unsupported answer");
    expect(markup).toContain("I couldn&#x27;t find an answer in the active FAQ source.");
  });

  it("renders no active source state with text", () => {
    const markup = renderToStaticMarkup(
      <ChatPage
        useCase={{ ...useCase, has_active_source: false, active_source_name: null }}
        messages={[
          {
            id: "a-1",
            role: "assistant",
            text: "No active FAQ source is available for this use case.",
            answer_state: "no_active_source",
          },
        ]}
        composerValue=""
        state="ready"
      />,
    );

    expect(markup).toContain("No active FAQ source");
    expect(markup).toContain("No active FAQ source is available for this use case.");
  });
});
