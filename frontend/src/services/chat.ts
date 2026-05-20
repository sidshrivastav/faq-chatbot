import { requestJson } from "./apiClient";
import type { FaqEntryInput } from "./faqSources";

export type UseCaseSummary = {
  id: string;
  name: string;
  description?: string | null;
  has_active_source: boolean;
  active_source_name?: string | null;
};

export type ChatQuestionPayload = {
  conversation_id?: string | null;
  use_case_id: string;
  question_text: string;
};

export type ChatAnswerResponse = {
  question_id: string;
  answer_id: string;
  answer_state: "answered" | "unsupported" | "no_active_source" | "error";
  message: string;
  use_case_id: string;
  source_id?: string | null;
  source_name?: string | null;
  retrieved_entries: FaqEntryInput[];
  feedback_allowed: boolean;
};

export function submitChatQuestion(payload: ChatQuestionPayload) {
  return requestJson<ChatAnswerResponse>("/chat/questions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

