"""
Figure scripts for ACI Lesson 5: NEAT & NAS companion handout.
Generates:
  fig_speciation_fitness.png  — bar chart of raw vs shared fitness per species
  fig_nas_strategies.png      — bar chart comparing NAS search strategy costs
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for up in ("../../../scripts", "../../../../.claude/skills/make-lecture-kit/scripts"):
    p = os.path.normpath(os.path.join(HERE, up))
    if os.path.isdir(p):
        sys.path.insert(0, p)
        break

# Fall back to plain matplotlib with house style applied manually
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

NAVY   = "#21355E"
GREEN  = "#2E7D52"
AMBER  = "#8A5A1E"
BLUE   = "#2C5AA0"
RED    = "#B23A48"
LIGHT  = "#F4F7FC"

def house_style(ax, title):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#AAAAAA")
    ax.spines["bottom"].set_color("#AAAAAA")
    ax.tick_params(colors="#444444", labelsize=9)
    ax.set_title(title, fontsize=10, fontweight="bold", color=NAVY, pad=8)

# ── Figure 1: Speciation & Fitness Sharing ─────────────────────────────────
# S1: 4 individuals, raw fitness [10, 8, 6, 4]  → shared = raw/4
# S2: 2 individuals, raw fitness [9, 7]          → shared = raw/2

labels_s1 = ["S1-A\n(raw 10)", "S1-B\n(raw 8)", "S1-C\n(raw 6)", "S1-D\n(raw 4)"]
raw_s1    = [10, 8, 6, 4]
shared_s1 = [v / 4 for v in raw_s1]

labels_s2 = ["S2-A\n(raw 9)", "S2-B\n(raw 7)"]
raw_s2    = [9, 7]
shared_s2 = [v / 2 for v in raw_s2]

all_labels = labels_s1 + labels_s2
all_raw    = raw_s1 + raw_s2
all_shared = shared_s1 + shared_s2
x = np.arange(len(all_labels))
w = 0.35

fig, ax = plt.subplots(figsize=(8, 4.2))
b1 = ax.bar(x - w/2, all_raw,    w, label="Raw fitness",    color=BLUE,  alpha=0.75)
b2 = ax.bar(x + w/2, all_shared, w, label="Shared fitness", color=GREEN, alpha=0.85)

# Draw a vertical line between S1 and S2 groups
ax.axvline(x=3.5, color="#AAAAAA", linestyle="--", linewidth=0.9)
ax.text(1.5,  10.5, "Species $S_1$ (size 4)", ha="center", fontsize=8.5, color=NAVY)
ax.text(4.5,  10.5, "Species $S_2$ (size 2)", ha="center", fontsize=8.5, color=NAVY)

ax.set_xticks(x)
ax.set_xticklabels(all_labels, fontsize=8)
ax.set_ylabel("Fitness", fontsize=9, color="#444444")
ax.legend(fontsize=9)
house_style(ax, "Fitness Sharing: raw vs. shared fitness by species")
fig.tight_layout()
out1 = os.path.join(HERE, "fig_speciation_fitness.png")
fig.savefig(out1, dpi=150)
plt.close(fig)
print(f"Saved {out1}")

# ── Figure 2: NAS Search Strategy Comparison ──────────────────────────────
# Approximate relative costs (GPU-hours for ImageNet-scale search, order-of-magnitude)
strategies  = ["Grid\nsearch", "Random\nsearch", "RL\ncontroller", "Evolutionary\n(NEAT-style)", "Gradient-based\n(DARTS)"]
gpu_hours   = [10000, 4000, 1800, 3150, 4]   # rough representative values
colors      = [RED, AMBER, BLUE, GREEN, NAVY]

fig, ax = plt.subplots(figsize=(8, 4.2))
bars = ax.bar(strategies, gpu_hours, color=colors, alpha=0.85, edgecolor="white")
for bar, val in zip(bars, gpu_hours):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 120,
            f"{val:,}", ha="center", va="bottom", fontsize=8.5, color=NAVY)
ax.set_ylabel("Approx. GPU-hours (relative scale)", fontsize=9, color="#444444")
ax.set_ylim(0, 12000)
house_style(ax, "NAS search strategy: approximate search cost (lower is faster)")
fig.tight_layout()
out2 = os.path.join(HERE, "fig_nas_strategies.png")
fig.savefig(out2, dpi=150)
plt.close(fig)
print(f"Saved {out2}")
