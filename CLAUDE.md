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

## ADR-005 — Theme System: All Colours from `site/theme.css`

**Decision:** Every HTML file in this portal must link to `site/theme.css` and use only CSS custom properties (e.g. `var(--navy)`, `var(--tint-success)`) for colours — never raw hex values in inline styles or lesson-specific `:root` blocks.

**Rules:**
- `<link rel="stylesheet" href="[depth]/theme.css">` must be the first child of `<head>`
- No inline `:root {}` colour tokens — only layout tokens (`--sidebar`, `--r`, `--mono`) are permitted in lesson files
- Callout box backgrounds: always `var(--tint-success/formula/info/danger/warning/try)` — never `#f0fff4`, `#fffbe6`, `#eef4ff`, etc.
- Sidebar background: always `var(--sidebar-bg)` — never `var(--navy)` or any hardcoded dark colour
- Dark mode toggle: every lesson must have the standard toggle button + script using localStorage key `'theme'` (not `'aci-theme'` or subject-prefixed keys)
- DRL toggle init: wrap button label update in `DOMContentLoaded` so the element exists when the script runs

**Full reference:** [`docs/theming-guide.md`](docs/theming-guide.md) — complete colour table, page template skeleton, per-subject notes, forbidden patterns, and how to run the audit tool.

**Why:** Inconsistent colours and dark-mode breakage across ACI/DRL/NLP/SEML required a bulk fix. Centralising in `theme.css` means any colour change is one-line edit; the audit script (`node scripts/theme-audit.js`) verifies all 46 pages.

## ADR-004 — Tables: Always Wrap for Mobile Scroll

**Decision:** Every `<table>` in any HTML file produced in this project must be wrapped in `<div class="table-scroll">`.

**Rules:**
- CSS: `.table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0.6rem 0; }`
- The wrapper replaces any inline `overflow-x:auto` div previously used around individual tables.
- Applies to all table types: `.trace-table`, `.peas-table`, `.grid-table`, `.solution table`, comparison tables, and any future table.
- The `.table-scroll` CSS rule must be present in the `<style>` block of every HTML file that contains a table.
- Exception: `<table>` elements used as layout containers (not data tables) do not need the wrapper.

**Why:** Wide trace tables (GBFS, A*, BFS step-by-step) overflow on mobile screens (~375px) and are clipped — users cannot scroll horizontally to see all columns. Discovered when inspecting the ACI exercise bank on mobile.

## ADR-006 — Lesson Color-Coding Convention

**Decision:** Every ACI lesson page uses a fixed semantic color system for callout blocks. Colors are assigned by the *purpose* of the block — never arbitrarily.

| Block class | Color signal | Use for |
|---|---|---|
| `.card` (default) | Gold left border | Key concept, definition, "golden rule" |
| `.card.green` | Green left border | Worked example, correct solution |
| `.card.red` | Accent/red left border | Common mistake, exam trap, "never do this" |
| `.memorise` | Gold thick border + `var(--tint-formula)` bg | Must-memorize formula or fact (once per h2 section) |
| `.collapsible` | Dashed green border | Self-check exercise with hidden answer |
| `.try-it-sa` | Dashed green border | Exam-style practice question |
| `.diagram` | Monospace + `var(--code-bg)` | Tree diagrams, ASCII graphs, pseudocode |
| `.trace-table .expanded` | `var(--tint-success)` row bg | Currently expanding node in algorithm traces |

**Rules:**
- `.card` (gold) for every concept introduced for the first time
- `.card.green` for every worked example / solution block
- `.card.red` for every "common mistake" or "exam trap" callout
- `.memorise` once per major section (h2 level) to summarize the take-away formula
- `.trace-table .expanded` on every node currently being expanded in search/algorithm traces
- Never use raw background hex — always `var(--tint-*)` or the above class patterns
- Applies to all new lesson files under any subject (ACI, DRL, NLP, SEML)

**EC3 sub-portal depth:** Files in `semester2/ACI/lessons/EC3/` use `../../../theme.css` (one extra `../` compared to parent ACI lessons). The `<base href="/semester2/ACI/EC3/">` tag is required in every EC3 lesson. Links back to parent ACI lessons use `../0001-agents-peas-environments.html` etc.

**Why:** Inconsistent callout block colors across lessons made it hard to scan at a glance. A gold/green/red system matches traffic-light intuition: gold = information, green = correct, red = danger.

## ADR-007 — PDF Study Guides: No Color in Body Content

**Decision:** All LaTeX-generated PDFs (exam guides, companion notes, study guides) must use **black, white, and grayscale only** in the document body. Color is reserved exclusively for watermarks, headers, and footers.

**Rules:**
- `tcolorbox` backgrounds: `colback=white` or `colback=gray!8` — never `lightblue`, `lightgreen`, `lightyellow`, etc.
- `tcolorbox` frames: `colframe=black` or `colframe=gray!60` — never `navy`, `green!70!black`, `red!70!black`, etc.
- Section headings: `\color{black}` — never `\color{navy}` or any other hue
- Table row shading: `\rowcolor{gray!15}` at most — never `\rowcolor{navy}` or colored rows
- Hyperlinks: `colorlinks=false` or `linkcolor=black,urlcolor=black`
- Headers/footers: may use a single subtle gray rule — text must be black
- Watermarks: color is applied by `bits_watermark.py` after LaTeX compile — do not pre-color for it

**Why:** Colored callout boxes cause visual confusion and look poor in black-and-white printing. The BITS watermark overlay already provides color identity. Body content must be clean, legible, and print-friendly.

## ADR-008 — PDF Handouts: No LaTeX Headers or Footers

**Decision:** All LaTeX-generated handouts (exam handouts, study guides, companion docs) must have **no `\usepackage{fancyhdr}` headers or footers**. The branding strip (college name, "Innovate · Achieve · Lead") is added automatically by `bits_watermark.py` on slide-format pages. Handout pages are plain — just body content plus the watermark overlay.

**Rules:**
- Do **not** load `fancyhdr`, `pagestyle`, or any `\lhead`/`\rhead`/`\cfoot` commands.
- Do **not** hardcode "Innovate · Achieve · Lead" or any institutional tagline in LaTeX source.
- A single `\hrule` + `{\footnotesize …}` line at the very bottom of the document body (for attribution / subject + session reference) is permitted — it is not a header/footer.
- Slide-format pages (2-in-1 landscape outputs) have the BITS header/footer baked in by the watermark script — no duplication needed.
- Headers/footers may only be added in a later stage when explicitly producing slide-format handouts (not exam handouts).
- **`bits_watermark.py` flag for handouts:** always use `--watermark-only` (NOT `--one-per-page`).
  `--watermark-only` sets `chrome=False` and skips tricolor bars, Innovate/Achieve/Lead ribbon,
  footer text, and page number badge — leaving only the diagonal corner text strips and BITS logo.
  `--one-per-page` keeps the full chrome (ribbon + bars + footer) and is for slide-format pages only.

**Why:** The "Innovate · Achieve · Lead" strip on the companion handout PDFs is added by the watermark overlay for slide pages only. Duplicating it in LaTeX body or plain handouts clutters the page. All exam handouts use `--watermark-only`.
