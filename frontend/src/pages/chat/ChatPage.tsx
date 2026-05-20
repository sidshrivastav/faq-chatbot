import { AnswerFeedback } from "../../components/feedback/AnswerFeedback";
import { LoadingState } from "../../components/common/LoadingState";
import { StatusBadge } from "../../components/common/StatusBadge";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  text: string;
  answer_state?: "answered" | "unsupported" | "no_active_source" | "error";
  source_name?: string | null;
  feedback_allowed?: boolean;
};

export type { ChatMessage };

type ChatPageProps = {
  useCase: {
    id: string;
    name: string;
    has_active_source: boolean;
    active_source_name?: string | null;
  };
  messages: ChatMessage[];
  composerValue: string;
  state?: "ready" | "loading";
  onComposerChange?: (value: string) => void;
  onSubmitQuestion?: () => void;
};

function answerTone(answerState?: ChatMessage["answer_state"]) {
  if (answerState === "answered") {
    return "success" as const;
  }
  if (answerState === "unsupported") {
    return "warning" as const;
  }
  if (answerState === "no_active_source") {
    return "danger" as const;
  }
  return "neutral" as const;
}

function answerLabel(answerState?: ChatMessage["answer_state"]) {
  if (answerState === "answered") {
    return "Grounded answer";
  }
  if (answerState === "unsupported") {
    return "Unsupported answer";
  }
  if (answerState === "no_active_source") {
    return "No active FAQ source";
  }
  if (answerState === "error") {
    return "Answer error";
  }
  return "Chat message";
}

export function ChatPage({
  useCase,
  messages,
  composerValue,
  state = "ready",
  onComposerChange,
  onSubmitQuestion,
}: ChatPageProps) {
  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmitQuestion?.();
  }

  return (
    <section aria-labelledby="chat-title" className="space-y-6">
      <header className="space-y-2">
        <p className="text-sm font-medium uppercase text-emerald-700">Chat</p>
        <h1 id="chat-title" className="text-2xl font-semibold text-slate-950">
          Ask a grounded question
        </h1>
        <div className="flex flex-wrap gap-2">
          <StatusBadge tone="neutral">{useCase.name}</StatusBadge>
          <StatusBadge tone={useCase.has_active_source ? "success" : "danger"}>
            {useCase.has_active_source
              ? `Active source: ${useCase.active_source_name ?? "Available"}`
              : "No active FAQ source"}
          </StatusBadge>
        </div>
      </header>

      {state === "loading" ? (
        <div className="space-y-2">
          <p className="text-sm font-medium text-slate-950">Generating answer</p>
          <LoadingState label="Loading grounded response" />
        </div>
      ) : null}

      <div className="space-y-3">
        {messages.length === 0 ? (
          <p className="text-sm text-slate-700">Ask a question to start the conversation.</p>
        ) : null}
        {messages.map((message) => (
          <article className="rounded-md border border-slate-200 bg-white p-4" key={message.id}>
            <div className="flex flex-wrap items-center gap-2">
              <StatusBadge tone={message.role === "assistant" ? answerTone(message.answer_state) : "neutral"}>
                {message.role === "assistant" ? answerLabel(message.answer_state) : "User question"}
              </StatusBadge>
              {message.source_name ? <span className="text-xs text-slate-600">{message.source_name}</span> : null}
            </div>
            <p className="mt-3 text-slate-900">{message.text}</p>
            {message.role === "assistant" && message.feedback_allowed ? (
              <AnswerFeedback answerId={message.id} state="idle" />
            ) : null}
          </article>
        ))}
      </div>

      <form className="space-y-3" onSubmit={handleSubmit}>
        <label className="block space-y-2">
          <span className="text-sm font-medium text-slate-900">Ask a question</span>
          <textarea
            aria-label="Question composer"
            className="min-h-28 w-full rounded-md border border-slate-300 bg-white p-3 text-sm text-slate-950"
            placeholder="Ask a question"
            onChange={(event) => onComposerChange?.(event.target.value)}
            value={composerValue}
          />
        </label>
        <button
          className="rounded-md bg-slate-950 px-4 py-2 text-sm font-medium text-white"
          disabled={state === "loading" || composerValue.trim().length === 0}
          type="submit"
        >
          Ask a question
        </button>
      </form>
    </section>
  );
}
