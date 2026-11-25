# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: ux-accessibility.spec.ts >> AQVERA Accessibility Audit (axe-core) >> no critical/serious violations on chat
- Location: tests\ux-accessibility.spec.ts:17:5

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  -   1
+ Received  + 150

- Array []
+ Array [
+   Object {
+     "description": "Ensure touch targets have sufficient size and space",
+     "help": "All touch targets must be 24px large, or leave sufficient space",
+     "helpUrl": "https://dequeuniversity.com/rules/axe/4.14/target-size?application=playwright",
+     "id": "target-size",
+     "impact": "serious",
+     "nodes": Array [
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": Object {
+               "height": 17,
+               "minSize": 24,
+               "width": 107.1,
+             },
+             "id": "target-size",
+             "impact": "serious",
+             "message": "Target has insufficient size (107.1px by 17px, should be at least 24px by 24px)",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "closestOffset": 16.6,
+               "minOffset": 24,
+             },
+             "id": "target-offset",
+             "impact": "serious",
+             "message": "Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 16.6px instead of at least 24px.",
+             "relatedNodes": Array [
+               Object {
+                 "html": "<a href=\"/courses\" class=\"flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors text-muted hover:text-ink hover:bg-surface/50\">Course Library</a>",
+                 "target": Array [
+                   "a[href$=\"courses\"]",
+                 ],
+               },
+             ],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Target has insufficient size (107.1px by 17px, should be at least 24px by 24px)
+   Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 16.6px instead of at least 24px.",
+         "html": "<a href=\"/resources\" class=\"flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors text-muted hover:text-ink hover:bg-surface/50\">Study Resources</a>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           "a[href$=\"resources\"]",
+         ],
+       },
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": Object {
+               "height": 17,
+               "minSize": 24,
+               "width": 51.6,
+             },
+             "id": "target-size",
+             "impact": "serious",
+             "message": "Target has insufficient size (51.6px by 17px, should be at least 24px by 24px)",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "closestOffset": 9.8,
+               "minOffset": 24,
+             },
+             "id": "target-offset",
+             "impact": "serious",
+             "message": "Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 9.8px instead of at least 24px.",
+             "relatedNodes": Array [
+               Object {
+                 "html": "<a href=\"/sections\" class=\"flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors text-muted hover:text-ink hover:bg-surface/50\">Academic Sections</a>",
+                 "target": Array [
+                   "a[href$=\"sections\"]",
+                 ],
+               },
+               Object {
+                 "html": "<a href=\"/learning\" class=\"flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors text-muted hover:text-ink hover:bg-surface/50\">Learning Progress</a>",
+                 "target": Array [
+                   "a[href$=\"learning\"]",
+                 ],
+               },
+             ],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Target has insufficient size (51.6px by 17px, should be at least 24px by 24px)
+   Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 9.8px instead of at least 24px.",
+         "html": "<a href=\"/settings\" class=\"flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors text-muted hover:text-ink hover:bg-surface/50\">Settings</a>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           "a[href$=\"settings\"]",
+         ],
+       },
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": Object {
+               "height": 23,
+               "minSize": 24,
+               "width": 28,
+             },
+             "id": "target-size",
+             "impact": "serious",
+             "message": "Target has insufficient size (28px by 23px, should be at least 24px by 24px)",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "closestOffset": 23,
+               "minOffset": 24,
+             },
+             "id": "target-offset",
+             "impact": "serious",
+             "message": "Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 23px instead of at least 24px.",
+             "relatedNodes": Array [
+               Object {
+                 "html": "<button class=\"w-full flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium text-ink bg-surface hover:bg-surface/80 transition-colors\">+ New Chat</button>",
+                 "target": Array [
+                   ".w-full",
+                 ],
+               },
+             ],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Target has insufficient size (28px by 23px, should be at least 24px by 24px)
+   Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 23px instead of at least 24px.",
+         "html": "<button class=\"md:hidden p-2 text-muted hover:text-ink\" aria-label=\"Open navigation\">☰</button>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           ".md\\:hidden.p-2[aria-label=\"Open navigation\"]",
+         ],
+       },
+     ],
+     "tags": Array [
+       "cat.sensory-and-visual-cues",
+       "wcag22aa",
+       "wcag258",
+       "EN-301-549v4",
+       "EN-9.2.5.8",
+     ],
+   },
+ ]
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - banner [ref=e3]:
    - img "AQVERA" [ref=e4]:
      - img "AQVERA" [ref=e5]
      - generic [ref=e9]: AQVERAAcademic Learning
    - button "Open navigation" [ref=e10]: ☰
  - generic [ref=e11]:
    - complementary [ref=e12]:
      - img "AQVERA" [ref=e14]:
        - img "AQVERA" [ref=e15]
        - generic [ref=e19]: AQVERAAcademic Learning
      - navigation [ref=e20]:
        - generic [ref=e21]:
          - link "Dashboard" [ref=e22] [cursor=pointer]:
            - /url: /dashboard
          - link "Course Library" [ref=e23] [cursor=pointer]:
            - /url: /courses
          - link "Academic Sections" [ref=e24] [cursor=pointer]:
            - /url: /sections
          - link "Learning Progress" [ref=e25] [cursor=pointer]:
            - /url: /learning
          - link "Study Resources" [ref=e26] [cursor=pointer]:
            - /url: /resources
          - link "Settings" [ref=e27] [cursor=pointer]:
            - /url: /settings
        - generic [ref=e28]:
          - heading "Academic Sections" [level=3] [ref=e29]
          - generic [ref=e30]:
            - link "Mathematics & Statistics" [ref=e31] [cursor=pointer]:
              - /url: /sections/mathematics
            - link "Programming & Computer Science" [ref=e32] [cursor=pointer]:
              - /url: /sections/programming
            - link "Languages" [ref=e33] [cursor=pointer]:
              - /url: /sections/languages
            - link "Natural Sciences" [ref=e34] [cursor=pointer]:
              - /url: /sections/natural-sciences
            - link "Humanities & Social Sciences" [ref=e35] [cursor=pointer]:
              - /url: /sections/humanities
        - generic [ref=e36]:
          - heading "Recent Chats" [level=3] [ref=e37]
          - generic [ref=e38]: No recent conversations
      - button "+ New Chat" [ref=e41]
    - main [ref=e42]:
      - generic [ref=e44]:
        - button "Open navigation" [ref=e45]: ☰
        - img "AQVERA" [ref=e47]:
          - img "AQVERA" [ref=e48]
          - generic [ref=e52]: AQVERAAcademic Learning
        - button "Help" [ref=e54]
      - paragraph [ref=e57]: Loading conversation…
```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | import AxeBuilder from "@axe-core/playwright";
  3  | 
  4  | const pages = [
  5  |   { path: "/", label: "landing" },
  6  |   { path: "/dashboard", label: "dashboard" },
  7  |   { path: "/courses", label: "course-library" },
  8  |   { path: "/courses/1", label: "course-workspace" },
  9  |   { path: "/sections", label: "sections-explorer" },
  10 |   { path: "/sections/mathematics", label: "section-page" },
  11 |   { path: "/chat/general-calculus", label: "chat" },
  12 |   { path: "/settings", label: "settings" },
  13 | ];
  14 | 
  15 | test.describe("AQVERA Accessibility Audit (axe-core)", () => {
  16 |   for (const { path, label } of pages) {
  17 |     test(`no critical/serious violations on ${label}`, async ({ page }) => {
  18 |       await page.goto(path);
  19 |       await page.waitForLoadState("networkidle");
  20 | 
  21 |       const results = await new AxeBuilder({ page })
  22 |         .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
  23 |         .analyze();
  24 | 
  25 |       const violations = results.violations.filter(
  26 |         (v) => v.impact === "critical" || v.impact === "serious"
  27 |       );
  28 | 
> 29 |       expect(violations).toEqual([]);
     |                          ^ Error: expect(received).toEqual(expected) // deep equality
  30 |     });
  31 |   }
  32 | });
  33 | 
```