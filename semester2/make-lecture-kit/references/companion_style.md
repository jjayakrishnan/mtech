# Companion Style — the authoring guide

Read this **before** writing a single line of a companion. A companion is the
plain-English book that walks beside a terse lecture deck. The slides give the
formulas; **this reader gives the why.** It expands every slide concept into the
full teaching treatment and works **every** slide example out in full, step by
step, in easy English.

The look is fixed and non-negotiable: a navy title banner, a `fancyhdr` running
header, numbered ruled section headings, and **five** coloured callout boxes
with pill tabs. The compilable specimen at `examples/sample_companion.tex` is the
quality bar — when in doubt, match it. The figure helper is
`scripts/figstyle.py`. The full template preamble lives in
`templates/companion.tex`.

---

## 0. The non-negotiable visual contract

| Element | Spec |
|---|---|
| Header (every page) | left `ISM Companion`, right `Session N · <Lecture Title>`, thin rule below |
| Footer | centred page number |
| Title banner (page 1) | full-width dark-navy `tcolorbox` (`#21355E`), white text: tracked uppercase label → very large bold title → light subtitle → thin white rule → small meta line |
| Intro | one paragraph **"How to use this companion."** explaining the colour code |
| Sections | sans, bold, navy, **numbered** (`1  The big idea: …`), horizontal rule beneath |
| Body | justified serif (lmodern), `parskip` spacing, `microtype`, math via `amsmath`, tables via `booktabs` |
| Figures | full-textwidth matplotlib PNGs, centred, **bold title baked into the plot** |

### The FIVE callout boxes — exact taxonomy (quote it, don't improvise)

| Box | Pill label | Glyph | Frame hex | Tint | Use it for |
|---|---|---|---|---|---|
| Intuition | `The intuition` | ☞ `\ding{43}` | `#2C5AA0` blue | `blue!4` | the idea in plain words, before any math |
| Everyday | `Everyday picture` | ★ `\ding{72}` | `#8A5A1E` amber | `orange!7` | the real-life analogy for a tricky idea |
| Worked | `Worked example: <caption>` | ✎ `\ding{46}` | `#2E7D52` green | `green!5` | a problem solved with real numbers, every step |
| Watch out | `Watch out` | ✗ `\ding{55}` | `#B23A48` red | `red!4` | the common mistake / trap |
| Key takeaway | `Key takeaway` | ✓ `\ding{52}` | `#6A4C93` purple | `violet!6` | the one line to remember |

Box style (from the template): `enhanced, breakable`, rounded corners,
`boxrule=0.6pt`, **pill tab** via `attach boxed title to top
left={xshift=6mm,yshift=-3mm}`, `boxed title style={colback=<frame>, rounded
corners}`, `coltitle=white`, `fonttitle=\bfseries\sffamily\small`. Never change
the colours, labels, or glyphs — they are the reader's mental index.

---

## 1. Ingest the slide deck (do this first, in full)

You cannot expand what you have not catalogued. Before writing:

1. **Read the source.** Open the `.pdf` or `.pptx`. If it is `.pptx`, use the
   `pptx` skill to extract text and notes; if `.pdf`, use the `pdf` skill. Read
   **every** slide, including the agenda and any "example" one-liners.
2. **List every concept.** One line each, in slide order. A concept is anything
   that earns a definition, a formula, or a named idea. This becomes your
   section list.
3. **List every slide example.** Each terse "e.g. λ=3, find P(X=2)" is a
   **promise** you must keep: it gets a full `worked` box with every step. Mark
   which concept each example belongs to.
4. **List every formula and symbol.** You will name every symbol on first use,
   so collect them now.
5. **Write the spine.** For each concept, plan the order in §2. Confirm the
   count: *number of `worked` boxes ≥ number of slide examples.* If a slide has
   three examples, the companion has at least three worked boxes for it.

Output of this step is a checklist. Do not start prose until the checklist is
complete. A dropped slide example is a failed companion.

---

## 2. Map each concept onto the teaching spine

Every concept follows the same gentle arc. Not every concept needs every box,
but the order never changes:

1. **Open in plain words** — one or two body sentences saying what this is and
   why we care. No jargon yet.
2. **The intuition box** (blue ☞) — the idea stated simply, the mental model.
3. **The everyday picture box** (amber ★) — the analogy. **Mandatory for any
   tricky idea.** Put it *before* the math, so the reader meets the concept in
   the world before meeting it in symbols.
4. **Formalize** — introduce the formula in body text. Name **every** symbol
   the first time it appears (see §3). Build it up, never drop it whole.
5. **The worked example box(es)** (green ✎) — solve the slide example(s) in
   full (see §4). One box per example; keep each box coherent.
6. **The watch-out box** (red ✗) — the trap a beginner falls into here.
7. **The ML/AI connection** (see §7) — a short body paragraph, `\textbf{Where
   this shows up in ML.}`, on how the idea appears in machine learning.
8. **The key-takeaway box** (purple ✓) — the single line to remember. Always
   last for the concept.

**When to use which box** (decide fast):
- Explaining *what something means*? → **intuition** (blue).
- Reaching for "it's like…"? → **everyday** (amber).
- Touching real numbers? → **worked** (green).
- About to say "be careful" / "a common error is"? → **watch out** (red).
- Compressing to one sentence? → **key takeaway** (purple).

Do not stack two boxes of the same colour back to back. Do not put math
derivations inside the intuition or everyday boxes — those stay word-only.

---

## 3. The EASY-LANGUAGE mandate

Write for a smart beginner. **Simple common words. Short sentences (under ~20
words). Define every term on first use.** Prefer "average" to "expectation" on
first contact, then introduce the technical word in parentheses.

Rewrite every dense slide sentence. Before → after:

- **Before:** "X ~ Poisson(λ) models the number of arrivals in a fixed interval
  under independence and stationarity assumptions."
  **After:** "A Poisson count answers one question: how many rare events happen
  in a fixed window? It needs just one number, λ, the average count."

- **Before:** "The MLE is obtained by setting the score function to zero."
  **After:** "To find the best-fit value, we find where the slope of the
  likelihood is zero. That slope is called the *score*."

- **Before:** "The estimator is unbiased and consistent."
  **After:** "On average this estimate hits the truth (it is *unbiased*), and it
  gets better as we collect more data (it is *consistent*)."

Rules of thumb: one idea per sentence; active voice; spell out the first use of
every Greek letter ("λ, the Greek letter lambda"); replace "thus/hence/whence"
with "so"; never write "clearly" or "obviously" — if it were obvious the
companion would not exist.

---

## 4. Write a FULLY worked example

This is the heart of the companion. **Show every algebraic step with real
numbers.** Never write "it can be shown that", "after simplification", or "the
details are left to the reader". If you skipped a step, you failed.

Put it in a `worked` box with a short caption in the pill label, and a numbered
`enumerate` list (the template styles the labels as "Step 1.", "Step 2.", …).
Skeleton:

```latex
\begin{worked}{<short caption, e.g. help-desk calls in one hour>}
<One plain sentence restating the problem and the target.>
\begin{enumerate}[label=\textbf{Step \arabic*.}]
  \item \textbf{Write down what we know.} State each given value: lambda = 3, k = 2.
  \item \textbf{Plug into the formula.} Substitute the numbers literally:
        \[ P(X=2) = \frac{3^{2}\,e^{-3}}{2!}. \]
  \item \textbf{Work out each piece.} 3^2 = 9; 2! = 2; e^{-3} = 0.049787.
  \item \textbf{Combine.}
        \[ P(X=2) = \frac{9 \times 0.049787}{2} = 0.224042. \]
        So about \textbf{22.4\%}.
  \item \textbf{Sense-check.} Is it between 0 and 1? Does it sit near the peak? Yes.
\end{enumerate}
<One sentence naming any trick used (e.g. the "1 - P(0)" shortcut).>
\end{worked}
```

Discipline for worked examples:
- **Every** intermediate number appears. Carry 4–6 significant figures, then
  round the final answer and **bold** it.
- One step does one thing. If a step has two computations, split it.
- End with a **sense-check**: range, units, "is it near the mean?", a sanity
  bound. This teaches judgement, not just arithmetic.
- Keep a single worked example **coherent** — it may break across pages
  (`breakable`), but do not interleave unrelated prose inside it.

---

## 5. Figures with `scripts/figstyle.py`

Figures are local matplotlib PNGs — **keyless, offline, no network at author
time.** The house style lives in `scripts/figstyle.py`; you write one tiny
`figures/<lecture>.py` per lecture and call `housefig`.

Per-lecture figure script:

```python
# figures/poisson.py
import numpy as np
from math import exp, factorial
from scripts.figstyle import housefig, PALETTE, savefig

fig, ax = housefig("Poisson(lambda=3): bars peak near the mean")
k = np.arange(0, 11)
p = [3**i * exp(-3) / factorial(i) for i in k]
ax.bar(k, p, color=PALETTE["green"], width=0.7)
ax.set_xlabel("k (number of events)")
ax.set_ylabel("P(X = k)")
savefig(fig, "figures/poisson.png")
```

`housefig(title)` returns `(fig, ax)` with the **bold title baked in** (left
aligned, navy), thin spines, the muted house palette, and a width that fills the
text column. Run the script once at author time to produce the PNG; commit the
PNG. The figure colours match the callout taxonomy: `PALETTE["green"]` for a
worked plot, `PALETTE["blue"]` for an intuition plot, etc.

In the `.tex`, include it at the text width via the template's helper
(`\housefig{path}{baked-in title}` expands to a centred, full-width
`\includegraphics[width=\linewidth]{...}`). If you have no toolchain, a TikZ
mini-figure (see the specimen) is an acceptable inline substitute for a simple
bar/curve — but real data plots use matplotlib PNGs.

Plot style: muted palette, thin spines (top/right removed), readable axis
labels, a legend only when more than one series. One clear message per figure.

---

## 6. LaTeX anti-overflow discipline

**Never ship an Overfull `\hbox`.** The reader prints this; overflow is visible
and ugly. Defences:

- **Long math:** never one overlong line. Break with `align` / `split` /
  `multline`. Each `&=` continuation wraps at the margin:
  ```latex
  \begin{aligned}
    P(X \ge 1) &= 1 - P(X = 0) \\
               &= 1 - 0.049787 = 0.950213.
  \end{aligned}
  ```
- **Wide tables:** wrap in `\resizebox{\linewidth}{!}{...}` or
  `\begin{adjustbox}{max width=\linewidth}...\end{adjustbox}`. Build the table
  with `booktabs` (`\toprule \midrule \bottomrule`), no vertical rules.
- **Long URLs / tokens:** `\url{...}` (xurl lets them break anywhere); add
  `\allowbreak` inside long inline identifiers in prose.
- **Figures:** always `width=\linewidth` so an image never exceeds the text.
- **Callouts:** all five are `breakable`, so they flow onto the next page
  cleanly — but keep one worked example **coherent** (§4); do not let an
  example split mid-derivation if you can group it.
- Compile **twice** (header / `hyperref` / refs) and scan the log for
  `Overfull`. Fix every one before declaring done.

---

## 7. The ML/AI-connection habit

**Every concept gets one.** After the math, add a short body paragraph led by
`\textbf{Where this shows up in ML.}` connecting the idea to machine learning or
AI — a model, a loss, a layer, a trick. Keep it concrete and one paragraph.

Examples of the move:
- Poisson → Poisson regression for count targets (`λ = e^{βᵀx}`), the Poisson
  NLL loss, photon-noise image models.
- Gaussian → the squared-error loss is the Gaussian NLL; weight init; the
  reparameterisation trick in VAEs.
- Bias/variance → why regularisation, dropout, and ensembles work.

If a concept has no honest ML hook, say so in one line rather than inventing a
forced one — but this is rare; most statistics concepts have a real connection.

---

## 8. Final self-review checklist (mirror the rubric)

Before you ship, confirm **every** line:

- [ ] **Banner** present on page 1: navy `#21355E`, tracked uppercase label,
      huge bold title, light subtitle, white rule, meta line (`Session N (dates)
      · Read alongside the lecture slides · Every slide example worked out in
      full`).
- [ ] **Header** every page: `ISM Companion` left, `Session N · <Title>` right,
      rule below; **footer** centred page number.
- [ ] **"How to use this companion."** intro paragraph explains all five colours.
- [ ] **Sections** numbered, sans, navy, ruled (`1  The big idea: …`).
- [ ] **All five callout types** used at least once, with the **exact** labels,
      glyphs, frames (`#2C5AA0 / #8A5A1E / #2E7D52 / #B23A48 / #6A4C93`) and
      tints (`blue!4 / orange!7 / green!5 / red!4 / violet!6`).
- [ ] **Every slide concept** expanded; **every slide example** worked in full,
      every step, real numbers, no "it can be shown that".
- [ ] **Easy language:** short sentences (<~20 words), every term defined on
      first use, every Greek letter named.
- [ ] **Every tricky idea** has an everyday-picture analogy **before** the math.
- [ ] **Every formula** built up with **every symbol named**.
- [ ] **Each concept** has an ML/AI connection.
- [ ] **No Overfull `\hbox`** in the log; wide math in `align/split`, wide tables
      in `adjustbox`/`booktabs`, figures at `width=\linewidth`.
- [ ] **Figures** are house-styled via `\housefig{path}{caption}`, full-width, bold baked-in title.
- [ ] **Worked examples coherent** — none split mid-derivation awkwardly.
- [ ] Compiles to a **real PDF**, keyless, twice through `pdflatex`.

If any box is unchecked, the companion is not done. Boring beats brilliant: a
deterministic, complete, plain-English reader that keeps every promise on the
slides beats a clever, partial one.
