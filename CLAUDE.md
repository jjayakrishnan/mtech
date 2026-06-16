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
