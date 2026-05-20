type LoadingStateProps = {
  label: string;
};

export function LoadingState({ label }: LoadingStateProps) {
  return (
    <div aria-label={label} className="rounded-md border border-slate-200 bg-white p-4" role="status">
      <span className="text-sm text-slate-700">{label}</span>
    </div>
  );
}
