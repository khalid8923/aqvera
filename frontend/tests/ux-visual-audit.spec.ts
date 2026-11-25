import { test } from "@playwright/test";

const AUDIT_DIR = "D:/AQVERA/artifacts/ux-audit";

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

const breakpoints = [
  { name: "mobile", width: 390, height: 844 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1440, height: 900 },
];

test.describe("AQVERA Visual Audit", () => {
  for (const { path, label } of pages) {
    for (const { name, width, height } of breakpoints) {
      test(`captures ${label} at ${name} (${width}x${height})`, async ({
        page,
      }) => {
        await page.setViewportSize({ width, height });
        await page.goto(path);
        await page.waitForLoadState("networkidle");
        await page.screenshot({
          path: `${AUDIT_DIR}/${label}-${name}.png`,
          fullPage: true,
        });
      });
    }
  }
});
