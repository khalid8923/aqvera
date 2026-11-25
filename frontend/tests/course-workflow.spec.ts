import { test, expect } from "@playwright/test";

test.use({ baseURL: "http://localhost:3000" });

test("Course CRUD workflow", async ({ page }) => {
  // Navigate to courses page
  await page.goto("/courses");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(2000);

  // Should start empty (fresh database)
  await expect(page.getByText("No courses yet")).toBeVisible();

  // Create a course via JavaScript (open the modal)
  await page.evaluate(() => {
    const modal = document.getElementById("create-course-modal");
    if (modal) modal.classList.remove("hidden");
  });

  // Wait for modal to open
  await expect(page.getByLabel("Course title")).toBeVisible({ timeout: 5000 });

  // Fill the modal form
  await page.getByLabel("Course title").fill("Introduction to Mathematics");
  await page.getByLabel("Course code").fill("MATH101");
  await page.getByLabel("Semester").fill("Fall 2026");
  await page.getByLabel("Subject domain").fill("Mathematics");
  await page.getByRole("button", { name: "Create course" }).click();

  // Course should appear in the list
  await expect(page.getByText("Introduction to Mathematics")).toBeVisible();
  await expect(page.getByText("MATH101")).toBeVisible();

  // Open the course workspace
  await page.getByRole("button", { name: "Open" }).first().click();
  await expect(page.getByText("Introduction to Mathematics")).toBeVisible();

  // Go back to courses and edit
  await page.goto("/courses");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(1000);
  await page.getByRole("button", { name: "Edit" }).first().click();
  await expect(page.getByLabel("Course title")).toBeVisible({ timeout: 5000 });
  await page.getByLabel("Course title").fill("Advanced Mathematics");
  await page.getByRole("button", { name: "Save changes" }).click();
  await expect(page.getByText("Advanced Mathematics")).toBeVisible();

  // Archive the course
  await page.getByRole("button", { name: "Archive" }).first().click();
  await expect(page.getByText("Archived")).toBeVisible();

  // Show archived
  await page.getByRole("button", { name: "Show archived" }).click();
  await expect(page.getByText("Advanced Mathematics")).toBeVisible();

  // Delete the course
  await page.getByRole("button", { name: "Delete" }).first().click();
  await expect(page.getByText("Advanced Mathematics")).not.toBeVisible();
});
