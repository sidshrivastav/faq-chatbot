type ErrorStateProps = {
  title: string;
  description?: string;
};

export function ErrorState({ title, description }: ErrorStateProps) {
  return (
    <section className="rounded-md border border-red-200 bg-red-50 p-4" role="alert">
      <h2 className="text-base font-semibold text-red-900">{title}</h2>
      {description ? <p className="mt-1 text-sm text-red-800">{description}</p> : null}
    </section>
  );
}
