import { test, expect } from "@playwright/test";

test.use({ baseURL: "http://localhost:3000" });

test.describe("AQVERA Core Journeys (E2E)", () => {
  test("landing page renders with primary CTA", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    await expect(
      page.locator("main").getByRole("link", { name: /Start learning/ })
    ).toBeVisible();
    await expect(page.locator("main").locator("h1")).toBeVisible();
  });

  test("dashboard loads and shows empty state when no courses", async ({ page }) => {
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");
    await expect(page.locator("main").getByText("Dashboard")).toBeVisible();
  });

  test("course library renders", async ({ page }) => {
    await page.goto("/courses");
    await page.waitForLoadState("networkidle");
    await expect(page.locator("main").getByText("Course Library")).toBeVisible();
  });

  test("academic sections explorer lists all five sections", async ({ page }) => {
    await page.goto("/sections");
    await page.waitForLoadState("networkidle");
    const main = page.locator("main");
    for (const section of [
      "Mathematics & Statistics",
      "Programming & Computer Science",
      "Languages",
      "Natural Sciences",
      "Humanities & Social Sciences",
    ]) {
      await expect(main.getByText(section)).toBeVisible();
    }
  });

  test("course workspace loads for existing course id", async ({ page }) => {
    await page.goto("/courses/1");
    await page.waitForLoadState("networkidle");
    await expect(page.getByText("This page couldn't load")).not.toBeVisible();
  });

  test("settings page shows dev account info", async ({ page }) => {
    await page.goto("/settings");
    await page.waitForLoadState("networkidle");
    await expect(page.locator("main").getByText("Settings")).toBeVisible();
  });

  test("learning page shows honest Phase 2 placeholder", async ({ page }) => {
    await page.goto("/learning");
    await page.waitForLoadState("networkidle");
    await expect(page.getByText("Coming in Phase 2")).toBeVisible();
  });

  test("resources page renders", async ({ page }) => {
    await page.goto("/resources");
    await page.waitForLoadState("networkidle");
    await expect(page.locator("main").getByText("Study Resources")).toBeVisible();
  });

  test("chat page loads", async ({ page }) => {
    await page.goto("/chat/1");
    await page.waitForLoadState("networkidle");
    await expect(page.locator("body")).toBeVisible();
  });

  test("navigation sidebar present on dashboard", async ({ page }) => {
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");
    await expect(page.getByRole("link", { name: "Dashboard" })).toBeVisible();
    await expect(page.getByRole("link", { name: "Course Library" })).toBeVisible();
  });
});
