import { StatusBadge } from "../../components/common/StatusBadge";
import type { FaqSourceDetailData } from "../../services/faqSources";

type FaqSourceDetailProps = {
  source: FaqSourceDetailData;
};

export function FaqSourceDetail({ source }: FaqSourceDetailProps) {
  return (
    <section aria-labelledby="faq-source-detail-title" className="space-y-5">
      <div>
        <p className="text-sm font-medium uppercase text-emerald-700">FAQ Source Detail</p>
        <h1 id="faq-source-detail-title" className="text-2xl font-semibold text-slate-950">
          {source.name}
        </h1>
        <div className="mt-2 flex gap-2">
          <StatusBadge tone={source.is_active ? "success" : "neutral"}>
            {source.is_active ? "Active source" : "Inactive source"}
          </StatusBadge>
          <StatusBadge tone={source.readiness_state === "invalid" ? "danger" : "success"}>
            {source.readiness_message ?? source.readiness_state}
          </StatusBadge>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        <button type="button">Activate</button>
        <button type="button">Deactivate</button>
        <button type="button">Archive</button>
        <button type="button">Delete</button>
      </div>

      {source.warnings.length > 0 ? (
        <ul className="rounded-md border border-amber-200 bg-amber-50 p-3 text-amber-900">
          {source.warnings.map((warning) => (
            <li key={warning}>{warning}</li>
          ))}
        </ul>
      ) : null}

      <div className="space-y-3">
        {source.entries.map((entry) => (
          <article className="rounded-md border border-slate-200 p-3" key={entry.question_text}>
            <h2 className="font-medium text-slate-950">{entry.question_text}</h2>
            <p className="mt-1 text-slate-700">{entry.answer_text}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
