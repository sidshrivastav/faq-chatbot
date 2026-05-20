import { useState } from "react";
import { LoginPage } from "./pages/LoginPage";
import { UnauthorizedState } from "./components/common/UnauthorizedState";

type Role = "admin" | "end_user" | null;

type AppProps = {
  role?: Role;
};

function AdminNav() {
  return (
    <nav aria-label="Admin navigation">
      <ul className="flex gap-4 text-sm font-medium">
        <li>
          <a href="/admin/faq-sources" className="text-slate-700 hover:text-slate-900">
            FAQ Sources
          </a>
        </li>
        <li>
          <a href="/admin/analytics" className="text-slate-700 hover:text-slate-900">
            Analytics
          </a>
        </li>
        <li>
          <a href="/admin/unanswered" className="text-slate-700 hover:text-slate-900">
            Unanswered Questions
          </a>
        </li>
      </ul>
    </nav>
  );
}

function EndUserNav() {
  return (
    <nav aria-label="User navigation">
      <ul className="flex gap-4 text-sm font-medium">
        <li>
          <a href="/chat" className="text-slate-700 hover:text-slate-900">
            Ask a Question
          </a>
        </li>
      </ul>
    </nav>
  );
}

function AppShell({ role, onSignOut }: { role: "admin" | "end_user"; onSignOut: () => void }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white px-6 py-4">
        <div className="flex items-center justify-between">
          <span className="text-lg font-semibold text-slate-900">
            FAQ Knowledge Assistant
          </span>
          <div className="flex items-center gap-6">
            {role === "admin" ? <AdminNav /> : <EndUserNav />}
            <span className="text-xs text-slate-500">
              {role === "admin" ? "Admin" : "End User"}
            </span>
            <button
              type="button"
              onClick={onSignOut}
              className="text-xs text-slate-500 hover:text-slate-700"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>
      <main className="p-6">
        {role === "admin" ? (
          <p className="text-slate-700">Select an area from the navigation above.</p>
        ) : (
          <p className="text-slate-700">
            Use the navigation above to ask a question.
          </p>
        )}
      </main>
    </div>
  );
}

export function App({ role: initialRole }: AppProps = {}) {
  const [role, setRole] = useState<Role>(initialRole ?? null);

  if (role === null) {
    return <LoginPage onSelectRole={setRole} />;
  }

  return (
    <AppShell
      role={role}
      onSignOut={() => setRole(null)}
    />
  );
}

export default function Root() {
  return <App />;
}
