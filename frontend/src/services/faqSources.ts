import { requestJson } from "./apiClient";

export type FaqEntryInput = {
  question_text: string;
  answer_text: string;
  keywords?: string[];
};

export type FaqSourceSummary = {
  id: string;
  name: string;
  description?: string | null;
  use_case_id: string;
  use_case_name?: string | null;
  status: string;
  is_active: boolean;
  readiness_state: string;
  readiness_message?: string | null;
  updated_at?: string;
};

export type FaqSourceDetailData = FaqSourceSummary & {
  entries: FaqEntryInput[];
  warnings: string[];
};

export type FaqSourceCreatePayload = {
  name: string;
  description?: string;
  use_case_id: string;
  entries: FaqEntryInput[];
};

export type FaqSourceUpdatePayload = Partial<FaqSourceCreatePayload>;

export function faqSourceRequest<T>(path: string, options: RequestInit = {}) {
  return requestJson<T>(path, options);
}

export function listFaqSources() {
  return faqSourceRequest<{ items: FaqSourceSummary[] }>("/admin/faq-sources", { method: "GET" });
}

export function getFaqSource(sourceId: string) {
  return faqSourceRequest<FaqSourceDetailData>(`/admin/faq-sources/${sourceId}`, { method: "GET" });
}

export function createFaqSource(payload: FaqSourceCreatePayload) {
  return faqSourceRequest<FaqSourceSummary>("/admin/faq-sources", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function updateFaqSource(sourceId: string, payload: FaqSourceUpdatePayload) {
  return faqSourceRequest<FaqSourceDetailData>(`/admin/faq-sources/${sourceId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function activateFaqSource(sourceId: string) {
  return faqSourceRequest<FaqSourceSummary>(`/admin/faq-sources/${sourceId}/activate`, {
    method: "POST",
  });
}

export function deactivateFaqSource(sourceId: string) {
  return faqSourceRequest<FaqSourceSummary>(`/admin/faq-sources/${sourceId}/deactivate`, {
    method: "POST",
  });
}

export function archiveFaqSource(sourceId: string) {
  return faqSourceRequest<FaqSourceSummary>(`/admin/faq-sources/${sourceId}/archive`, {
    method: "POST",
  });
}

export function deleteFaqSource(sourceId: string) {
  return faqSourceRequest<void>(`/admin/faq-sources/${sourceId}`, { method: "DELETE" });
}
