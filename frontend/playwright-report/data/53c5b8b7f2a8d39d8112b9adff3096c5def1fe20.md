# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: ux-accessibility.spec.ts >> AQVERA Accessibility Audit (axe-core) >> no critical/serious violations on dashboard
- Location: tests\ux-accessibility.spec.ts:17:5

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  -   1
+ Received  + 276

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
+                   ".hover\\:bg-surface\\/50.rounded-md[href$=\"sections\"]",
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
+               "height": 17,
+               "minSize": 24,
+               "width": 31.1,
+             },
+             "id": "target-size",
+             "impact": "serious",
+             "message": "Target has insufficient size (31.1px by 17px, should be at least 24px by 24px)",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "closestOffset": 19,
+               "minOffset": 24,
+             },
+             "id": "target-offset",
+             "impact": "serious",
+             "message": "Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 19px instead of at least 24px.",
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
+   Target has insufficient size (31.1px by 17px, should be at least 24px by 24px)
+   Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 19px instead of at least 24px.",
+         "html": "<a class=\"flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium text-muted hover:text-ink hover:bg-surface/50 transition-colors\" href=\"/chat/3?course=12\">ضض</a>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           ".hover\\:bg-surface\\/50.rounded-md[href=\"/chat/3?course=12\"]",
+         ],
+       },
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": Object {
+               "height": 21,
+               "minSize": 24,
+               "width": 86,
+             },
+             "id": "target-size",
+             "impact": "serious",
+             "message": "Target has insufficient size (86px by 21px, should be at least 24px by 24px)",
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
+                 "html": "<a class=\"flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium text-muted hover:text-ink hover:bg-surface/50 transition-colors\" href=\"/chat/2?course=11\">Derivatives Practice</a>",
+                 "target": Array [
+                   ".hover\\:bg-surface\\/50.rounded-md[href=\"/chat/2?course=11\"]",
+                 ],
+               },
+             ],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Target has insufficient size (86px by 21px, should be at least 24px by 24px)
+   Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 23px instead of at least 24px.",
+         "html": "<button class=\"w-full flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium text-ink bg-surface hover:bg-surface/80 transition-colors\">+ New Chat</button>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           ".w-full",
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
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": Object {
+               "height": 17,
+               "minSize": 24,
+               "width": 73.7,
+             },
+             "id": "target-size",
+             "impact": "serious",
+             "message": "Target has insufficient size (73.7px by 17px, should be at least 24px by 24px)",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": Object {
+               "closestOffset": 19,
+               "minOffset": 24,
+             },
+             "id": "target-offset",
+             "impact": "serious",
+             "message": "Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 19px instead of at least 24px.",
+             "relatedNodes": Array [
+               Object {
+                 "html": "<a class=\"group relative block bg-white border border-border rounded-xl p-6 hover:border-sage-dark/40 transition-colors\" href=\"/sections/mathematics\">",
+                 "target": Array [
+                   ".relative.block[href$=\"mathematics\"]",
+                 ],
+               },
+             ],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Target has insufficient size (73.7px by 17px, should be at least 24px by 24px)
+   Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 19px instead of at least 24px.",
+         "html": "<a href=\"/sections\"><span class=\"text-sm font-medium text-muted hover:text-ink transition-colors\">View all →</span></a>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           ".mb-6.justify-between.items-center > a[href$=\"sections\"]",
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
- generic [active] [ref=e1]:
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
            - generic [ref=e38]:
              - link "ضض" [ref=e39] [cursor=pointer]:
                - /url: /chat/3?course=12
              - link "Derivatives Practice" [ref=e40] [cursor=pointer]:
                - /url: /chat/2?course=11
              - link "Limits & Continuity" [ref=e41] [cursor=pointer]:
                - /url: /chat/1?course=11
        - button "+ New Chat" [ref=e43]
      - main [ref=e44]:
        - generic [ref=e46]:
          - button "Open navigation" [ref=e47]: ☰
          - img "AQVERA" [ref=e49]:
            - img "AQVERA" [ref=e50]
            - generic [ref=e54]: AQVERAAcademic Learning
          - button "Help" [ref=e56]
        - generic [ref=e58]:
          - generic [ref=e59]:
            - generic [ref=e60]:
              - generic [ref=e61]:
                - img "AQVERA" [ref=e62]:
                  - img "AQVERA" [ref=e63]
                  - generic [ref=e67]: AQVERAAcademic Learning
                - text: Dashboard
              - paragraph [ref=e68]: Your academic courses, sections, and recent conversations.
            - button "+ Create course" [ref=e69]
          - generic [ref=e70]:
            - generic [ref=e71]:
              - heading "Academic Sections" [level=2] [ref=e72]
              - link "View all →" [ref=e73] [cursor=pointer]:
                - /url: /sections
            - generic [ref=e74]:
              - link "∑ Mathematics & Statistics Explore courses" [ref=e75] [cursor=pointer]:
                - /url: /sections/mathematics
                - generic [ref=e76]: ∑
                - heading "Mathematics & Statistics" [level=3] [ref=e77]
                - paragraph [ref=e78]: Explore courses
              - link "</> Programming & Computer Science Explore courses" [ref=e79] [cursor=pointer]:
                - /url: /sections/programming
                - generic [ref=e80]: </>
                - heading "Programming & Computer Science" [level=3] [ref=e81]
                - paragraph [ref=e82]: Explore courses
              - link "💬 Languages Explore courses" [ref=e83] [cursor=pointer]:
                - /url: /sections/languages
                - generic [ref=e84]: 💬
                - heading "Languages" [level=3] [ref=e85]
                - paragraph [ref=e86]: Explore courses
              - link "⚗️ Natural Sciences Explore courses" [ref=e87] [cursor=pointer]:
                - /url: /sections/natural-sciences
                - generic [ref=e88]: ⚗️
                - heading "Natural Sciences" [level=3] [ref=e89]
                - paragraph [ref=e90]: Explore courses
              - link "🏛️ Humanities & Social Sciences Explore courses" [ref=e91] [cursor=pointer]:
                - /url: /sections/humanities
                - generic [ref=e92]: 🏛️
                - heading "Humanities & Social Sciences" [level=3] [ref=e93]
                - paragraph [ref=e94]: Explore courses
          - generic [ref=e95]:
            - heading "Continue Learning" [level=2] [ref=e97]
            - generic [ref=e98]:
              - link "📘 Nov 16, 01:17 AM Get Test Course mathematics Open course→" [ref=e99] [cursor=pointer]:
                - /url: /courses/45
                - generic [ref=e101]:
                  - generic [ref=e102]: 📘
                  - text: Nov 16, 01:17 AM
                - heading "Get Test Course" [level=3] [ref=e103]
                - paragraph [ref=e104]: mathematics
                - generic [ref=e105]: Open course→
              - link "📘 Nov 16, 01:17 AM Updated Title mathematics Open course→" [ref=e106] [cursor=pointer]:
                - /url: /courses/46
                - generic [ref=e108]:
                  - generic [ref=e109]: 📘
                  - text: Nov 16, 01:17 AM
                - heading "Updated Title" [level=3] [ref=e110]
                - paragraph [ref=e111]: mathematics
                - generic [ref=e112]: Open course→
              - link "📘 Nov 16, 01:17 AM Introduction to Mathematics mathematics Open course→" [ref=e113] [cursor=pointer]:
                - /url: /courses/43
                - generic [ref=e115]:
                  - generic [ref=e116]: 📘
                  - text: Nov 16, 01:17 AM
                - heading "Introduction to Mathematics" [level=3] [ref=e117]
                - paragraph [ref=e118]: mathematics
                - generic [ref=e119]: Open course→
          - generic [ref=e120]:
            - generic [ref=e121]:
              - heading "Recent Conversations" [level=2] [ref=e122]
              - link "View all →" [ref=e123] [cursor=pointer]:
                - /url: /chat
            - generic [ref=e124]:
              - link [ref=e125] [cursor=pointer]:
                - /url: /chat/3?course=12
                - generic [ref=e126]:
                  - heading "ضض" [level=3] [ref=e127]
                  - paragraph [ref=e128]: Nov 16, 12:04 AM
                - text: →
              - link [ref=e129] [cursor=pointer]:
                - /url: /chat/2?course=11
                - generic [ref=e130]:
                  - heading "Derivatives Practice" [level=3] [ref=e131]
                  - paragraph [ref=e132]: Nov 15, 11:01 PM
                - text: →
              - link [ref=e133] [cursor=pointer]:
                - /url: /chat/1?course=11
                - generic [ref=e134]:
                  - heading "Limits & Continuity" [level=3] [ref=e135]
                  - paragraph [ref=e136]: Nov 15, 11:00 PM
                - text: →
          - generic [ref=e137]:
            - heading "Quick Actions" [level=2] [ref=e139]
            - generic [ref=e140]:
              - 'button "📎 Upload Materials Coming soon: attach lecture notes and documents" [ref=e141]':
                - generic [ref=e142]: 📎
                - heading "Upload Materials" [level=3] [ref=e143]
                - paragraph [ref=e144]: "Coming soon: attach lecture notes and documents"
              - button "💬 Start New Chat Begin a new learning conversation" [ref=e145]:
                - generic [ref=e146]: 💬
                - heading "Start New Chat" [level=3] [ref=e147]
                - paragraph [ref=e148]: Begin a new learning conversation
              - button "📚 Explore Courses Browse the course library" [ref=e149]:
                - generic [ref=e150]: 📚
                - heading "Explore Courses" [level=3] [ref=e151]
                - paragraph [ref=e152]: Browse the course library
          - generic [ref=e153]:
            - heading "Your Courses" [level=2] [ref=e155]
            - generic [ref=e156]:
              - generic [ref=e157]:
                - generic [ref=e158]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e159]
                - paragraph [ref=e160]: MATH101
                - generic [ref=e161]:
                  - text: Fall 2026
                  - link "Open" [ref=e162] [cursor=pointer]:
                    - /url: /courses/1
              - generic [ref=e163]:
                - generic [ref=e164]: mathematics
                - heading "List Test Course" [level=3] [ref=e165]
                - link "Open" [ref=e167] [cursor=pointer]:
                  - /url: /courses/2
              - generic [ref=e168]:
                - generic [ref=e169]: mathematics
                - heading "Get Test Course" [level=3] [ref=e170]
                - link "Open" [ref=e172] [cursor=pointer]:
                  - /url: /courses/3
              - generic [ref=e173]:
                - generic [ref=e174]: mathematics
                - heading "Updated Title" [level=3] [ref=e175]
                - link "Open" [ref=e177] [cursor=pointer]:
                  - /url: /courses/4
              - generic [ref=e178]:
                - generic [ref=e179]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e180]
                - paragraph [ref=e181]: MATH101
                - generic [ref=e182]:
                  - text: Fall 2026
                  - link "Open" [ref=e183] [cursor=pointer]:
                    - /url: /courses/6
              - generic [ref=e184]:
                - generic [ref=e185]: mathematics
                - heading "List Test Course" [level=3] [ref=e186]
                - link "Open" [ref=e188] [cursor=pointer]:
                  - /url: /courses/7
              - generic [ref=e189]:
                - generic [ref=e190]: mathematics
                - heading "Get Test Course" [level=3] [ref=e191]
                - link "Open" [ref=e193] [cursor=pointer]:
                  - /url: /courses/8
              - generic [ref=e194]:
                - generic [ref=e195]: mathematics
                - heading "Updated Title" [level=3] [ref=e196]
                - link "Open" [ref=e198] [cursor=pointer]:
                  - /url: /courses/9
              - generic [ref=e199]:
                - generic [ref=e200]: mathematics
                - heading "Calculus" [level=3] [ref=e201]
                - paragraph [ref=e202]: MATH101
                - generic [ref=e203]:
                  - text: Fall 2026
                  - link "Open" [ref=e204] [cursor=pointer]:
                    - /url: /courses/11
              - generic [ref=e205]:
                - generic [ref=e206]: "23"
                - heading "علوم" [level=3] [ref=e207]
                - paragraph [ref=e208]: "3434"
                - generic [ref=e209]:
                  - text: "1"
                  - link "Open" [ref=e210] [cursor=pointer]:
                    - /url: /courses/12
              - generic [ref=e211]:
                - generic [ref=e212]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e213]
                - paragraph [ref=e214]: MATH101
                - generic [ref=e215]:
                  - text: Fall 2026
                  - link "Open" [ref=e216] [cursor=pointer]:
                    - /url: /courses/13
              - generic [ref=e217]:
                - generic [ref=e218]: mathematics
                - heading "List Test Course" [level=3] [ref=e219]
                - link "Open" [ref=e221] [cursor=pointer]:
                  - /url: /courses/14
              - generic [ref=e222]:
                - generic [ref=e223]: mathematics
                - heading "Get Test Course" [level=3] [ref=e224]
                - link "Open" [ref=e226] [cursor=pointer]:
                  - /url: /courses/15
              - generic [ref=e227]:
                - generic [ref=e228]: mathematics
                - heading "Updated Title" [level=3] [ref=e229]
                - link "Open" [ref=e231] [cursor=pointer]:
                  - /url: /courses/16
              - generic [ref=e232]:
                - generic [ref=e233]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e234]
                - paragraph [ref=e235]: MATH101
                - generic [ref=e236]:
                  - text: Fall 2026
                  - link "Open" [ref=e237] [cursor=pointer]:
                    - /url: /courses/18
              - generic [ref=e238]:
                - generic [ref=e239]: mathematics
                - heading "List Test Course" [level=3] [ref=e240]
                - link "Open" [ref=e242] [cursor=pointer]:
                  - /url: /courses/19
              - generic [ref=e243]:
                - generic [ref=e244]: mathematics
                - heading "Get Test Course" [level=3] [ref=e245]
                - link "Open" [ref=e247] [cursor=pointer]:
                  - /url: /courses/20
              - generic [ref=e248]:
                - generic [ref=e249]: mathematics
                - heading "Updated Title" [level=3] [ref=e250]
                - link "Open" [ref=e252] [cursor=pointer]:
                  - /url: /courses/21
              - generic [ref=e253]:
                - generic [ref=e254]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e255]
                - paragraph [ref=e256]: MATH101
                - generic [ref=e257]:
                  - text: Fall 2026
                  - link "Open" [ref=e258] [cursor=pointer]:
                    - /url: /courses/23
              - generic [ref=e259]:
                - generic [ref=e260]: mathematics
                - heading "List Test Course" [level=3] [ref=e261]
                - link "Open" [ref=e263] [cursor=pointer]:
                  - /url: /courses/24
              - generic [ref=e264]:
                - generic [ref=e265]: mathematics
                - heading "Get Test Course" [level=3] [ref=e266]
                - link "Open" [ref=e268] [cursor=pointer]:
                  - /url: /courses/25
              - generic [ref=e269]:
                - generic [ref=e270]: mathematics
                - heading "Updated Title" [level=3] [ref=e271]
                - link "Open" [ref=e273] [cursor=pointer]:
                  - /url: /courses/26
              - generic [ref=e274]:
                - generic [ref=e275]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e276]
                - paragraph [ref=e277]: MATH101
                - generic [ref=e278]:
                  - text: Fall 2026
                  - link "Open" [ref=e279] [cursor=pointer]:
                    - /url: /courses/28
              - generic [ref=e280]:
                - generic [ref=e281]: mathematics
                - heading "List Test Course" [level=3] [ref=e282]
                - link "Open" [ref=e284] [cursor=pointer]:
                  - /url: /courses/29
              - generic [ref=e285]:
                - generic [ref=e286]: mathematics
                - heading "Get Test Course" [level=3] [ref=e287]
                - link "Open" [ref=e289] [cursor=pointer]:
                  - /url: /courses/30
              - generic [ref=e290]:
                - generic [ref=e291]: mathematics
                - heading "Updated Title" [level=3] [ref=e292]
                - link "Open" [ref=e294] [cursor=pointer]:
                  - /url: /courses/31
              - generic [ref=e295]:
                - generic [ref=e296]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e297]
                - paragraph [ref=e298]: MATH101
                - generic [ref=e299]:
                  - text: Fall 2026
                  - link "Open" [ref=e300] [cursor=pointer]:
                    - /url: /courses/33
              - generic [ref=e301]:
                - generic [ref=e302]: mathematics
                - heading "List Test Course" [level=3] [ref=e303]
                - link "Open" [ref=e305] [cursor=pointer]:
                  - /url: /courses/34
              - generic [ref=e306]:
                - generic [ref=e307]: mathematics
                - heading "Get Test Course" [level=3] [ref=e308]
                - link "Open" [ref=e310] [cursor=pointer]:
                  - /url: /courses/35
              - generic [ref=e311]:
                - generic [ref=e312]: mathematics
                - heading "Updated Title" [level=3] [ref=e313]
                - link "Open" [ref=e315] [cursor=pointer]:
                  - /url: /courses/36
              - generic [ref=e316]:
                - generic [ref=e317]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e318]
                - paragraph [ref=e319]: MATH101
                - generic [ref=e320]:
                  - text: Fall 2026
                  - link "Open" [ref=e321] [cursor=pointer]:
                    - /url: /courses/38
              - generic [ref=e322]:
                - generic [ref=e323]: mathematics
                - heading "List Test Course" [level=3] [ref=e324]
                - link "Open" [ref=e326] [cursor=pointer]:
                  - /url: /courses/39
              - generic [ref=e327]:
                - generic [ref=e328]: mathematics
                - heading "Get Test Course" [level=3] [ref=e329]
                - link "Open" [ref=e331] [cursor=pointer]:
                  - /url: /courses/40
              - generic [ref=e332]:
                - generic [ref=e333]: mathematics
                - heading "Updated Title" [level=3] [ref=e334]
                - link "Open" [ref=e336] [cursor=pointer]:
                  - /url: /courses/41
              - generic [ref=e337]:
                - generic [ref=e338]: mathematics
                - heading "Introduction to Mathematics" [level=3] [ref=e339]
                - paragraph [ref=e340]: MATH101
                - generic [ref=e341]:
                  - text: Fall 2026
                  - link "Open" [ref=e342] [cursor=pointer]:
                    - /url: /courses/43
              - generic [ref=e343]:
                - generic [ref=e344]: mathematics
                - heading "List Test Course" [level=3] [ref=e345]
                - link "Open" [ref=e347] [cursor=pointer]:
                  - /url: /courses/44
              - generic [ref=e348]:
                - generic [ref=e349]: mathematics
                - heading "Get Test Course" [level=3] [ref=e350]
                - link "Open" [ref=e352] [cursor=pointer]:
                  - /url: /courses/45
              - generic [ref=e353]:
                - generic [ref=e354]: mathematics
                - heading "Updated Title" [level=3] [ref=e355]
                - link "Open" [ref=e357] [cursor=pointer]:
                  - /url: /courses/46
  - alert [ref=e358]
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