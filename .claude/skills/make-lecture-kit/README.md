# make-lecture-kit — turn any lecture into an easy, visual, interactive study kit

Give it a lecture (slides, notes, or just a topic) and your AI assistant
produces two things into an `output/` folder:

- **`companion.pdf`** — a real, professionally typeset study companion in plain,
  easy English, with analogies and fully-worked examples (built with LaTeX +
  figures, the way the originals were made).
- **`lecture.html`** — a complete, very detailed, very interactive lecture: the
  whole lecture rebuilt as a story-driven page where you *play* with every idea
  and watch the intuition appear.

**No API keys. You install nothing.** Your own agent session writes the source,
makes the figures, and compiles the PDF for you. It works on **any agentic coding
platform** — Claude Code, Claude Cowork, OpenAI Codex, Google Jules, Cursor, and
the like — because it is just a plain `SKILL.md` plus standard LaTeX and
standard-library Python, with nothing platform-specific. The companion PDF
compiles wherever TeX is available (most agent sandboxes have it built in).

---

## Install (pick your assistant)

You received a folder named `make-lecture-kit/` (from the zip). Put it where your
assistant looks for skills:

### Claude Code
```bash
mkdir -p ~/.claude/skills
cp -R make-lecture-kit ~/.claude/skills/
```
Or, for one project only: copy it to `<your-project>/.claude/skills/`.

### Claude Cowork
Add the `make-lecture-kit` folder to your Cowork skills (drag it into your
skills location, or use the in-app "add skill" flow). Then just ask for a lecture
kit in chat.

### OpenAI Codex
```bash
mkdir -p ~/.agents/skills
cp -R make-lecture-kit ~/.agents/skills/
```
(Codex also reads `.agents/skills/` inside a project.) Then list skills with
`/skills`, or simply tell Codex: *"Use the make-lecture-kit skill to turn the
attached lecture into a companion study PDF and an interactive lecture page."*

### Google Jules / Cursor / any other agent
The kit is platform-neutral. Put the `make-lecture-kit/` folder wherever your
agent reads skills (or just attach/point it at the folder in chat) and ask it to
*"use make-lecture-kit on the attached lecture."* It reads `SKILL.md` and follows
the same workflow everywhere — no proprietary tools, no API keys.

### Or don't install at all
You can also just drop the `make-lecture-kit` folder into a chat with Claude or
Codex and say: *"Use this skill to turn my lecture into a companion PDF and an
interactive lecture."*

---

## Use

Attach your lecture file (PDF/PPTX) if you have one — results are much better —
then tell your assistant any of these (more in `references/prompts.md`):

- "Use make-lecture-kit on this lecture PDF."
- "Make a study PDF and a complete interactive lecture for **eigenvectors**."
- "Explain **backpropagation** simply, with worked examples and an interactive lecture."

You'll get a new folder `output/<topic>/` containing `companion.pdf` (the typeset
study companion) and `lecture.html` (the complete interactive lecture), alongside
the `companion.tex` source and the `figures/` used to build it.

Behind the scenes, your assistant reads `SKILL.md` and follows its workflow
(read the style references, expand every slide, work every example in full,
build the page and the PDF, then run the quality gates). You don't do any of
that — just give it a lecture.

> **About the PDF:** it compiles instantly in Claude Cowork and Codex sandboxes
> (TeX Live is built in). On a bare machine without TeX, the assistant will say
> so plainly, leave the ready-to-compile `companion.tex` + figures, and tell you
> the one-line TinyTeX install to finish the job.

---

## What's inside

```
make-lecture-kit/
├─ START_HERE.md                read this first (1-minute setup)
├─ README.md                    this file
├─ SKILL.md                     the instructions your AI follows
├─ templates/
│  ├─ companion.tex             LaTeX study-companion template (→ PDF)
│  └─ lecture.html              complete interactive lecture template
├─ references/
│  ├─ quality_rubric.md         the quality bar + ship checklist (both)
│  ├─ companion_style.md        how to expand slides into the companion
│  ├─ lecture_style.md          how to build the complete interactive lecture
│  ├─ intuition_playbook.md     analogies, mental models, ML/AI links
│  └─ prompts.md                copy-paste prompts for students
├─ scripts/
│  ├─ figstyle.py               matplotlib house style + reusable plotters
│  ├─ build_pdf.py              run figures + compile companion.tex → PDF
│  └─ lint.py                   lecture HTML quality gate (readability, no-overflow, keyless)
├─ examples/
│  ├─ sample_companion.tex      a finished example to show the quality bar
│  └─ figures/
│     └─ example_normal_curve.py  copy-adaptable house-style figure script
└─ output/                      your generated kits land here (the skill
                                creates one subfolder per lecture — don't
                                edit this folder by hand)
```

The companion uses LaTeX + matplotlib (already present in Cowork/Codex
sandboxes); the helper scripts are standard-library Python. Nothing phones home,
nothing needs an API key.

---

## The promise

Built around five rules: **easy words**, **relatable analogies**,
**step-by-step math intuition**, **generous fully-solved examples**, and
**interactions that uncover the intuition** — with a hard no-clutter,
no-overflow guarantee so text never runs off the page or screen.
