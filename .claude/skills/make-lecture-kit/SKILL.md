---
name: make-lecture-kit
description: >-
  Turn ANY lecture — a slide deck (PDF/PPTX), notes, or just a topic — into two
  beautiful, beginner-friendly study artifacts written to an output/ folder: a
  real, professionally typeset companion PDF (LaTeX: navy title banner, colour-
  coded callout boxes, matplotlib figures — "every slide example worked out in
  full"), and a complete, very detailed, very interactive HTML lecture — the
  whole lecture rebuilt as an interactive experience. Plain easy English,
  relatable analogies, math intuition built step by step, generous fully-solved
  examples, and interactions that uncover the intuition. No API keys. The student
  installs nothing — your Claude/Codex session writes the .tex, generates the
  figures, compiles the PDF, and builds the lecture page. Trigger on: "turn this
  lecture/these slides into a companion PDF and an interactive lecture", "make a
  study PDF for <topic>", "explain <hard topic> simply with worked examples",
  "build a complete interactive lecture for <topic>", "make-lecture-kit <file-or-topic>".
---

# make-lecture-kit (student edition)

Give this skill a lecture and it produces, into `output/<session>/`:

1. **`companion.pdf`** — a real, professionally typeset study companion (built
   from `companion.tex` + matplotlib figures with LaTeX). Colour-coded callout
   boxes, clean math, worked examples in full. This is the primary deliverable.
2. **`lecture.html`** — a complete, very detailed, very interactive lecture: the
   *entire* lecture rebuilt as a story-driven web page, every concept covered in
   depth, with working interactions that let the learner *play* with each idea
   and watch the intuition appear.

**The student installs nothing and manages no toolchain.** You — the host agent
(Claude Code, Claude Cowork, or OpenAI Codex) — author everything and compile the
PDF yourself. In Cowork/Codex sandboxes TeX Live + matplotlib are already present,
so the PDF compiles directly. No API keys, no secrets, ever.

---

## The five non-negotiable rules (this is what makes it good)

Read `references/quality_rubric.md` fully first; self-score against it before you finish.

1. **Easy language.** Simple, common words. Short sentences (aim under ~20 words). Define every new term the first time. Write for a smart person meeting this topic for the *first* time. No academic fog.
2. **Analogies that stick.** Every tricky idea gets a relatable, real-life analogy in plain language *before* the math (the "Everyday picture" box).
3. **Math intuition, simply detailed.** Build every formula up step by step — nothing skipped, every symbol named. Explain *why*, not just *what*.
4. **Fully solved examples, generously.** Wherever an example helps a concept land, include one (often more than one). Work **every slide example out in full**, every step, real numbers. Never "it can be shown that".
5. **Interaction uncovers intuition (visualizer).** Each control must *reveal* something — move a slider and watch the idea change, step through and see the derivation build, toggle and expose the picture. Not decoration.

Plus the **no-clutter / no-overflow contract**: nothing overlaps, no text runs off the page (no Overfull `\hbox`; wrap long math in `align`/`split`; wide tables via `adjustbox`/`booktabs`), worked examples stay coherent, the HTML is fully responsive.

---

## Workflow

### 1. Read the references first
- `references/quality_rubric.md` — the bar + the ship checklist (both deliverables)
- `references/companion_style.md` — how to expand slides into the LaTeX companion
- `references/lecture_style.md` — how to build the complete interactive lecture
- `references/intuition_playbook.md` — analogies, mental models, ML/AI connections

### 2. Read the input lecture
The input is usually a **slide deck** (PDF/PPTX) — but may be notes or just a topic. Read it with your own document ability (or a PDF/PPTX skill). List **every concept** to teach and **every slide example** to work out in full, in a sensible order (simple → hard, prerequisites first).

### 3. Pick a slug and make the output folder
Choose a short kebab slug (e.g. `session6-distributions`, `eigenvectors`) and create `output/<slug>/` and `output/<slug>/figures/`.

### 4. Author the companion → `output/<slug>/companion.pdf`
1. Copy `templates/companion.tex` to `output/<slug>/companion.tex`. Fill the banner/header placeholders (`{{COURSE_SHORT}}`, `{{SESSION}}`, `{{LECTURE_TITLE}}`).
2. For **each** concept, walk the full teaching spine in plain words, using the colour-coded callout boxes:
   > **Hook** (real-life) → **`\begin{intuition}`** (analogy + mental model) → **the math, step by step** → **`\begin{worked}` fully-solved example(s)** with real numbers → **`\begin{everyday}`** real-world picture → ML/AI connection → a **figure** (visual intuition) → **`\begin{watchout}`** pitfalls → **`\begin{keytake}`** recap.
   Work out **every example from the slides** in full.
3. Make figures: write `output/<slug>/figures/*.py` that `import figstyle` (from `scripts/`), call `use_house_style()`, and save PNGs; reference them with `\housefig{figures/xyz.png}{caption}`.
4. Compile to PDF (run from the skill root, so figure scripts can import
   `figstyle` from `scripts/`):
   ```bash
   python3 scripts/build_pdf.py output/<slug>/companion.tex
   ```
   `build_pdf.py` runs the figure scripts, compiles with `latexmk`/`pdflatex`, and writes `output/<slug>/companion.pdf`. It also reports any Overfull-box / reference warnings so you can fix overflow before shipping. If the environment has no TeX engine, it prints clear guidance (Cowork/Codex have TeX Live; otherwise install TinyTeX) and leaves the `.tex` + figures ready — it never fails silently.

### 5. Author the complete lecture → `output/<slug>/lecture.html`
Start from `templates/lecture.html` (a working 3-chapter demo — its chapters set the depth bar; replace them with the real lecture's chapters). Rebuild the **entire** lecture as a connected **story** — a grouped sidebar TOC, one chapter per concept, cover **everything**, drop nothing. Each concept gets the full detailed treatment *and* a **bespoke hand-drawn `<canvas>` lab** with 2+ working controls that *uncover* the intuition (slider→watch the idea change, step→build it up, toggle→reveal the structure) — use the template's `makeSlider`/`setupCanvas` helpers; don't reach for chart libraries. All math via MathJax (the only external dependency). Dark, clean, responsive, nothing overlapping. Then gate it:
```bash
python3 scripts/lint.py output/<slug>/lecture.html
```
`lint.py` fails on template-hygiene leaks (broken comments, leftover `{{placeholders}}`), possible overflow, long unreadable sentences, blocked math, missing interactivity, any non-CDN dependency, or leaked secrets. Fix every FAIL and re-run until it passes. Also replace the `<title>` tag and every demo-chapter remnant — the shipped page must be entirely about the student's lecture.

### 6. Finish honestly
Tell the learner what landed in `output/<slug>/` and which checks passed. If `build_pdf.py` couldn't compile here (no TeX engine in this environment), say so plainly and give the exact next step — **don't claim a `companion.pdf` exists if it doesn't.** Then self-score against `references/quality_rubric.md`.

---

## Works everywhere
Plain `SKILL.md`, standard LaTeX, matplotlib, and standard-library Python — runs unchanged in **Claude Code**, **Claude Cowork**, and **OpenAI Codex**. See `README.md` for the one-line install in each. The companion PDF compiles wherever TeX Live exists (the Cowork/Codex sandboxes); the lecture page needs only a browser.
