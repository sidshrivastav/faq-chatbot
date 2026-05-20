/**
 * T044 – AnswerFeedback component tests.
 *
 * Covers:
 * - Default state renders helpful and unhelpful buttons with accessible names
 * - Saved state renders confirmation text (not color-only)
 * - Optional comment textarea is present
 * - Error state renders error text and preserves comment
 * - Buttons have accessible labels
 */
import { describe, expect, it } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { AnswerFeedback } from "../src/components/feedback/AnswerFeedback";

describe("AnswerFeedback – default state", () => {
  it("renders helpful and unhelpful buttons", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="idle" />,
    );
    expect(markup).toContain("Helpful");
    expect(markup).toContain("Unhelpful");
  });

  it("buttons have aria-labels for accessibility", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="idle" />,
    );
    expect(markup).toMatch(/aria-label="Mark as helpful"/);
    expect(markup).toMatch(/aria-label="Mark as unhelpful"/);
  });

  it("renders optional comment textarea", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="idle" />,
    );
    expect(markup).toMatch(/comment|Comment/);
  });
});

describe("AnswerFeedback – saved state", () => {
  it("renders saved confirmation text, not only color", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="saved" rating="helpful" />,
    );
    expect(markup).toMatch(/thank|saved|recorded/i);
  });

  it("shows which rating was saved", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="saved" rating="unhelpful" />,
    );
    expect(markup).toMatch(/unhelpful/i);
  });
});

describe("AnswerFeedback – reason selector (TC03)", () => {
  it("shows reason selector when selectedRating is unhelpful", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="idle" selectedRating="unhelpful" />,
    );
    expect(markup).toMatch(/incorrect_answer|not_specific_enough|missing_from_faq|confusing_response|outdated_source/);
  });

  it("does not show reason selector in plain idle state", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="idle" />,
    );
    expect(markup).not.toMatch(/incorrect_answer|not_specific_enough|missing_from_faq/);
  });

  it("each reason option has a human-readable label", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="idle" selectedRating="unhelpful" />,
    );
    expect(markup).toMatch(/Incorrect answer/i);
    expect(markup).toMatch(/Not specific enough/i);
    expect(markup).toMatch(/Missing from FAQ/i);
    expect(markup).toMatch(/Confusing response/i);
    expect(markup).toMatch(/Outdated source/i);
  });

  it("reason options use input elements with accessible labels", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback answerId="ans-1" state="idle" selectedRating="unhelpful" />,
    );
    expect(markup).toContain('type="radio"');
  });
});

describe("AnswerFeedback – error state", () => {
  it("renders error text on submission failure", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback
        answerId="ans-1"
        state="error"
        comment="Too vague."
      />,
    );
    expect(markup).toMatch(/error|try again/i);
  });

  it("preserves comment on error so user can retry", () => {
    const markup = renderToStaticMarkup(
      <AnswerFeedback
        answerId="ans-1"
        state="error"
        comment="Too vague."
      />,
    );
    expect(markup).toContain("Too vague.");
  });
});
