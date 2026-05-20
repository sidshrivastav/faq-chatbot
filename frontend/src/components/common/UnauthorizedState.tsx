export function UnauthorizedState() {
  return (
    <section
      className="rounded-md border border-amber-200 bg-amber-50 p-6"
      role="alert"
      aria-label="Unauthorized"
    >
      <h2 className="text-base font-semibold text-amber-900">
        You are not authorized to view this page
      </h2>
      <p className="mt-2 text-sm text-amber-800">
        This area requires admin role. Contact your administrator if you believe
        this is an error.
      </p>
    </section>
  );
}
