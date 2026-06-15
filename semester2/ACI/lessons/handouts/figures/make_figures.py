#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure scripts for Session 1: Agents, PEAS & Task Environments.
Produces four PNGs next to this script:
  fig_agent_loop.png      — the agent-environment loop (flow diagram)
  fig_peas_taxi.png       — PEAS for the automated taxi (bar/table figure)
  fig_ai_perspectives.png — the 2x2 AI perspectives table as a visual
  fig_vacuum_table.png    — vacuum percept-action summary
  fig_ai_timeline.png     — AI history timeline (bars)
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Find the kit's scripts/ folder so we can import figstyle.
# Walk up from HERE looking for the make-lecture-kit/scripts directory.
_found = False
_search = HERE
for _ in range(10):
    _candidate = os.path.join(_search, ".claude", "skills", "make-lecture-kit", "scripts")
    if os.path.isdir(_candidate):
        sys.path.insert(0, _candidate)
        _found = True
        break
    _search = os.path.dirname(_search)
    if _search == os.path.dirname(_search):  # filesystem root
        break

if not _found:
    # Absolute fallback: hard-coded relative path from the known repo root
    _kit = os.path.normpath(os.path.join(HERE, "../../../../../.claude/skills/make-lecture-kit/scripts"))
    if os.path.isdir(_kit):
        sys.path.insert(0, _kit)

import figstyle as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------------------------------------------------------------------------
# 1. Agent-environment loop flow diagram
# ---------------------------------------------------------------------------
F.flow(
    ["Environment", "Percepts\n(sensors)", "Agent\ndecision", "Actions\n(actuators)"],
    "The agent-environment loop: perceive, decide, act, repeat",
    direction="lr",
    out=os.path.join(HERE, "fig_agent_loop.png"),
)

# ---------------------------------------------------------------------------
# 2. PEAS for the automated taxi — a labelled bar-style summary
# ---------------------------------------------------------------------------
F.use_house_style()
fig, ax = plt.subplots(figsize=(7.0, 3.2))
ax.axis("off")

rows = [
    ("P  Performance", "Safe + fast + legal + comfortable trip; maximise profit"),
    ("E  Environment", "Roads, traffic, pedestrians, weather, signals, customers"),
    ("A  Actuators",   "Steering wheel, accelerator, brake, horn, turn signals"),
    ("S  Sensors",     "Cameras, LIDAR, GPS, speedometer, odometer, keyboard"),
]

colours = [F.PALETTE["blue"], F.PALETTE["green"],
           F.PALETTE["amber"], F.PALETTE["purple"]]

y = 0.88
for (label, detail), col in zip(rows, colours):
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.01, y - 0.14), 0.20, 0.16,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        fc=col, ec="none", transform=ax.transAxes))
    ax.text(0.11, y - 0.06, label, ha="center", va="center",
            transform=ax.transAxes, color="white",
            fontsize=9.5, fontweight="bold")
    ax.text(0.24, y - 0.06, detail, ha="left", va="center",
            transform=ax.transAxes, color=F.PALETTE["ink"],
            fontsize=9.5)
    y -= 0.22

ax.set_title("PEAS for the automated taxi driver",
             color=F.PALETTE["ink"], fontweight="bold", fontsize=12, pad=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_peas_taxi.png"))
plt.close(fig)

# ---------------------------------------------------------------------------
# 3. Four perspectives on AI — 2x2 grid visual
# ---------------------------------------------------------------------------
F.use_house_style()
fig, ax = plt.subplots(figsize=(7.0, 3.2))
ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.axis("off")

cells = [
    # (col, row, label, colour)
    (0, 1, "(1) Thinking\nHumanly\n(Cognitive modelling)",   F.PALETTE["muted"]),
    (1, 1, "(3) Thinking\nRationally\n(Laws of thought)",    F.PALETTE["muted"]),
    (0, 0, "(2) Acting\nHumanly\n(Turing Test)",             F.PALETTE["muted"]),
    (1, 0, "(4) Acting\nRationally\n(Rational agent) ★",     F.PALETTE["blue"]),
]

for col, row, txt, colour in cells:
    x0, y0 = col, row
    ax.add_patch(mpatches.FancyBboxPatch(
        (x0 + 0.04, y0 + 0.04), 0.92, 0.92,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        fc=colour + "22", ec=colour, lw=2.0))
    ax.text(x0 + 0.5, y0 + 0.5, txt, ha="center", va="center",
            fontsize=9.5, color=F.PALETTE["ink"],
            fontweight="bold" if colour == F.PALETTE["blue"] else "normal")

# axis labels
ax.text(0.5, 2.08, "Human performance", ha="center", va="bottom",
        fontsize=10, color=F.PALETTE["ink"], fontweight="bold",
        transform=ax.transData)
ax.text(1.5, 2.08, "Rational performance", ha="center", va="bottom",
        fontsize=10, color=F.PALETTE["ink"], fontweight="bold",
        transform=ax.transData)
ax.text(-0.08, 1.5, "Thought /\nReasoning", ha="right", va="center",
        fontsize=9.5, color=F.PALETTE["ink"], rotation=90,
        transform=ax.transData)
ax.text(-0.08, 0.5, "Acting /\nBehaviour", ha="right", va="center",
        fontsize=9.5, color=F.PALETTE["ink"], rotation=90,
        transform=ax.transData)

ax.set_title("Four perspectives on AI — this course focuses on cell (4)",
             color=F.PALETTE["ink"], fontweight="bold", fontsize=11, pad=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_ai_perspectives.png"))
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. Vacuum percept-action table — a tidy annotated table visual
# ---------------------------------------------------------------------------
F.use_house_style()
fig, ax = plt.subplots(figsize=(7.0, 3.2))
ax.axis("off")

percepts = [
    "[A, Clean]", "[A, Dirty]", "[B, Clean]", "[B, Dirty]",
    "[A,C],[A,C]", "[A,C],[A,D]",
]
actions = ["Right", "Suck", "Left", "Suck", "Right", "Suck"]

col_w = [0.62, 0.18]
headers = ["Percept sequence", "Action"]
y_start = 0.88
row_h = 0.12

# header row
for j, (h, w_frac) in enumerate(zip(headers, [0.62, 0.38])):
    x = 0.02 if j == 0 else 0.66
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y_start), w_frac - 0.03, row_h,
        boxstyle="square,pad=0.005",
        fc=F.PALETTE["blue"], ec="none", transform=ax.transAxes))
    ax.text(x + (w_frac - 0.03) / 2, y_start + row_h / 2, h,
            ha="center", va="center", transform=ax.transAxes,
            color="white", fontsize=9.5, fontweight="bold")

# data rows
for i, (perc, act) in enumerate(zip(percepts, actions)):
    y = y_start - (i + 1) * row_h
    bg = F.PALETTE["fill"] if i % 2 == 0 else "white"
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.02, y), 0.59, row_h,
        boxstyle="square,pad=0.005", fc=bg, ec=F.PALETTE["grid"],
        lw=0.5, transform=ax.transAxes))
    ax.text(0.04, y + row_h / 2, perc, ha="left", va="center",
            transform=ax.transAxes, color=F.PALETTE["ink"], fontsize=9.5)
    act_col = F.PALETTE["green"] if act == "Suck" else F.PALETTE["blue"]
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.66, y), 0.32, row_h,
        boxstyle="square,pad=0.005", fc=bg, ec=F.PALETTE["grid"],
        lw=0.5, transform=ax.transAxes))
    ax.text(0.82, y + row_h / 2, act, ha="center", va="center",
            transform=ax.transAxes, color=act_col,
            fontsize=9.5, fontweight="bold")

ax.set_title("Vacuum-cleaner agent: percept sequence → action (the agent function)",
             color=F.PALETTE["ink"], fontweight="bold", fontsize=11, pad=9)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_vacuum_table.png"))
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. AI history timeline — bar chart of eras
# ---------------------------------------------------------------------------
eras   = ["1900–1950\nFoundations", "1950–1973\nEarly AI",
          "1980–1987\nExpert sys.", "1993–2000\nRobots",
          "2000–2012\nDeep belief", "2012–2017\nDeep learning",
          "2017–2020\nTransformers", "2020–\nLLMs & agents"]
scores = [1, 2, 3, 2, 3, 5, 6, 8]   # relative progress score
cols   = [F.PALETTE["muted"], F.PALETTE["muted"], F.PALETTE["muted"],
          F.PALETTE["muted"], F.PALETTE["blue"], F.PALETTE["blue"],
          F.PALETTE["green"], F.PALETTE["purple"]]

F.bars(
    eras, scores,
    "AI progress by era — data, compute, and algorithms converge post-2012",
    ylabel="relative progress (illustrative)", colors=cols,
    annotate=False,
    out=os.path.join(HERE, "fig_ai_timeline.png"),
)

# ---------------------------------------------------------------------------
# 6. Rational agents — performance measure bar chart for vacuum cleaner
# ---------------------------------------------------------------------------
F.bars(
    ["Dirt cleaned", "Energy used\n(lower = better)", "Noise made\n(lower = better)", "Time taken\n(lower = better)"],
    [0.9, 0.4, 0.3, 0.6],
    "Vacuum-cleaner performance measure: what counts as success?",
    ylabel="score (higher bar = better outcome)", colors=[
        F.PALETTE["green"], F.PALETTE["red"], F.PALETTE["amber"], F.PALETTE["blue"]
    ],
    annotate=False,
    out=os.path.join(HERE, "fig_performance_measure.png"),
)

print("All figures written to:", HERE)
