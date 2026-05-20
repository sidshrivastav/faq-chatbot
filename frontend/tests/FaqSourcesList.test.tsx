import { describe, expect, it, vi } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { FaqSourcesList } from "../src/pages/admin/FaqSourcesList";
import { FaqSourceDetail } from "../src/pages/admin/FaqSourceDetail";
import * as faqSourcesService from "../src/services/faqSources";

const sources = [
  {
    id: "src-1",
    name: "Employee handbook FAQ",
    use_case_id: "hr",
    use_case_name: "HR",
    status: "active",
    is_active: true,
    readiness_state: "ready",
    readiness_message: "Source is ready for Q&A",
    updated_at: "2026-05-20T00:00:00Z",
  },
  {
    id: "src-2",
    name: "Facilities FAQ",
    use_case_id: "facilities",
    use_case_name: "Facilities",
    status: "invalid",
    is_active: false,
    readiness_state: "invalid",
    readiness_message: "At least one valid FAQ entry is required",
    updated_at: "2026-05-20T00:00:00Z",
  },
] as const;

describe("FaqSourcesList", () => {
  it("renders source list with text status labels", () => {
    const markup = renderToStaticMarkup(<FaqSourcesList sources={[...sources]} state="ready" />);

    expect(markup).toContain("Employee handbook FAQ");
    expect(markup).toContain("Active source");
    expect(markup).toContain("Invalid source");
    expect(markup).toContain("At least one valid FAQ entry is required");
  });

  it("renders loading, empty, and error states", () => {
    expect(renderToStaticMarkup(<FaqSourcesList sources={[]} state="loading" />)).toContain(
      "Loading FAQ sources",
    );
    expect(renderToStaticMarkup(<FaqSourcesList sources={[]} state="empty" />)).toContain(
      "No FAQ sources",
    );
    expect(renderToStaticMarkup(<FaqSourcesList sources={[]} state="error" />)).toContain(
      "Could not load FAQ sources",
    );
  });
});

describe("FaqSourceDetail", () => {
  it("renders source detail actions and readiness", () => {
    const markup = renderToStaticMarkup(
      <FaqSourceDetail
        source={{
          ...sources[0],
          entries: [
            {
              question_text: "How do I update tax declarations?",
              answer_text: "Use payroll self-service.",
              keywords: ["tax"],
            },
          ],
          warnings: [],
        }}
      />,
    );

    expect(markup).toContain("Employee handbook FAQ");
    expect(markup).toContain("Activate");
    expect(markup).toContain("Deactivate");
    expect(markup).toContain("Archive");
    expect(markup).toContain("Use payroll self-service.");
  });
});

describe("faqSources service", () => {
  it("uses contract paths for source lifecycle calls", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ "Content-Type": "application/json" }),
      json: async () => ({ id: "src-1" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await faqSourcesService.listFaqSources();
    await faqSourcesService.getFaqSource("src-1");
    await faqSourcesService.createFaqSource({ name: "FAQ", use_case_id: "hr", entries: [] });
    await faqSourcesService.updateFaqSource("src-1", { name: "Updated" });
    await faqSourcesService.activateFaqSource("src-1");
    await faqSourcesService.deactivateFaqSource("src-1");
    await faqSourcesService.archiveFaqSource("src-1");
    await faqSourcesService.deleteFaqSource("src-1");

    expect(fetchMock).toHaveBeenCalledWith("/admin/faq-sources", expect.any(Object));
    expect(fetchMock).toHaveBeenCalledWith("/admin/faq-sources/src-1", expect.any(Object));
    expect(fetchMock).toHaveBeenCalledWith("/admin/faq-sources/src-1/activate", expect.any(Object));
    expect(fetchMock).toHaveBeenCalledWith("/admin/faq-sources/src-1/deactivate", expect.any(Object));
    expect(fetchMock).toHaveBeenCalledWith("/admin/faq-sources/src-1/archive", expect.any(Object));
    vi.unstubAllGlobals();
  });
});
