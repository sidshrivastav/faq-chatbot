import { describe, expect, it } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { EmptyState } from "../../src/components/common/EmptyState";
import { ErrorState } from "../../src/components/common/ErrorState";
import { LoadingState } from "../../src/components/common/LoadingState";
import { StatusBadge } from "../../src/components/common/StatusBadge";

describe("common UI states", () => {
  it("renders text labels for status badges", () => {
    const markup = renderToStaticMarkup(<StatusBadge tone="success">Active source</StatusBadge>);

    expect(markup).toContain("Active source");
  });

  it("renders empty, error, and loading states with accessible text", () => {
    const markup = renderToStaticMarkup(
      <>
        <EmptyState title="No FAQ sources" description="Add a source to answer questions." />
        <ErrorState title="Could not load analytics" description="Retry with the same filters." />
        <LoadingState label="Loading analytics" />
      </>,
    );

    expect(markup).toContain("No FAQ sources");
    expect(markup).toContain("Could not load analytics");
    expect(markup).toContain('role="status"');
    expect(markup).toContain('aria-label="Loading analytics"');
  });
});
