type LoginPageProps = {
  onSelectRole: (role: "admin" | "end_user") => void;
};

export function LoginPage({ onSelectRole }: LoginPageProps) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50">
      <section className="w-full max-w-sm rounded-lg border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="mb-6 text-xl font-semibold text-slate-900">
          FAQ Knowledge Assistant
        </h1>
        <p className="mb-4 text-sm text-slate-600">Sign in as</p>
        <div className="flex flex-col gap-3">
          <button
            type="button"
            className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
            onClick={() => onSelectRole("admin")}
          >
            Admin
          </button>
          <button
            type="button"
            className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            onClick={() => onSelectRole("end_user")}
          >
            End User
          </button>
        </div>
      </section>
    </main>
  );
}
