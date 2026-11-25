import { test, expect } from "@playwright/test";

test.use({ baseURL: "https://children-emissions-framing-gmt.trycloudflare.com" });

test("wait longer after navigation for data", async ({ page }) => {
  await page.goto("/dashboard", { waitUntil: "load", timeout: 30000 });
  // wait for loading to disappear, up to 15s
  try {
    await expect(page.locator("body")).not.toContainText("Loading your dashboard", { timeout: 15000 });
    process.stdout.write("\n=== Loading DISAPPEARED ===\n");
  } catch {
    process.stdout.write("\n=== Loading STILL PRESENT after 15s ===\n");
  }
  const body = await page.locator("body").innerText();
  process.stdout.write(`\n=== BODY: courses=${body.includes("Introduction to Mathematics")} continue=${body.includes("Continue Learning")} noCourses=${body.includes("No courses yet")} ===\n`);
  process.stdout.write(`\n=== BODY (first 1500) ===\n${body.slice(0,1500)}\n`);
});
