import { useState } from "react";
import type { FormEvent } from "react";
import { EmptyState } from "../../components/common/EmptyState";
import { ErrorState } from "../../components/common/ErrorState";
import { LoadingState } from "../../components/common/LoadingState";
import { StatusBadge } from "../../components/common/StatusBadge";
import { activateFaqSource, createFaqSource, deleteFaqSource } from "../../services/faqSources";
import type { FaqSourceSummary } from "../../services/faqSources";

type FaqSourcesListProps = {
  sources: FaqSourceSummary[];
  state?: "ready" | "loading" | "empty" | "error";
  onSourcesChanged?: () => void | Promise<void>;
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

function AddSourceForm({ onSourcesChanged }: { onSourcesChanged?: () => void | Promise<void> }) {
  const [status, setStatus] = useState<"idle" | "saving" | "saved" | "error">("idle");
  const [message, setMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    const name = String(formData.get("name") ?? "").trim();
    const description = String(formData.get("description") ?? "").trim();
    const useCaseId = String(formData.get("use_case_id") ?? "").trim();
    const questionText = String(formData.get("question_text") ?? "").trim();
    const answerText = String(formData.get("answer_text") ?? "").trim();

    if (!name || !useCaseId || !questionText || !answerText) {
      setStatus("error");
      setMessage("Source name, use case, FAQ question, and FAQ answer are required.");
      return;
    }

    setStatus("saving");
    setMessage("Creating FAQ source");

    try {
      await createFaqSource({
        name,
        description: description || undefined,
        use_case_id: useCaseId,
        entries: [
          {
            question_text: questionText,
            answer_text: answerText,
            keywords: [],
          },
        ],
      });
      form.reset();
      await onSourcesChanged?.();
      setStatus("saved");
      setMessage("FAQ source created. Source list refreshed for readiness review.");
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "Could not create FAQ source.");
    }
  }

  return (
    <form
      aria-labelledby="add-source-title"
      className="space-y-4 rounded-md border border-slate-200 bg-white p-4"
      onSubmit={handleSubmit}
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-sm font-medium uppercase text-emerald-700">Add Source</p>
          <h2 id="add-source-title" className="text-lg font-semibold text-slate-950">
            Create FAQ source
          </h2>
        </div>
        <button
          className="rounded-md bg-slate-950 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          disabled={status === "saving"}
          type="submit"
        >
          {status === "saving" ? "Creating source" : "Create FAQ source"}
        </button>
      </div>

      {message ? (
        <p className={status === "error" ? "text-sm text-red-800" : "text-sm text-slate-700"}>
          {message}
        </p>
      ) : null}

      <div className="grid gap-4 md:grid-cols-2">
        <label className="space-y-2">
          <span className="block text-sm font-medium text-slate-900">Source name</span>
          <input
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-950"
            name="name"
            placeholder="Employee handbook FAQ"
            required
            type="text"
          />
        </label>

        <label className="space-y-2">
          <span className="block text-sm font-medium text-slate-900">Use case</span>
          <select
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-950"
            defaultValue="hr"
            name="use_case_id"
            required
          >
            <option value="hr">HR</option>
            <option value="it_support">IT Support</option>
            <option value="product_support">Product Support</option>
            <option value="admissions">Admissions</option>
          </select>
        </label>
      </div>

      <label className="space-y-2">
        <span className="block text-sm font-medium text-slate-900">Description</span>
        <input
          className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-950"
          name="description"
          placeholder="Optional context for admins"
          type="text"
        />
      </label>

      <div className="grid gap-4 md:grid-cols-2">
        <label className="space-y-2">
          <span className="block text-sm font-medium text-slate-900">FAQ question</span>
          <textarea
            className="min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-950"
            name="question_text"
            placeholder="How do I request parental leave?"
            required
          />
        </label>

        <label className="space-y-2">
          <span className="block text-sm font-medium text-slate-900">FAQ answer</span>
          <textarea
            className="min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-950"
            name="answer_text"
            placeholder="Submit the request in the HR portal."
            required
          />
        </label>
      </div>
    </form>
  );
}

function SourceActions({
  source,
  onSourcesChanged,
}: {
  source: FaqSourceSummary;
  onSourcesChanged?: () => void | Promise<void>;
}) {
  const [message, setMessage] = useState<string | null>(null);
  const [isWorking, setIsWorking] = useState(false);

  async function handleActivate() {
    setIsWorking(true);
    setMessage(`Activating ${source.name}`);
    try {
      await activateFaqSource(source.id);
      await onSourcesChanged?.();
      setMessage(`${source.name} activated for ${source.use_case_name ?? source.use_case_id}.`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : `Could not activate ${source.name}.`);
    } finally {
      setIsWorking(false);
    }
  }

  async function handleDelete() {
    const confirmed =
      typeof window === "undefined" ||
      window.confirm(`Delete ${source.name}? This removes the FAQ source from admin management.`);
    if (!confirmed) {
      return;
    }

    setIsWorking(true);
    setMessage(`Deleting ${source.name}`);
    try {
      await deleteFaqSource(source.id);
      await onSourcesChanged?.();
      setMessage(`${source.name} deleted.`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : `Could not delete ${source.name}.`);
    } finally {
      setIsWorking(false);
    }
  }

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap gap-2">
        <button
          className="rounded-md border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-800 hover:bg-slate-100 disabled:text-slate-400"
          disabled={isWorking || source.is_active || source.status === "archived"}
          onClick={handleActivate}
          type="button"
        >
          Activate source
        </button>
        <button
          className="rounded-md border border-red-300 px-3 py-1.5 text-xs font-medium text-red-800 hover:bg-red-50 disabled:text-slate-400"
          disabled={isWorking}
          onClick={handleDelete}
          type="button"
        >
          Delete source
        </button>
      </div>
      {message ? <p className="text-xs text-slate-700">{message}</p> : null}
    </div>
  );
}

export function FaqSourcesList({ sources, state = "ready", onSourcesChanged }: FaqSourcesListProps) {
  if (state === "loading") {
    return <LoadingState label="Loading FAQ sources" />;
  }
  if (state === "error") {
    return <ErrorState title="Could not load FAQ sources" description="Retry with the same filters." />;
  }
  if (state === "empty" || sources.length === 0) {
    return (
      <section className="space-y-4">
        <EmptyState title="No FAQ sources" description="Add a source before users can receive grounded answers." />
        <AddSourceForm onSourcesChanged={onSourcesChanged} />
      </section>
    );
  }

  return (
    <section aria-labelledby="faq-sources-title" className="space-y-4">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase text-emerald-700">FAQ Sources</p>
          <h1 id="faq-sources-title" className="text-2xl font-semibold text-slate-950">
            Manage active knowledge by use case
          </h1>
        </div>
      </div>
      <AddSourceForm onSourcesChanged={onSourcesChanged} />
      <div className="overflow-hidden rounded-md border border-slate-200">
        <table className="w-full border-collapse text-left text-sm">
          <thead className="bg-slate-50 text-slate-700">
            <tr>
              <th className="p-3">Source</th>
              <th className="p-3">Use case</th>
              <th className="p-3">Status</th>
              <th className="p-3">Readiness</th>
              <th className="p-3">Actions</th>
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
                <td className="p-3">
                  <SourceActions source={source} onSourcesChanged={onSourcesChanged} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
