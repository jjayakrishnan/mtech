# Start here

## What this is

Your teacher made this kit for you. Give it any lecture — slides, notes, or
just a topic — and your AI assistant turns it into a beautiful study PDF
(`companion.pdf`) and a complete interactive lecture page (`lecture.html`).
No accounts, no API keys, nothing to configure.

## Set it up in 1 minute

Pick the assistant you use and copy-paste:

**Claude Code**
```bash
mkdir -p ~/.claude/skills
cp -R make-lecture-kit ~/.claude/skills/
```

**OpenAI Codex**
```bash
mkdir -p ~/.agents/skills
cp -R make-lecture-kit ~/.agents/skills/
```

**Claude Cowork**
Add the `make-lecture-kit` folder as a skill (use the in-app "add skill"
flow) — or simply drag the folder into your chat.

**Using Google Jules, Cursor, or another agent?**
The kit is platform-neutral — put the folder wherever that agent reads skills,
or just point it at the folder, and ask the same way.

**Don't want to install anything?**
Just drop the whole `make-lecture-kit` folder into a chat with Claude, Codex,
Jules, or any agent and ask away.

## Use it

Attach your lecture file (PDF or PPTX) if you have one — results are much
better — then say something like:

- "Use make-lecture-kit on the attached lecture slides."
- "Make a study PDF and a complete interactive lecture for eigenvectors."
- "Explain backpropagation simply, with fully worked examples and an
  interactive lecture."

More ready-made prompts: `references/prompts.md`.

## What you get

Everything lands in a new folder, `output/<your-topic>/`:

- **`lecture.html`** — double-click it; it opens in your browser. Move the
  sliders, step through the math, toggle things on and off. That's the point.
- **`companion.pdf`** — your study document: plain English, analogies before
  the math, every example worked out in full. Print it, scribble on it.

If the PDF didn't compile on your machine (no LaTeX installed), the assistant
will say so plainly and tell you exactly what to do next — your
`companion.tex` source and figures are still there, ready to compile.

## If something goes wrong

- Ask: "Run `scripts/lint.py` on my lecture.html and show me what it says."
- Ask: "lint reported FAILs — fix every FAIL and re-run until it passes."
- Weak or generic result? Re-ask with the actual lecture file attached.

Happy studying.
