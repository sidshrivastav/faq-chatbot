import { requestJson } from "./apiClient";

export type FeedbackRating = "helpful" | "unhelpful";

export type FeedbackReason =
  | "incorrect_answer"
  | "not_specific_enough"
  | "missing_from_faq"
  | "confusing_response"
  | "outdated_source";

export const FEEDBACK_REASON_LABELS: Record<FeedbackReason, string> = {
  incorrect_answer: "Incorrect answer",
  not_specific_enough: "Not specific enough",
  missing_from_faq: "Missing from FAQ",
  confusing_response: "Confusing response",
  outdated_source: "Outdated source",
};

export type FeedbackPayload = {
  rating: FeedbackRating;
  reason?: FeedbackReason | null;
  comment?: string | null;
};

export type FeedbackResponse = {
  id: string;
  answer_id: string;
  question_id: string;
  use_case_id: string;
  faq_source_id_at_time: string | null;
  rating: FeedbackRating;
  reason: FeedbackReason | null;
  comment: string | null;
  created_at: string;
};

export function submitFeedback(answerId: string, payload: FeedbackPayload) {
  return requestJson<FeedbackResponse>(`/answers/${answerId}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}
