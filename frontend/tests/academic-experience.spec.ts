import { test, expect } from "@playwright/test";

test.use({ baseURL: "http://localhost:3000" });

test.describe("Academic Sections", () => {
  test("sections explorer lists all five sections", async ({ page }) => {
    await page.goto("/sections");
    await page.waitForLoadState("networkidle");

    const main = page.locator("main");
    await expect(main.getByText("Mathematics & Statistics")).toBeVisible();
    await expect(main.getByText("Programming & Computer Science")).toBeVisible();
    await expect(main.getByText("Languages")).toBeVisible();
    await expect(main.getByText("Natural Sciences")).toBeVisible();
    await expect(main.getByText("Humanities & Social Sciences")).toBeVisible();
  });

  test("clicking a section opens the section page", async ({ page }) => {
    await page.goto("/sections");
    await page.waitForLoadState("networkidle");

    await page
      .locator("main")
      .getByRole("link", { name: "Mathematics & Statistics" })
      .click();
    await expect(page).toHaveURL(/.*\/sections\/mathematics/);
    await expect(
      page.locator("main").getByText("Mathematics & Statistics")
    ).toBeVisible();
    await expect(
      page.locator("main").getByRole("heading", { name: "Calculus" })
    ).toBeVisible();
  });
});

test.describe("Course Workspace", () => {
  test("course workspace renders without crashing", async ({ page }) => {
    await page.goto("/courses/1");
    await page.waitForLoadState("networkidle");

    await expect(page.getByText("This page couldn't load")).not.toBeVisible();
  });
});

test.describe("AI Chat", () => {
  test("chat page loads with welcome message", async ({ page }) => {
    await page.goto("/chat/general-calculus");
    await page.waitForLoadState("networkidle");

    await expect(page.getByText(/AQVERA AI learning companion/)).toBeVisible();
  });

  test("sending a message produces an AI response", async ({ page }) => {
    await page.goto("/chat/general-calculus");
    await page.waitForLoadState("networkidle");

    await page
      .getByPlaceholder("Ask anything about your courses…")
      .fill("hello");
    await page.getByRole("button", { name: "Send" }).click();

    await expect(
      page.getByText(/Hello! I'm your AQVERA AI learning companion/)
    ).toBeVisible();
  });
});
