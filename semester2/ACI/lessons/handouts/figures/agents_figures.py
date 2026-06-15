#!/usr/bin/env python3
"""Figure scripts for ACI Session 1: Agents, PEAS & Task Environments.

Run via build_pdf.py which sets MPLBACKEND=Agg and PYTHONPATH so that
figstyle is importable. Saves PNGs next to this script (in figures/).
"""
import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
# Locate figstyle.py: try ../../scripts (handouts/figures -> handouts -> lessons)
# then ../../../scripts (handouts/figures -> handouts -> ACI -> semester2)
# then the kit root scripts/ relative to a known path
for _up in (
    os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".claude", "skills", "make-lecture-kit", "scripts")),
    os.path.normpath(os.path.join(HERE, "..", "..", "scripts")),
    os.path.normpath(os.path.join(HERE, "..", "scripts")),
    os.path.normpath(os.path.join(HERE, "../../..", ".claude/skills/make-lecture-kit/scripts")),
):
    if os.path.isfile(os.path.join(_up, "figstyle.py")):
        sys.path.insert(0, _up)
        break

# Try absolute kit path as fallback
_kit_scripts = "/Users/jayakrishnanj/mtech/.claude/skills/make-lecture-kit/scripts"
if os.path.isdir(_kit_scripts) and _kit_scripts not in sys.path:
    sys.path.insert(0, _kit_scripts)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# ---------------------------------------------------------------------------
# House style constants (mirror figstyle.py palette)
# ---------------------------------------------------------------------------
NAVY      = "#21355E"
BLUE      = "#2C5AA0"
GREEN     = "#2E7D52"
AMBER     = "#8A5A1E"
RED       = "#B23A48"
PURPLE    = "#6A4C93"
LIGHT_BG  = "#F7F9FC"


def _save(fig, fname):
    fig.savefig(os.path.join(HERE, fname), dpi=150, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print(f"  saved: {fname}")


# ---------------------------------------------------------------------------
# Figure 1: Four perspectives on AI (2x2 grid)
# ---------------------------------------------------------------------------
def fig_ai_perspectives():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Draw the 2x2 grid
    cells = [
        (0.3, 3.6, 4.4, 3.0, BLUE,   "(1) Thinking Humanly",   "Cognitive Modelling\n(mirror human thought)"),
        (5.3, 3.6, 4.4, 3.0, NAVY,   "(3) Thinking Rationally","Laws of Thought\n(logic & correct inference)"),
        (0.3, 0.2, 4.4, 3.0, GREEN,  "(2) Acting Humanly",     "Turing Test Approach\n(behave like a human)"),
        (5.3, 0.2, 4.4, 3.0, PURPLE, "(4) Acting Rationally",  "Rational Agent\n(do the right thing — this course)"),
    ]
    for x, y, w, h, col, title, body in cells:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                              linewidth=1.5, edgecolor=col,
                              facecolor=col + "18")
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.45, title, ha="center", va="top",
                fontsize=9, fontweight="bold", color=col)
        ax.text(x + w/2, y + h/2 - 0.25, body, ha="center", va="center",
                fontsize=8, color="#333333", linespacing=1.4)

    # Row / column labels
    ax.text(5.0, 6.8, "human-like  vs.  rational", ha="center", va="top",
            fontsize=10, color=NAVY, fontweight="bold")
    ax.text(0.05, 5.1, "thought /\nreasoning", ha="left", va="center",
            fontsize=8, color="#555555", rotation=0)
    ax.text(0.05, 1.7, "behaviour /\nacting", ha="left", va="center",
            fontsize=8, color="#555555", rotation=0)

    # Dividers
    ax.plot([0.3, 9.7], [3.55, 3.55], color="#AAAAAA", lw=1, ls="--")
    ax.plot([5.0, 5.0], [0.2, 6.7], color="#AAAAAA", lw=1, ls="--")

    ax.set_title("Four Perspectives on Artificial Intelligence",
                 fontsize=11, fontweight="bold", color=NAVY, pad=8)
    _save(fig, "fig_ai_perspectives.png")


# ---------------------------------------------------------------------------
# Figure 2: Agent loop (sensors → percepts → agent → actions → actuators → env)
# ---------------------------------------------------------------------------
def fig_agent_loop():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    def box(cx, cy, w, h, label, col, sub=""):
        rect = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                              boxstyle="round,pad=0.08",
                              linewidth=1.5, edgecolor=col,
                              facecolor=col + "22")
        ax.add_patch(rect)
        ax.text(cx, cy + (0.15 if sub else 0), label, ha="center", va="center",
                fontsize=9, fontweight="bold", color=col)
        if sub:
            ax.text(cx, cy - 0.28, sub, ha="center", va="center",
                    fontsize=7.5, color="#555555")

    def arrow(x1, y1, x2, y2, label="", col=NAVY):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.22, label, ha="center", va="bottom",
                    fontsize=7.5, color=col)

    # Nodes
    box(1.5, 2.5, 2.2, 1.1, "Environment", NAVY)
    box(5.0, 2.5, 1.8, 1.1, "Agent", BLUE, "f: P* → A")
    box(8.5, 3.8, 1.8, 0.9, "Sensors", GREEN)
    box(8.5, 1.2, 1.8, 0.9, "Actuators", AMBER)

    # Arrows
    arrow(9.4, 3.4, 6.8, 3.1, "percepts", GREEN)   # sensors -> agent
    arrow(6.8, 1.9, 9.4, 1.6, "actions",  AMBER)   # agent -> actuators
    arrow(9.4, 1.6, 8.6, 3.3, "",         "#999999") # actuators link to sensors (env loop)
    arrow(2.6, 3.0, 4.1, 2.8, "perceives", NAVY)   # env -> agent
    arrow(4.1, 2.2, 2.6, 2.0, "acts on",  NAVY)    # agent -> env

    # env <-> sensors/actuators side arrows
    ax.annotate("", xy=(7.6, 3.8), xytext=(2.6, 3.5),
                arrowprops=dict(arrowstyle="-|>", color="#888888", lw=1,
                                connectionstyle="arc3,rad=-0.3"))
    ax.text(5.1, 4.45, "sensors read environment", ha="center",
            fontsize=7.5, color="#666666")

    ax.annotate("", xy=(2.6, 1.5), xytext=(7.6, 1.2),
                arrowprops=dict(arrowstyle="-|>", color="#888888", lw=1,
                                connectionstyle="arc3,rad=-0.3"))
    ax.text(5.1, 0.65, "actuators change environment", ha="center",
            fontsize=7.5, color="#666666")

    ax.set_title("The Agent Loop: perceive → decide → act",
                 fontsize=11, fontweight="bold", color=NAVY, pad=8)
    _save(fig, "fig_agent_loop.png")


# ---------------------------------------------------------------------------
# Figure 3: Vacuum-cleaner agent percept-action table (bar chart style)
# ---------------------------------------------------------------------------
def fig_vacuum_table():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis("off")

    percepts = [
        "[A, Clean]",
        "[A, Dirty]",
        "[B, Clean]",
        "[B, Dirty]",
        "[A,Clean],[A,Clean]",
        "[A,Clean],[A,Dirty]",
    ]
    actions = ["Right", "Suck", "Left", "Suck", "Right", "Suck"]
    colours = [GREEN if a == "Suck" else BLUE for a in actions]

    col_labels = ["Percept sequence", "Action"]
    table_data = [[p, a] for p, a in zip(percepts, actions)]

    tbl = ax.table(
        cellText=table_data,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9.5)
    tbl.scale(1, 1.6)

    for (row, col), cell in tbl.get_celld().items():
        cell.set_edgecolor("#CCCCCC")
        if row == 0:
            cell.set_facecolor(NAVY)
            cell.set_text_props(color="white", fontweight="bold")
        elif col == 1:
            a = actions[row - 1]
            cell.set_facecolor(GREEN + "33" if a == "Suck" else BLUE + "22")
        else:
            cell.set_facecolor("#FAFAFA" if row % 2 == 0 else "white")

    ax.set_title("Vacuum-cleaner agent: percept sequence → action mapping",
                 fontsize=10, fontweight="bold", color=NAVY, pad=10)
    _save(fig, "fig_vacuum_table.png")


# ---------------------------------------------------------------------------
# Figure 4: PEAS for automated taxi (structured summary box)
# ---------------------------------------------------------------------------
def fig_peas_taxi():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    rows = [
        ("P",  "Performance",  "Safe, fast, legal, comfortable trip;\nmaximise profits",            PURPLE),
        ("E",  "Environment",  "Roads, traffic, signals,\npedestrians, customers",                  BLUE),
        ("A",  "Actuators",    "Steering wheel, accelerator,\nbrake, signal, horn",                 GREEN),
        ("S",  "Sensors",      "Cameras, sonar, speedometer,\nGPS, odometer, engine sensors",       AMBER),
    ]

    row_h = 1.15
    for i, (letter, label, detail, col) in enumerate(rows):
        y = 4.5 - i * row_h
        # Letter pill
        pill = FancyBboxPatch((0.2, y - 0.42), 0.65, 0.84,
                              boxstyle="round,pad=0.05",
                              linewidth=1.5, edgecolor=col, facecolor=col)
        ax.add_patch(pill)
        ax.text(0.52, y, letter, ha="center", va="center",
                fontsize=14, fontweight="bold", color="white")
        # Label
        ax.text(1.1, y + 0.12, label, ha="left", va="center",
                fontsize=9.5, fontweight="bold", color=col)
        # Detail
        ax.text(1.1, y - 0.22, detail, ha="left", va="center",
                fontsize=8.5, color="#444444", linespacing=1.35)
        # Horizontal rule
        if i < 3:
            ax.plot([0.2, 9.8], [y - 0.58, y - 0.58], color="#DDDDDD", lw=0.8)

    # Outer border
    border = FancyBboxPatch((0.15, 0.08), 9.7, 5.4,
                            boxstyle="round,pad=0.05",
                            linewidth=1.5, edgecolor=NAVY,
                            facecolor="none")
    ax.add_patch(border)

    ax.set_title("PEAS description: Automated Taxi Driver",
                 fontsize=11, fontweight="bold", color=NAVY, pad=8)
    _save(fig, "fig_peas_taxi.png")


# ---------------------------------------------------------------------------
# Figure 5: AI history mini timeline (key milestones)
# ---------------------------------------------------------------------------
def fig_ai_timeline():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.set_xlim(1940, 2030)
    ax.set_ylim(-1.5, 2.5)
    ax.axis("off")

    milestones = [
        (1950, "Turing\nTest",    1.2,  BLUE),
        (1956, "AI term\nborn",   1.2,  NAVY),
        (1986, "Back-\nprop",    -0.8,  GREEN),
        (1997, "Deep\nBlue",      1.2,  AMBER),
        (2012, "AlexNet\n(DL)",  -0.8,  GREEN),
        (2017, "Transformers",    1.2,  PURPLE),
        (2022, "ChatGPT",        -0.8,  RED),
    ]

    # Baseline
    ax.plot([1945, 2027], [0, 0], color=NAVY, lw=2)

    for year, label, yoff, col in milestones:
        ax.plot([year, year], [0, yoff * 0.55], color=col, lw=1.2, ls="--")
        ax.plot(year, 0, "o", color=col, markersize=8, zorder=5)
        ax.text(year, yoff * 0.55 + (0.2 if yoff > 0 else -0.2),
                label, ha="center",
                va="bottom" if yoff > 0 else "top",
                fontsize=7.5, color=col, fontweight="bold",
                linespacing=1.3)
        ax.text(year, -0.22, str(year), ha="center", va="top",
                fontsize=7, color="#666666")

    # "AI winters" shading
    for x0, x1, lab in [(1973, 1980, "1st\nWinter"), (1987, 1993, "2nd\nWinter")]:
        ax.axvspan(x0, x1, alpha=0.08, color="gray")
        ax.text((x0+x1)/2, -1.1, lab, ha="center", va="center",
                fontsize=7, color="#888888")

    ax.set_title("A brief history of AI: key milestones",
                 fontsize=11, fontweight="bold", color=NAVY, pad=6)
    _save(fig, "fig_ai_timeline.png")


# Run all
if __name__ == "__main__":
    fig_ai_perspectives()
    fig_agent_loop()
    fig_vacuum_table()
    fig_peas_taxi()
    fig_ai_timeline()
    print("All figures done.")
