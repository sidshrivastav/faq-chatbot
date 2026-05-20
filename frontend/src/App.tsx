import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { LoginPage } from "./pages/LoginPage";
import { EmptyState } from "./components/common/EmptyState";
import { UnauthorizedState } from "./components/common/UnauthorizedState";
import { FaqSourcesList } from "./pages/admin/FaqSourcesList";
import { ChatPage } from "./pages/chat/ChatPage";
import type { ChatMessage } from "./pages/chat/ChatPage";
import { listFaqSources } from "./services/faqSources";
import type { FaqSourceSummary } from "./services/faqSources";
import { listUseCases } from "./services/useCases";
import { submitChatQuestion } from "./services/chat";
import type { UseCaseSummary } from "./services/chat";

type Role = "admin" | "end_user" | null;
type AppRoute = "/admin/faq-sources" | "/admin/analytics" | "/admin/unanswered" | "/chat";
const LOCAL_AUTH_KEY = "faq-assistant-role";

type AppProps = {
  role?: Role;
  initialRoute?: AppRoute;
};

function NavButton({
  active,
  children,
  onClick,
}: {
  active: boolean;
  children: ReactNode;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      aria-current={active ? "page" : undefined}
      className={active ? "text-slate-950" : "text-slate-700 hover:text-slate-900"}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

function AdminNav({
  currentRoute,
  onNavigate,
}: {
  currentRoute: AppRoute;
  onNavigate: (route: AppRoute) => void;
}) {
  return (
    <nav aria-label="Admin navigation">
      <ul className="flex gap-4 text-sm font-medium">
        <li>
          <NavButton
            active={currentRoute === "/admin/faq-sources"}
            onClick={() => onNavigate("/admin/faq-sources")}
          >
            FAQ Sources
          </NavButton>
        </li>
        <li>
          <NavButton
            active={currentRoute === "/admin/analytics"}
            onClick={() => onNavigate("/admin/analytics")}
          >
            Analytics
          </NavButton>
        </li>
        <li>
          <NavButton
            active={currentRoute === "/admin/unanswered"}
            onClick={() => onNavigate("/admin/unanswered")}
          >
            Unanswered Questions
          </NavButton>
        </li>
      </ul>
    </nav>
  );
}

function EndUserNav({
  currentRoute,
  onNavigate,
}: {
  currentRoute: AppRoute;
  onNavigate: (route: AppRoute) => void;
}) {
  return (
    <nav aria-label="User navigation">
      <ul className="flex gap-4 text-sm font-medium">
        <li>
          <NavButton
            active={currentRoute === "/chat"}
            onClick={() => onNavigate("/chat")}
          >
            Ask a Question
          </NavButton>
        </li>
      </ul>
    </nav>
  );
}

function defaultRouteForRole(role: "admin" | "end_user"): AppRoute {
  return role === "admin" ? "/admin/faq-sources" : "/chat";
}

function routeAllowedForRole(role: "admin" | "end_user", route: AppRoute) {
  if (role === "admin") {
    return route.startsWith("/admin/");
  }
  return route === "/chat";
}

function getStoredRole(): Role {
  if (typeof localStorage === "undefined") {
    return null;
  }

  const storedRole = localStorage.getItem(LOCAL_AUTH_KEY);
  if (storedRole === "admin" || storedRole === "end_user") {
    return storedRole;
  }
  return null;
}

function storeRole(role: "admin" | "end_user") {
  if (typeof localStorage !== "undefined") {
    localStorage.setItem(LOCAL_AUTH_KEY, role);
  }
}

function clearStoredRole() {
  if (typeof localStorage !== "undefined") {
    localStorage.removeItem(LOCAL_AUTH_KEY);
  }
}

function FaqSourcesRoute() {
  const [sources, setSources] = useState<FaqSourceSummary[]>([]);
  const [state, setState] = useState<"ready" | "loading" | "empty" | "error">("loading");

  async function refreshSources() {
    setState("loading");
    try {
      const response = await listFaqSources();
      setSources(response.items);
      setState(response.items.length > 0 ? "ready" : "empty");
    } catch {
      setState("error");
    }
  }

  useEffect(() => {
    void refreshSources();
  }, []);

  return (
    <FaqSourcesList
      sources={sources}
      state={state}
      onSourcesChanged={refreshSources}
    />
  );
}

const DEFAULT_CHAT_USE_CASE: UseCaseSummary = {
  id: "hr",
  name: "HR",
  has_active_source: false,
  active_source_name: null,
};

function ChatRoute() {
  const [useCase, setUseCase] = useState<UseCaseSummary>(DEFAULT_CHAT_USE_CASE);
  const [state, setState] = useState<"ready" | "loading">("loading");
  const [composerValue, setComposerValue] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  useEffect(() => {
    async function loadUseCases() {
      setState("loading");
      try {
        const response = await listUseCases();
        setUseCase(response.items.find((item) => item.id === "hr") ?? DEFAULT_CHAT_USE_CASE);
      } catch {
        setUseCase(DEFAULT_CHAT_USE_CASE);
      } finally {
        setState("ready");
      }
    }

    void loadUseCases();
  }, []);

  async function submitQuestion() {
    const questionText = composerValue.trim();
    if (!questionText) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `local-question-${Date.now()}`,
      role: "user",
      text: questionText,
    };
    setMessages((currentMessages) => [...currentMessages, userMessage]);
    setComposerValue("");
    setState("loading");

    try {
      const response = await submitChatQuestion({
        use_case_id: useCase.id,
        question_text: questionText,
      });
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: response.answer_id,
          role: "assistant",
          text: response.message,
          answer_state: response.answer_state,
          source_name: response.source_name,
          feedback_allowed: response.feedback_allowed,
        },
      ]);
    } catch (error) {
      setMessages((currentMessages) => [
        ...currentMessages,
        {
          id: `local-error-${Date.now()}`,
          role: "assistant",
          text: error instanceof Error ? error.message : "Could not submit the question.",
          answer_state: "error",
          feedback_allowed: false,
        },
      ]);
    } finally {
      setState("ready");
    }
  }

  return (
    <ChatPage
      useCase={useCase}
      messages={messages}
      composerValue={composerValue}
      onComposerChange={setComposerValue}
      onSubmitQuestion={submitQuestion}
      state={state}
    />
  );
}

function AppContent({ role, currentRoute }: { role: "admin" | "end_user"; currentRoute: AppRoute }) {
  if (!routeAllowedForRole(role, currentRoute)) {
    return <UnauthorizedState />;
  }

  if (currentRoute === "/chat") {
    return <ChatRoute />;
  }

  if (currentRoute === "/admin/faq-sources") {
    return <FaqSourcesRoute />;
  }

  if (currentRoute === "/admin/analytics") {
    return (
      <EmptyState
        title="No analytics yet"
        description="Analytics will appear after users ask questions and submit feedback."
      />
    );
  }

  return (
    <EmptyState
      title="No unanswered questions"
      description="Unsupported questions will appear here after users ask questions."
    />
  );
}

function AppShell({
  role,
  currentRoute,
  onNavigate,
  onSignOut,
}: {
  role: "admin" | "end_user";
  currentRoute: AppRoute;
  onNavigate: (route: AppRoute) => void;
  onSignOut: () => void;
}) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white px-6 py-4">
        <div className="flex items-center justify-between">
          <span className="text-lg font-semibold text-slate-900">
            FAQ Knowledge Assistant
          </span>
          <div className="flex items-center gap-6">
            {role === "admin" ? (
              <AdminNav currentRoute={currentRoute} onNavigate={onNavigate} />
            ) : (
              <EndUserNav currentRoute={currentRoute} onNavigate={onNavigate} />
            )}
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
        <AppContent role={role} currentRoute={currentRoute} />
      </main>
    </div>
  );
}

export function App({ role: initialRole, initialRoute }: AppProps = {}) {
  const startingRole = initialRole ?? getStoredRole();
  const [role, setRole] = useState<Role>(startingRole);
  const [currentRoute, setCurrentRoute] = useState<AppRoute>(
    initialRoute ?? defaultRouteForRole(startingRole ?? "end_user"),
  );

  function selectRole(nextRole: "admin" | "end_user") {
    storeRole(nextRole);
    setRole(nextRole);
    setCurrentRoute(defaultRouteForRole(nextRole));
  }

  function signOut() {
    clearStoredRole();
    setRole(null);
  }

  if (role === null) {
    return <LoginPage onSelectRole={selectRole} />;
  }

  return (
    <AppShell
      role={role}
      currentRoute={routeAllowedForRole(role, currentRoute) ? currentRoute : defaultRouteForRole(role)}
      onNavigate={setCurrentRoute}
      onSignOut={signOut}
    />
  );
}

export default function Root() {
  return <App />;
}
