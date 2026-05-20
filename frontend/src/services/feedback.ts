import { requestJson } from "./apiClient";

export type FeedbackRating = "helpful" | "unhelpful";

export type FeedbackPayload = {
  rating: FeedbackRating;
  comment?: string | null;
};

export type FeedbackResponse = {
  id: string;
  answer_id: string;
  question_id: string;
  use_case_id: string;
  faq_source_id_at_time: string | null;
  rating: FeedbackRating;
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
