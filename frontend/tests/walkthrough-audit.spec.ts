import { test, expect } from "@playwright/test";

test.setTimeout(300000);

const BREAKPOINTS = [
  { name: "mobile-390", width: 390, height: 844 },
  { name: "tablet-768", width: 768, height: 1024 },
  { name: "desktop-1440", width: 1440, height: 900 },
];

const PAGES = [
  { path: "/", label: "landing" },
  { path: "/dashboard", label: "dashboard" },
  { path: "/courses", label: "courses" },
  { path: "/courses/1", label: "course-workspace-1" },
  { path: "/sections", label: "sections" },
  { path: "/sections/mathematics", label: "section-mathematics" },
  { path: "/learning", label: "learning" },
  { path: "/resources", label: "resources" },
  { path: "/settings", label: "settings" },
  { path: "/chat/1?course=11", label: "chat-1" },
];

const SCREENSHOT_ROOT = "D:/AQVERA/artifacts/user-walkthrough/screenshots";

const allResults: any[] = [];
const allConsoleErrors: any[] = [];
const allFailedRequests: any[] = [];

for (const bp of BREAKPOINTS) {
  test(`walkthrough ${bp.name}`, async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: bp.width, height: bp.height },
    });
    context.on("console", (m) => {
      if (m.type() === "error")
        allConsoleErrors.push({ breakpoint: bp.name, type: "console", text: m.text() });
    });
    context.on("requestfailed", (req) =>
      allFailedRequests.push({ breakpoint: bp.name, method: req.method(), url: req.url() })
    );

    const page = await context.newPage();

    page.on("pageerror", (e: Error) =>
      allConsoleErrors.push({ breakpoint: bp.name, type: "pageerror", message: String(e.message) })
    );

    for (const pg of PAGES) {
      const entry: any = {
        breakpoint: bp.name,
        page: pg.label,
        url: pg.path,
        title: null,
        status: null,
        bodyText: null,
        interactions: [],
        errors: [],
      };

      try {
        const res = await page.goto(pg.path, { waitUntil: "load", timeout: 20000 });
        entry.status = res?.status();
        entry.title = await page.title().catch(() => null);
        entry.bodyText = (await page.locator("body").innerText().catch(() => "")).slice(0, 400);
      } catch (e) {
        entry.errors.push(`navigation failed: ${String(e)}`);
      }

      try {
        await page.screenshot({
          path: `${SCREENSHOT_ROOT}/${bp.name}-${pg.label}.png`,
          fullPage: true,
        });
      } catch {}

      if (bp.name !== "mobile-390") {
        for (const item of [
          "Dashboard",
          "Course Library",
          "Academic Sections",
          "Learning Progress",
          "Study Resources",
          "Settings",
        ]) {
          try {
            const link = page.getByRole("link", { name: item });
            if ((await link.count()) > 0) {
              await link.first().click();
              await page.waitForTimeout(500);
              entry.interactions.push({ action: `click nav "${item}"`, url: page.url() });
            }
          } catch (e) {
            entry.errors.push(`click nav "${item}": ${String(e)}`);
          }
        }
      }

      try {
        if (pg.label === "landing") {
          const start = page.getByRole("link", { name: /Start learning/ });
          if ((await start.count()) > 0) {
            await start.first().click();
            await page.waitForTimeout(500);
            entry.interactions.push({ action: "click 'Start learning'", url: page.url() });
          }
        }
        if (pg.label === "courses") {
          const create = page.getByRole("button", { name: /Create course/ });
          if ((await create.count()) > 0) {
            await create.first().click();
            await page.waitForTimeout(500);
            const titleInput = page.getByLabel(/Course title/);
            if ((await titleInput.count()) > 0) {
              await titleInput.first().fill("QA Walkthrough Test Course");
              await page.waitForTimeout(300);
              entry.interactions.push({ action: "fill course title" });
            }
            const submit = page.getByRole("button", { name: /Create course/ });
            if ((await submit.count()) > 0) {
              await submit.first().click();
              await page.waitForTimeout(800);
              entry.interactions.push({ action: "submit create course" });
            }
          }
        }
        if (pg.label === "course-workspace-1") {
          const newChat = page.getByRole("button", { name: /New chat/ });
          if ((await newChat.count()) > 0) {
            await newChat.first().click();
            await page.waitForTimeout(500);
            entry.interactions.push({ action: "click 'New chat'" });
            const titleInput = page.getByLabel(/Conversation title/);
            if ((await titleInput.count()) > 0) {
              await titleInput.first().fill("QA Walkthrough Conversation");
              const start = page.getByRole("button", { name: /Start chat/ });
              if ((await start.count()) > 0) {
                await start.first().click();
                await page.waitForTimeout(800);
                entry.interactions.push({ action: "create conversation via workspace" });
              }
            }
          }
        }
        if (pg.label === "chat-1") {
          const input = page.getByPlaceholder(/Ask anything/);
          if ((await input.count()) > 0) {
            await input.first().fill("What is the derivative of x squared?");
            await page.waitForTimeout(300);
            const send = page.getByRole("button", { name: /Send/ });
            if ((await send.count()) > 0) {
              await send.first().click();
              await page.waitForTimeout(1000);
              entry.interactions.push({ action: "send chat message" });
            }
          }
        }
        if (pg.label === "settings") {
          const inputs = page.locator("input, textarea, select");
          entry.interactions.push({ action: "count settings inputs", value: await inputs.count() });
        }
      } catch (e) {
        entry.errors.push(`interaction error: ${String(e)}`);
      }

      allResults.push(entry);
    }

    await context.close();

    const fs = require("fs");
    fs.writeFileSync(
      `D:/AQVERA/artifacts/user-walkthrough/results-${bp.name}.json`,
      JSON.stringify(
        { results: allResults.filter((r) => r.breakpoint === bp.name), consoleErrors: allConsoleErrors.filter((c) => c.breakpoint === bp.name), failedRequests: allFailedRequests.filter((f) => f.breakpoint === bp.name) },
        null,
        2
      )
    );
  });
}

test("report results", async () => {
  const fs = require("fs");
  fs.writeFileSync(
    "D:/AQVERA/artifacts/user-walkthrough/walkthrough-results.json",
    JSON.stringify(
      { results: allResults, consoleErrors: allConsoleErrors, failedRequests: allFailedRequests },
      null,
      2
    )
  );
  process.stdout.write(`\n=== WALKTHROUGH RESULTS (${allResults.length} page-breakpoint combos) ===\n`);
  for (const r of allResults) {
    process.stdout.write(
      `[${r.breakpoint}] ${r.page} (${r.url}) status=${r.status} title="${r.title}" interactions=${r.interactions.length} errors=${r.errors.length}\n`
    );
  }
  process.stdout.write(`\n=== CONSOLE ERRORS (${allConsoleErrors.length}) ===\n${allConsoleErrors.map((c) => JSON.stringify(c)).join("\n")}\n`);
  process.stdout.write(`\n=== FAILED REQUESTS (${allFailedRequests.length}) ===\n${allFailedRequests.map((f) => `${f.method} ${f.url}`).join("\n")}\n`);
});
