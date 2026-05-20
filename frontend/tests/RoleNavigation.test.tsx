/**
 * T061 – Role-aware navigation tests.
 *
 * Covers:
 * - Admin shell renders admin nav links (FAQ Sources, Analytics, Unanswered Questions)
 * - End-user shell renders chat-focused navigation only
 * - End-user shell does not render admin-only links
 * - Unauthorized page text is accessible (not color-only)
 */
import { describe, expect, it } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { App } from "../src/App";
import { UnauthorizedState } from "../src/components/common/UnauthorizedState";

describe("Role-aware navigation: admin", () => {
  it("renders admin nav links when role is admin", () => {
    const markup = renderToStaticMarkup(<App role="admin" />);
    expect(markup).toContain("FAQ Sources");
    expect(markup).toContain("Analytics");
  });

  it("admin shell does not hide FAQ Sources link", () => {
    const markup = renderToStaticMarkup(<App role="admin" />);
    expect(markup).toContain("FAQ Sources");
  });

  it("uses client-side navigation controls instead of full-page anchor reloads", () => {
    const markup = renderToStaticMarkup(<App role="admin" />);
    expect(markup).toContain("FAQ Sources");
    expect(markup).not.toContain('href="/admin/faq-sources"');
    expect(markup).not.toContain('href="/admin/analytics"');
    expect(markup).not.toContain('href="/admin/unanswered"');
  });
});

describe("Role-aware navigation: end user", () => {
  it("renders chat nav for end user", () => {
    const markup = renderToStaticMarkup(<App role="end_user" />);
    expect(markup).toContain("Ask a Question");
  });

  it("end user shell does not show admin-only links", () => {
    const markup = renderToStaticMarkup(<App role="end_user" />);
    expect(markup).not.toContain("FAQ Sources");
    expect(markup).not.toContain("Analytics");
  });

  it("uses client-side navigation for chat instead of a full-page anchor reload", () => {
    const markup = renderToStaticMarkup(<App role="end_user" />);
    expect(markup).toContain("Ask a Question");
    expect(markup).not.toContain('href="/chat"');
  });
});

describe("Role-aware navigation: login", () => {
  it("renders role selector when no role is set", () => {
    const markup = renderToStaticMarkup(<App role={null} />);
    expect(markup).toContain("Sign in as");
  });
});

describe("UnauthorizedState", () => {
  it("conveys unauthorized meaning with text not color alone", () => {
    const markup = renderToStaticMarkup(<UnauthorizedState />);
    expect(markup).toContain("not authorized");
  });

  it("renders an accessible description of role limitation", () => {
    const markup = renderToStaticMarkup(<UnauthorizedState />);
    expect(markup).toMatch(/admin|role|permission/i);
  });
});
