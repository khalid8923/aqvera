import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const pages = [
  { path: "/", label: "landing" },
  { path: "/dashboard", label: "dashboard" },
  { path: "/courses", label: "course-library" },
  { path: "/courses/1", label: "course-workspace" },
  { path: "/sections", label: "sections-explorer" },
  { path: "/sections/mathematics", label: "section-page" },
  { path: "/chat/general-calculus", label: "chat" },
  { path: "/settings", label: "settings" },
];

test.describe("AQVERA Accessibility Audit (axe-core)", () => {
  for (const { path, label } of pages) {
    test(`no critical/serious violations on ${label}`, async ({ page }) => {
      await page.goto(path);
      await page.waitForLoadState("networkidle");

      const results = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
        .analyze();

      const violations = results.violations.filter(
        (v) => v.impact === "critical" || v.impact === "serious"
      );

      expect(violations).toEqual([]);
    });
  }
});
