#!/usr/bin/env python3
"""Figure generator for SEML Session 1 companion PDF.

Produces two matplotlib PNGs:
  1. fig_sdlc_flow.png  — SDLC six-phase process flow (bars comparison)
  2. fig_se_vs_ml.png   — SE vs ML key dimension comparison (bar chart)

Run from the figures/ folder or via build_pdf.py.
"""
import os
import sys

# Resolve figstyle from the skill's scripts/ directory.
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_SCRIPTS = "/Users/jayakrishnanj/mtech/.claude/skills/make-lecture-kit/scripts"
for rel in (SKILL_SCRIPTS, "../../../scripts", "../../scripts"):
    p = os.path.normpath(os.path.join(HERE, rel)) if not os.path.isabs(rel) else rel
    if os.path.isdir(p):
        sys.path.insert(0, p)
        break

import figstyle as F  # noqa: E402
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

F.use_house_style()

# -----------------------------------------------------------------------
# Figure 1: SDLC six-phase horizontal flow
# A horizontal bar showing six phases left to right, colour-coded by type
# -----------------------------------------------------------------------
def make_sdlc_flow():
    fig, ax = plt.subplots(figsize=(7.0, 2.2))
    ax.set_axis_off()

    phases = [
        ("Planning",       F.PALETTE["blue"]),
        ("Requirements",   F.PALETTE["purple"]),
        ("Design",         F.PALETTE["green"]),
        ("Implementation", F.PALETTE["amber"]),
        ("Testing",        F.PALETTE["red"]),
        ("Deploy & Maintain", "#5B6470"),
    ]

    n = len(phases)
    w = 1.0 / n
    pad = 0.008
    arrow_len = 0.03

    for i, (label, col) in enumerate(phases):
        x0 = i * w + pad
        x1 = (i + 1) * w - pad - arrow_len
        ax.add_patch(
            mpatches.FancyBboxPatch(
                (x0, 0.25), x1 - x0, 0.5,
                boxstyle="round,pad=0.01",
                facecolor=col, edgecolor="white", linewidth=1.5,
                transform=ax.transAxes, clip_on=False,
            )
        )
        ax.text(
            (x0 + x1) / 2, 0.50, label,
            transform=ax.transAxes,
            ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white",
        )
        # Arrow to next phase
        if i < n - 1:
            ax.annotate(
                "", xy=((i + 1) * w + pad, 0.50),
                xytext=(x1, 0.50),
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.5),
            )

    ax.set_title(
        "SDLC: six phases from idea to running system",
        color=F.PALETTE["ink"], fontweight="bold", fontsize=11, pad=6,
    )
    out = os.path.join(HERE, "fig_sdlc_flow.png")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


# -----------------------------------------------------------------------
# Figure 2: SE vs ML side-by-side comparison bar chart
# Shows "complexity score" (1=low, 3=high) for four dimensions
# -----------------------------------------------------------------------
def make_se_vs_ml():
    dims = [
        "Specification\nclarity",
        "Debugging\neffort",
        "Test\ndefinability",
        "Failure\nvisibility",
    ]
    se_scores  = [3, 2, 3, 3]   # Traditional SE (higher = easier/better)
    ml_scores  = [1, 3, 1, 1]   # ML Engineering

    x = np.arange(len(dims))
    width = 0.32

    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    bars_se = ax.bar(x - width / 2, se_scores, width,
                     color=F.PALETTE["blue"], label="Traditional SE")
    bars_ml = ax.bar(x + width / 2, ml_scores, width,
                     color=F.PALETTE["amber"], label="ML Engineering")

    ax.set_xticks(x)
    ax.set_xticklabels(dims, fontsize=9.5)
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Low (1)", "Medium (2)", "High (3)"], fontsize=9)
    ax.set_ylabel("Score (higher = easier / clearer)", fontsize=9.5)
    ax.legend(fontsize=9.5)

    # Annotate bar tops
    for bar in list(bars_se) + list(bars_ml):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05,
                str(int(h)), ha="center", va="bottom", fontsize=9,
                color=F.PALETTE["ink"])

    ax.set_title(
        "SE vs ML Engineering: four key dimensions compared",
        color=F.PALETTE["ink"], fontweight="bold", fontsize=11,
    )
    fig.tight_layout()
    out = os.path.join(HERE, "fig_se_vs_ml.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_sdlc_flow()
    make_se_vs_ml()
    print("All figures rendered.")
