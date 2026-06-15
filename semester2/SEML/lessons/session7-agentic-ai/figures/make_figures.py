"""Figure scripts for SEML Session 7: Agentic AI, SAGA & Blackboard.

Generates three PNGs:
  fig_genai_vs_agentic.png   — bar/flow comparison of GenAI vs Agentic AI
  fig_saga_flow.png          — four-step saga happy path + compensating path
  fig_saga_orchestration.png — orchestrator + worker agents diagram
  fig_blackboard.png         — blackboard + knowledge sources + controller
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Locate the skills/scripts directory robustly (figstyle.py lives there).
for _up in ("../../../.claude/skills/make-lecture-kit/scripts",
            "../../../../.claude/skills/make-lecture-kit/scripts",
            "../scripts", "../../scripts", "../../../scripts"):
    _p = os.path.normpath(os.path.join(HERE, _up))
    if os.path.isfile(os.path.join(_p, "figstyle.py")):
        sys.path.insert(0, _p)
        break

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# ---------------------------------------------------------------------------
# House colours (matching the tcolorbox taxonomy in the .tex)
# ---------------------------------------------------------------------------
NAVY   = "#21355E"
BLUE   = "#2C5AA0"
GREEN  = "#2E7D52"
AMBER  = "#C8881E"
RED    = "#B23A48"
PURPLE = "#6A4C93"
MUTED  = "#5B6470"
FILL   = "#EAF0F7"
WHITE  = "#FFFFFF"

def _savefig(fig, name):
    path = os.path.join(HERE, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved: {name}")


# ===========================================================================
# Figure 1 — Generative AI vs Agentic AI
# ===========================================================================
def fig_genai_vs_agentic():
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    fig.patch.set_facecolor(WHITE)

    # ---- Left: Generative AI (one-shot) ------------------------------------
    ax = axes[0]
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3)
    ax.axis("off")
    ax.set_title("Generative AI", fontsize=12, fontweight="bold", color=NAVY)

    # prompt box
    _box(ax, 0.3, 2.1, 1.4, 0.55, FILL, BLUE, "Prompt", 10, NAVY)
    # model box
    _box(ax, 1.5, 2.1, 1.0, 0.55, "#FBF1E3", AMBER, "LLM", 10, NAVY)
    # output box
    _box(ax, 2.8, 2.1, 0.9, 0.55, "#F1F8F3", GREEN, "Output", 10, NAVY)
    # arrows
    _arr(ax, 1.7, 2.38, 1.5, 2.38)
    _arr(ax, 2.5, 2.38, 2.8, 2.38)
    ax.text(2.0, 1.55, "One prompt → One answer\nNo loop, no tools", ha="center",
            va="center", fontsize=9, color=MUTED)

    # ---- Right: Agentic AI (loop) ------------------------------------------
    ax2 = axes[1]
    ax2.set_facecolor(WHITE)
    ax2.set_xlim(0, 4)
    ax2.set_ylim(0, 3)
    ax2.axis("off")
    ax2.set_title("Agentic AI", fontsize=12, fontweight="bold", color=NAVY)

    _box(ax2, 0.1, 2.25, 0.9, 0.55, FILL, BLUE, "Goal", 9, NAVY)
    _box(ax2, 1.25, 2.25, 1.2, 0.55, "#FBF1E3", AMBER, "Reason\n& Plan", 8, NAVY)
    _box(ax2, 2.7, 2.25, 1.0, 0.55, "#F1F8F3", GREEN, "Act /\nCall Tool", 8, NAVY)
    _box(ax2, 1.55, 0.8, 1.0, 0.55, "#F4F0F9", PURPLE, "Check &\nRevise", 8, NAVY)

    _arr(ax2, 1.0, 2.52, 1.25, 2.52)
    _arr(ax2, 2.45, 2.52, 2.7, 2.52)
    # loop back: Action → Check
    _arr(ax2, 3.2, 2.25, 3.2, 1.5, style="arc3,rad=-0.3")
    _arr(ax2, 3.0, 1.07, 2.55, 1.07)
    # Check → Reason (another loop)
    _arr(ax2, 1.55, 1.07, 1.0, 1.07)
    _arr(ax2, 0.7, 1.07, 0.7, 2.25, style="arc3,rad=-0.3")

    fig.suptitle("Generative AI vs. Agentic AI: the loop makes the difference",
                 fontsize=11, fontweight="bold", color=NAVY, y=0.98)
    _savefig(fig, "fig_genai_vs_agentic.png")


def _box(ax, x, y, w, h, fc, ec, label, fs, tc):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.04", facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(x + w/2, y + h/2, label, ha="center", va="center",
            fontsize=fs, color=tc, fontweight="bold")


def _arr(ax, x0, y0, x1, y1, style="arc3,rad=0.0"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2,
                                connectionstyle=style))


# ===========================================================================
# Figure 2 — SAGA flow: happy path + compensating path
# ===========================================================================
def fig_saga_flow():
    fig, ax = plt.subplots(figsize=(9, 4.2))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(-0.3, 8.5)
    ax.set_ylim(-1.6, 3.4)
    ax.axis("off")
    ax.set_title("SAGA pattern: happy path and compensating rollback",
                 fontsize=11, fontweight="bold", color=NAVY)

    services = ["Order", "Inventory", "Payment", "Shipping"]
    colors   = [BLUE, GREEN, AMBER, PURPLE]
    xs = [0.5, 2.5, 4.5, 6.5]

    # Happy-path row (y=2.2)
    ax.text(-0.2, 2.2, "Happy path →", fontsize=8, color=MUTED, va="center")
    for i, (svc, col, x) in enumerate(zip(services, colors, xs)):
        _box(ax, x - 0.65, 1.85, 1.3, 0.65, FILL, col, svc, 9, NAVY)
        ax.text(x, 1.5, f"Step {i+1}", ha="center", fontsize=7.5, color=MUTED)
        if i < 3:
            ax.annotate("", xy=(xs[i+1] - 0.65, 2.17), xytext=(x + 0.65, 2.17),
                        arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.4))

    # Failure marker at step 3
    ax.text(xs[2], 2.65, "FAIL!", fontsize=8.5, color=RED, fontweight="bold",
            ha="center", va="bottom")
    ax.plot([xs[2]], [2.5], marker="x", markersize=10, color=RED, markeredgewidth=2)

    # Compensating path (y = 0.4 row)
    ax.text(-0.2, 0.4, "Compensate →", fontsize=8, color=MUTED, va="center")
    comp_labels = ["Cancel\nOrder", "Release\nInventory", "—", "—"]
    comp_cols   = [RED, RED, MUTED, MUTED]
    comp_fs     = [8, 8, 7, 7]
    for i, (lbl, col, x) in enumerate(zip(comp_labels[:2], comp_cols[:2], xs[:2])):
        _box(ax, x - 0.65, 0.05, 1.3, 0.65, "#FBF1F2", col, lbl, 8, col)
        ax.text(x, -0.25, f"Undo {i+1}", ha="center", fontsize=7.5, color=MUTED)

    # Arrow: failure drops down to compensate
    ax.annotate("", xy=(xs[1] + 0.65, 0.375), xytext=(xs[2] - 0.65, 1.85),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2,
                                connectionstyle="arc3,rad=0.25"))
    ax.text(3.3, 0.95, "compensating\ntransactions", fontsize=7.5, color=RED,
            ha="center")

    # reverse arrow
    ax.annotate("", xy=(xs[0] + 0.65, 0.375), xytext=(xs[1] - 0.65, 0.375),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
    ax.text(1.5, -0.6, "Reverse order: undo step 2 before step 1",
            fontsize=7.5, color=MUTED, ha="center")

    _savefig(fig, "fig_saga_flow.png")


# ===========================================================================
# Figure 3 — SAGA Orchestration in agentic AI
# ===========================================================================
def fig_saga_orchestration():
    fig, ax = plt.subplots(figsize=(9, 4.0))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("SAGA Orchestration: one orchestrator, many specialist workers",
                 fontsize=11, fontweight="bold", color=NAVY)

    # Orchestrator (centre-top)
    _box(ax, 3.0, 2.8, 3.0, 0.8, "#EAF0F7", NAVY, "Orchestrator Agent\n(plans + delegates)", 9, NAVY)

    # Workers (bottom row)
    workers = [("Research\nAgent", BLUE, 0.4),
               ("Coding\nAgent",  GREEN, 3.0),
               ("Writer\nAgent",  AMBER, 5.6),
               ("Review\nAgent",  PURPLE, 8.2)]
    for lbl, col, x in workers:
        _box(ax, x - 0.15, 0.6, 1.5, 0.9, FILL, col, lbl, 8.5, NAVY)
        # arrow down (delegate)
        ax.annotate("", xy=(x + 0.6, 1.5), xytext=(4.5, 2.8),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.1,
                                   connectionstyle="arc3,rad=0.1"))
        # arrow up (result / compensate)
        ax.annotate("", xy=(4.5, 2.8), xytext=(x + 0.6, 1.5),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8,
                                   connectionstyle="arc3,rad=-0.1"))

    # Shared memory box
    _box(ax, 3.3, 0.1, 2.4, 0.45, "#F1F8F3", GREEN, "Shared memory (saga log)", 8, NAVY)
    ax.text(4.5, 0.33, "", ha="center")

    # Labels
    ax.text(1.2, 2.15, "delegate", fontsize=7, color=BLUE)
    ax.text(1.2, 1.85, "sub-task", fontsize=7, color=BLUE)
    ax.text(7.2, 1.85, "result /", fontsize=7, color=MUTED)
    ax.text(7.2, 1.65, "compensate", fontsize=7, color=MUTED)

    _savefig(fig, "fig_saga_orchestration.png")


# ===========================================================================
# Figure 4 — Blackboard pattern
# ===========================================================================
def fig_blackboard():
    fig, ax = plt.subplots(figsize=(9, 4.2))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    ax.set_title("Blackboard pattern: shared memory + specialist agents + controller",
                 fontsize=11, fontweight="bold", color=NAVY)

    # Central Blackboard
    _box(ax, 3.0, 1.5, 3.0, 1.8, "#EAF0F7", NAVY,
         "Blackboard\n(shared memory)\n\ncurrent state\npartial solutions", 9, NAVY)

    # Controller (top)
    _box(ax, 3.3, 3.5, 2.4, 0.75, "#F4F0F9", PURPLE, "Controller / Scheduler", 9, NAVY)
    ax.annotate("", xy=(4.5, 3.5), xytext=(4.5, 3.3),
                arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.2))
    ax.annotate("", xy=(4.5, 3.3), xytext=(4.5, 3.5),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8))

    # Knowledge sources (left and right)
    ks_left  = [("KS-1\nSection Parser",   BLUE,   0.2, 3.1),
                ("KS-2\nClaim Extractor",  GREEN,  0.2, 1.8),
                ("KS-3\nEvidence Checker", AMBER,  0.2, 0.5)]
    ks_right = [("KS-4\nFact Resolver",   PURPLE, 6.8, 3.1),
                ("KS-5\nSummarizer",       RED,    6.8, 1.8),
                ("KS-6\nWriter",           MUTED,  6.8, 0.5)]

    for lbl, col, x, y in ks_left:
        _box(ax, x, y, 1.8, 0.75, FILL, col, lbl, 8, NAVY)
        # read arrow (KS → board)
        ax.annotate("", xy=(3.0, y + 0.375), xytext=(x + 1.8, y + 0.375),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0))
        # write arrow (board → KS)
        ax.annotate("", xy=(x + 1.8, y + 0.2), xytext=(3.0, y + 0.2),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7))

    for lbl, col, x, y in ks_right:
        _box(ax, x, y, 1.8, 0.75, FILL, col, lbl, 8, NAVY)
        ax.annotate("", xy=(6.0, y + 0.375), xytext=(x, y + 0.375),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0))
        ax.annotate("", xy=(x, y + 0.2), xytext=(6.0, y + 0.2),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7))

    ax.text(2.0, 0.22, "read / write", fontsize=7, color=MUTED, ha="center")
    ax.text(7.3, 0.22, "read / write", fontsize=7, color=MUTED, ha="center")

    _savefig(fig, "fig_blackboard.png")


# ===========================================================================
# Figure 5 — Prompt chaining (saga choreography at the LLM level)
# ===========================================================================
def fig_prompt_chaining():
    fig, ax = plt.subplots(figsize=(9, 3.6))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    ax.set_title("Prompt chaining = SAGA choreography at the LLM level",
                 fontsize=11, fontweight="bold", color=NAVY)

    steps_data = [
        ("Step 1\nHypothesis", BLUE,   0.4, 2.0),
        ("Step 2\nAnalysis",   GREEN,  2.4, 2.0),
        ("Step 3\nReport",     AMBER,  4.4, 2.0),
        ("Step 4\nRefine",     PURPLE, 6.4, 2.0),
    ]

    for lbl, col, x, y in steps_data:
        _box(ax, x, y, 1.6, 0.75, FILL, col, lbl, 9, NAVY)

    # Forward arrows
    for i in range(len(steps_data) - 1):
        x0 = steps_data[i][2] + 1.6
        x1 = steps_data[i+1][2]
        y_mid = 2.375
        ax.annotate("", xy=(x1, y_mid), xytext=(x0, y_mid),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.3))
        ax.text((x0 + x1) / 2, y_mid + 0.12, "output\nfeeds in", ha="center",
                fontsize=6.5, color=MUTED)

    # Compensating arrow (step 2 → retry)
    ax.annotate("", xy=(2.4, 2.0), xytext=(4.0, 2.0),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2,
                                connectionstyle="arc3,rad=0.45"))
    ax.text(3.2, 1.3, "compensate:\nretry prompt", ha="center",
            fontsize=7.5, color=RED)

    # Context window bar at the bottom
    _box(ax, 0.3, 0.25, 8.2, 0.55, "#F4F7FC", BLUE,
         "Shared context window (each step reads all prior outputs)", 8.5, NAVY)

    ax.text(0.5, 1.72, "LLM\ncalls:", fontsize=7, color=MUTED, va="center")

    _savefig(fig, "fig_prompt_chaining.png")


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Generating Session 7 figures...")
    fig_genai_vs_agentic()
    fig_saga_flow()
    fig_saga_orchestration()
    fig_blackboard()
    fig_prompt_chaining()
    print("Done.")
