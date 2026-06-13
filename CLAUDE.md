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
