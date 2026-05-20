import { requestJson } from "./apiClient";
import type { UseCaseSummary } from "./chat";

export function listUseCases() {
  return requestJson<{ items: UseCaseSummary[] }>("/use-cases", {
    method: "GET",
  });
}

