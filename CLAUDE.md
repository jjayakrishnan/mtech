# mtech — MTech AI/ML (BITS Pilani)

Root workspace for all MTech coursework. Each semester lives in its own subfolder.

## Structure

```
mtech/
├── semester2/          current semester
│   ├── ACl/            Advanced Computing for AI (ACI)
│   ├── DRL - Deep Reinforcement learning/
│   ├── NLP-Saurabh/    Natural Language Processing
│   ├── SEML/           Software Engineering for Machine Learning
│   └── make-lecture-kit/   study-kit skill (source lives here)
└── assignments/        cross-semester assignment work
    ├── ACI/
    ├── DRL/
    └── NLP/
```

## Skills

All skills are registered at `.claude/skills/` and available in every subfolder.

### make-lecture-kit
Turns any lecture (PDF, PPTX, or topic name) into:
- `output/<slug>/companion.pdf` — typeset study companion (LaTeX + matplotlib)
- `output/<slug>/lecture.html` — complete interactive lecture page

Trigger: `/make-lecture-kit` or *"use make-lecture-kit on this lecture"*.  
Source lives at `semester2/make-lecture-kit/`; outputs go into `output/` inside that folder.

### Other skills (from mattpocock/skills)
`/diagnose`, `/prototype`, `/tdd`, `/grill-me`, `/handoff`, `/teach`, `/write-a-skill`,
`/design-an-interface`, `/qa`, `/review`, `/writing-beats`, `/writing-fragments`, `/writing-shape`, and more.

## Conventions

- Lecture slides are PDFs or PPTX files inside each course folder.
- Lab/demo code is in zip archives; unzip before reading.
- When explaining lecture content: plain English first, analogy before math, fully-worked examples — same standard the make-lecture-kit skill enforces.
