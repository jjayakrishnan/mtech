# mtech — MTech AI/ML (BITS Pilani)

Root workspace for all MTech coursework.

## Structure

```
mtech/
├── semester2/                 current semester (git-tracked)
│   ├── ACI/                   Advanced Computing for AI
│   ├── DRL/                   Deep Reinforcement Learning
│   ├── NLP/                   Natural Language Processing
│   └── SEML/                  Software Engineering for Machine Learning
├── course-materials → symlink (gitignored, points to Google Drive)
└── assignments → symlink      (gitignored, points to Google Drive)
```

Each subject in `semester2/` contains only lightweight, Claude-generated content:
```
semester2/<SUBJECT>/
├── lessons/            interactive lectures and study content
├── learning-records/   learning state metadata (from /teach)
├── MISSION.md          goals and constraints
└── RESOURCES.md        pointers to course-materials via symlink
```

Heavy teacher-provided files (PDFs, PPTXs, zips, books) live on Google Drive:
```
course-materials/
├── {ACI,DRL,NLP,SEML}/
│   ├── slides/
│   ├── webinars/
│   ├── books/
│   ├── past-papers/
│   └── handouts/
```

## Setup

Create symlinks to your local Google Drive path (these are gitignored):
```sh
ln -s /path/to/your/google-drive/courses/semester2/course-materials course-materials
ln -s /path/to/your/google-drive/courses/semester2/assignments assignments
```

## Skills

All skills are registered at `.claude/skills/` and available in every subfolder.

### make-lecture-kit
Turns any lecture (PDF, PPTX, or topic name) into:
- Interactive lecture HTML → goes into `semester2/<SUBJECT>/lessons/`

Trigger: `/make-lecture-kit` or *"use make-lecture-kit on this lecture"*.

### Other skills
`/diagnose`, `/prototype`, `/tdd`, `/grill-me`, `/handoff`, `/teach`, `/write-a-skill`,
`/design-an-interface`, `/qa`, `/review`, `/writing-beats`, `/writing-fragments`, `/writing-shape`, and more.

## Conventions

- `RESOURCES.md` paths use `course-materials/` (the symlink) — never absolute paths with user-specific Drive locations.
- When explaining lecture content: plain English first, analogy before math, fully-worked examples.
- `lessons/` is the single home for all Claude-generated study content (from any skill).

## ADR-001 — Math Rendering: Always Use MathJax

**Decision:** Every formula or mathematical expression in any HTML file produced in this project (study guides, lessons, exam papers, cheat sheets, or any other output) **must be rendered using MathJax**, not written as plain text or ASCII approximations.

**Rules:**
- Load MathJax from cdnjs: `https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-svg.min.js`
- Configure before the script tag: `window.MathJax = { tex: { inlineMath: [['\\(','\\)']], displayMath: [['$$','$$']] }, svg: { fontCache:'global' }, startup: { typeset: false } }`
- Call `MathJax.typesetPromise()` after all DOM is built (on `window.addEventListener('load', ...)`)
- Inline math: `\( formula \)` — e.g. `\( V_\pi(s) \)`, `\( \gamma \)`, `\( \alpha \)`
- Display (block) math: `$$ formula $$` — e.g. `$$ V^*(s) = \max_a \sum_{s'} P(s'|s,a)[R + \gamma V^*(s')] $$`
- Wide equations go inside an `.eqbox` div with `overflow-x: auto` so they scroll in-box, never break the page layout
- **Never** write formulas as plain text like `V*(s) = max_a ...` or `α·[R − Q(a)]` — these are hard fails

**Why:** Plain-text math is ambiguous, visually poor, and inconsistent across documents. MathJax is already the project standard (make-lecture-kit, all lesson HTMLs). Discovered after the DRL exam study guide cheat sheet was generated with ASCII math instead of rendered symbols.

## ADR-003 — Vercel Deploy: Always Sync site/ Before Pushing

**Decision:** Vercel serves from the `site/` directory (configured in `vercel.json`: `"outputDirectory": "site"`). Any HTML file created or modified under `semester2/<SUBJECT>/lessons/` **must also be copied to the corresponding path under `site/semester2/<SUBJECT>/`** before committing and pushing.

**Rules:**
- After creating or editing any lesson file at `semester2/ACI/lessons/foo.html`, run: `cp semester2/ACI/lessons/foo.html site/semester2/ACI/foo.html`
- After renaming a lesson file, also rename (or delete-and-copy) the counterpart in `site/` — stale old-named files in `site/` will be served by Vercel and confuse users.
- `git add site/semester2/...` must be part of the same commit as `git add semester2/.../lessons/...` — never push lesson changes without the site/ mirror.
- The `site/` tree mirrors `semester2/` exactly for HTML lesson files. Non-lesson assets (PDFs, slides) are in `course-materials/` (symlinked, gitignored) and do not go in `site/`.

**Checklist before every `git push`:**
1. `ls site/semester2/<SUBJECT>/` — confirm all new/modified HTML files are present.
2. `ls semester2/<SUBJECT>/lessons/` vs `ls site/semester2/<SUBJECT>/` — no file exists in one and not the other.
3. No stale old-named files in `site/` from a rename.

**Why:** Discovered when ACI lessons 1–3 were updated and new lessons 3, 8, exam-study-guide were created — all changes were committed to `semester2/ACI/lessons/` only. Vercel deployed nothing because `site/` was unchanged. Users saw the old 6-lesson site.

## ADR-002 — Colour Scheme: Light by Default, Dark on Dark-Mode Only

**Decision:** Every HTML element in every lesson file must use **light backgrounds and dark text by default**. Dark backgrounds are only permitted inside `@media (prefers-color-scheme:dark)` blocks.

**Rules:**
- Default (no media query): all backgrounds must be light — white, off-white, or a light tint (e.g. `#eef4ff`, `#fffbe6`, `#f8f9ff`). Never use `#1a2744`, `#0f1f3d`, `#0a2a1a`, or any dark colour outside a dark-mode block.
- Text on light backgrounds: use dark navy (`#1a2744`) or near-black (`#2c2c2c`). Never white text outside dark-mode.
- Accent colours (gold borders, green borders): allowed at any time — they work in both modes.
- Inside `@media (prefers-color-scheme:dark){…}`: dark backgrounds and light text are fine and expected.
- This applies to every component: `.try-it-sa`, `.solution`, `.steps-drill`, `.formula-box`, `.memory-box`, `.box.*`, callout divs, and any future components.

**Why:** Study content must be readable in the default (light) browser mode without requiring users to be in dark mode. Discovered when drill panels and exercise cards used dark navy as the base colour, making them heavy and hard to read in light mode.
