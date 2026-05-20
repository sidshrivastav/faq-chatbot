type FeedbackRating = "helpful" | "unhelpful";

type AnswerFeedbackProps = {
  answerId: string;
  state: "idle" | "saving" | "saved" | "error";
  rating?: FeedbackRating;
  comment?: string;
};

export function AnswerFeedback({ state, rating, comment }: AnswerFeedbackProps) {
  if (state === "saved") {
    return (
      <aside
        className="mt-3 flex items-center gap-2 text-sm text-slate-600"
        aria-live="polite"
      >
        <span>
          Feedback recorded — thank you for marking this as{" "}
          <strong>{rating}</strong>.
        </span>
      </aside>
    );
  }

  if (state === "error") {
    return (
      <aside className="mt-3 space-y-2" aria-live="polite">
        <p className="text-sm font-medium text-red-700">
          Feedback submission failed — please try again.
        </p>
        {comment ? (
          <p className="text-sm text-slate-600">Your comment: {comment}</p>
        ) : null}
        <div className="flex gap-2">
          <button
            type="button"
            aria-label="Mark as helpful"
            className="rounded border border-slate-300 px-3 py-1 text-sm hover:bg-slate-100"
          >
            Helpful
          </button>
          <button
            type="button"
            aria-label="Mark as unhelpful"
            className="rounded border border-slate-300 px-3 py-1 text-sm hover:bg-slate-100"
          >
            Unhelpful
          </button>
        </div>
        <textarea
          className="w-full rounded border border-slate-300 p-2 text-sm"
          placeholder="Optional comment"
          aria-label="Optional comment"
          defaultValue={comment ?? ""}
        />
      </aside>
    );
  }

  return (
    <aside className="mt-3 space-y-2">
      <p className="text-xs font-medium text-slate-700">Was this answer helpful?</p>
      <div className="flex gap-2">
        <button
          type="button"
          aria-label="Mark as helpful"
          className="rounded border border-slate-300 px-3 py-1 text-sm hover:bg-slate-100 disabled:opacity-50"
          disabled={state === "saving"}
        >
          Helpful
        </button>
        <button
          type="button"
          aria-label="Mark as unhelpful"
          className="rounded border border-slate-300 px-3 py-1 text-sm hover:bg-slate-100 disabled:opacity-50"
          disabled={state === "saving"}
        >
          Unhelpful
        </button>
      </div>
      <textarea
        className="w-full rounded border border-slate-300 p-2 text-sm"
        placeholder="Optional comment"
        aria-label="Optional comment"
      />
    </aside>
  );
}
