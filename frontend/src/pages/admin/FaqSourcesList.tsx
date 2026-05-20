import { EmptyState } from "../../components/common/EmptyState";
import { ErrorState } from "../../components/common/ErrorState";
import { LoadingState } from "../../components/common/LoadingState";
import { StatusBadge } from "../../components/common/StatusBadge";
import type { FaqSourceSummary } from "../../services/faqSources";

type FaqSourcesListProps = {
  sources: FaqSourceSummary[];
  state?: "ready" | "loading" | "empty" | "error";
};

function statusLabel(source: FaqSourceSummary) {
  if (source.is_active) {
    return "Active source";
  }
  if (source.status === "invalid") {
    return "Invalid source";
  }
  if (source.status === "archived") {
    return "Archived source";
  }
  return "Inactive source";
}

function statusTone(source: FaqSourceSummary) {
  if (source.is_active) {
    return "success" as const;
  }
  if (source.status === "invalid") {
    return "danger" as const;
  }
  if (source.readiness_state === "warning") {
    return "warning" as const;
  }
  return "neutral" as const;
}

export function FaqSourcesList({ sources, state = "ready" }: FaqSourcesListProps) {
  if (state === "loading") {
    return <LoadingState label="Loading FAQ sources" />;
  }
  if (state === "error") {
    return <ErrorState title="Could not load FAQ sources" description="Retry with the same filters." />;
  }
  if (state === "empty" || sources.length === 0) {
    return <EmptyState title="No FAQ sources" description="Add a source before users can receive grounded answers." />;
  }

  return (
    <section aria-labelledby="faq-sources-title" className="space-y-4">
      <div>
        <p className="text-sm font-medium uppercase text-emerald-700">FAQ Sources</p>
        <h1 id="faq-sources-title" className="text-2xl font-semibold text-slate-950">
          Manage active knowledge by use case
        </h1>
      </div>
      <div className="overflow-hidden rounded-md border border-slate-200">
        <table className="w-full border-collapse text-left text-sm">
          <thead className="bg-slate-50 text-slate-700">
            <tr>
              <th className="p-3">Source</th>
              <th className="p-3">Use case</th>
              <th className="p-3">Status</th>
              <th className="p-3">Readiness</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((source) => (
              <tr className="border-t border-slate-200" key={source.id}>
                <td className="p-3 font-medium text-slate-950">{source.name}</td>
                <td className="p-3 text-slate-700">{source.use_case_name ?? source.use_case_id}</td>
                <td className="p-3">
                  <StatusBadge tone={statusTone(source)}>{statusLabel(source)}</StatusBadge>
                </td>
                <td className="p-3 text-slate-700">{source.readiness_message ?? source.readiness_state}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
