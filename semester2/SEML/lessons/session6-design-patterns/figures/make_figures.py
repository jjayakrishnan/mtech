"""Figure scripts for Session 6: EDA, Model Registry & Serving Patterns."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Resolve the make-lecture-kit scripts/ folder (up several levels).
for _up in ("../../../.claude/skills/make-lecture-kit/scripts",
            "../../../../.claude/skills/make-lecture-kit/scripts",
            "../../../../../.claude/skills/make-lecture-kit/scripts"):
    _p = os.path.normpath(os.path.join(HERE, _up))
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
        break

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

try:
    import figstyle as F
    F.use_house_style()
    PALETTE = F.PALETTE
except ImportError:
    PALETTE = {
        "blue":   "#2C5AA0",
        "green":  "#2E7D52",
        "amber":  "#C8881E",
        "red":    "#B23A48",
        "purple": "#6A4C93",
        "ink":    "#21355E",
        "muted":  "#5B6470",
        "grid":   "#D9DEE8",
    }

# ──────────────────────────────────────────────────────────────────────────────
# Figure 1 – Event-Driven Architecture: Publish-Subscribe flow
# ──────────────────────────────────────────────────────────────────────────────
def fig_eda_pubsub():
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    def box(x, y, w, h, label, color, fontsize=9):
        rect = mpatches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.1",
            linewidth=1.2, edgecolor=color, facecolor=color + "22"
        )
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=color, wrap=True)

    def arrow(x1, y1, x2, y2, label="", color="#21355E"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.4))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + 0.18
            ax.text(mx, my, label, ha="center", va="bottom",
                    fontsize=7.5, color=color)

    # Producers
    box(1.5, 3.0, 2.2, 0.7, "Producer A\n(user action)", PALETTE["blue"])
    box(1.5, 1.8, 2.2, 0.7, "Producer B\n(external API)", PALETTE["blue"])

    # Event Bus
    box(5.0, 2.4, 2.4, 1.2, "Event Bus /\nMessage Broker\n(Kafka, RabbitMQ)",
        PALETTE["ink"], fontsize=8)

    # Consumers
    box(8.5, 3.0, 2.2, 0.7, "Consumer 1\n(ML pipeline)", PALETTE["green"])
    box(8.5, 1.8, 2.2, 0.7, "Consumer 2\n(alerting)", PALETTE["green"])

    # Arrows
    arrow(2.6, 3.0, 3.8, 2.7, "publish")
    arrow(2.6, 1.8, 3.8, 2.1, "publish")
    arrow(6.2, 2.7, 7.4, 3.0, "notify")
    arrow(6.2, 2.1, 7.4, 1.8, "notify")

    ax.set_title(
        "Event-Driven Architecture: producers publish events; the broker routes them to subscribers",
        fontsize=9, fontweight="bold", color=PALETTE["ink"], pad=6
    )
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_eda_pubsub.png"), dpi=150)
    plt.close(fig)
    print("fig_eda_pubsub.png saved")


# ──────────────────────────────────────────────────────────────────────────────
# Figure 2 – Version Control Generations (bar / comparison)
# ──────────────────────────────────────────────────────────────────────────────
def fig_vcs_generations():
    fig, ax = plt.subplots(figsize=(7.0, 2.8))
    ax.set_xlim(0, 4.4)
    ax.set_ylim(-0.5, 3.5)
    ax.axis("off")

    gens = [
        ("Gen 1\n(RCS, SCCS)", "None", "One file\nat a time", PALETTE["muted"]),
        ("Gen 2\n(SVN, CVS)", "Centralised", "Multi-file", PALETTE["blue"]),
        ("Gen 3 – SD\n(Git)", "Distributed", "Changesets", PALETTE["green"]),
        ("Gen 3 – ML\n(MLflow, DVC)", "Distributed +\nArtifact tracking",
         "Models, data,\nexperiments", PALETTE["purple"]),
    ]

    for i, (gen, net, ops, col) in enumerate(gens):
        x = 0.5 + i * 0.95
        rect = mpatches.FancyBboxPatch(
            (x - 0.38, 0.1), 0.76, 2.8,
            boxstyle="round,pad=0.05",
            linewidth=1.2, edgecolor=col, facecolor=col + "18"
        )
        ax.add_patch(rect)
        ax.text(x, 2.7, gen, ha="center", va="top",
                fontsize=7.5, fontweight="bold", color=col)
        ax.text(x, 1.7, net, ha="center", va="center",
                fontsize=7, color=PALETTE["ink"])
        ax.text(x, 0.9, ops, ha="center", va="center",
                fontsize=7, color=PALETTE["ink"])

    # Row labels on the left
    ax.text(0.03, 2.7, "Tool", ha="left", va="top",
            fontsize=7, color=PALETTE["muted"], fontstyle="italic")
    ax.text(0.03, 1.7, "Network", ha="left", va="center",
            fontsize=7, color=PALETTE["muted"], fontstyle="italic")
    ax.text(0.03, 0.9, "Operations", ha="left", va="center",
            fontsize=7, color=PALETTE["muted"], fontstyle="italic")

    ax.set_title(
        "Three generations of version control — the fourth adds ML artifact tracking",
        fontsize=9, fontweight="bold", color=PALETTE["ink"], pad=4
    )
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_vcs_generations.png"), dpi=150)
    plt.close(fig)
    print("fig_vcs_generations.png saved")


# ──────────────────────────────────────────────────────────────────────────────
# Figure 3 – Model Registry: model lifecycle stages
# ──────────────────────────────────────────────────────────────────────────────
def fig_model_registry():
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")

    stages = [
        ("Experiment\n& Train", PALETTE["blue"],  1.0),
        ("Register\nModel", PALETTE["green"],     3.0),
        ("Staging /\nValidation", PALETTE["amber"], 5.0),
        ("Production\nDeployment", PALETTE["ink"], 7.0),
        ("Monitor\n& Retire", PALETTE["red"],      9.0),
    ]

    for label, col, x in stages:
        circle = plt.Circle((x, 1.5), 0.7, color=col, alpha=0.15, zorder=2)
        ax.add_patch(circle)
        circle2 = plt.Circle((x, 1.5), 0.7, color=col, fill=False,
                              linewidth=1.4, zorder=3)
        ax.add_patch(circle2)
        ax.text(x, 1.5, label, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=col, zorder=4)

    # Arrows between circles
    for i in range(len(stages) - 1):
        x1 = stages[i][2] + 0.7
        x2 = stages[i + 1][2] - 0.7
        ax.annotate("", xy=(x2, 1.5), xytext=(x1, 1.5),
                    arrowprops=dict(arrowstyle="->",
                                   color=PALETTE["muted"], lw=1.2))

    ax.set_title(
        "Model Registry: the lifecycle from experiment to production and retirement",
        fontsize=9, fontweight="bold", color=PALETTE["ink"], pad=4
    )
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_model_registry.png"), dpi=150)
    plt.close(fig)
    print("fig_model_registry.png saved")


# ──────────────────────────────────────────────────────────────────────────────
# Figure 4 – Batch vs Real-Time Serving comparison
# ──────────────────────────────────────────────────────────────────────────────
def fig_batch_vs_realtime():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))

    # Left: Batch prediction timeline
    ax = axes[0]
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("Batch Prediction", fontsize=9, fontweight="bold",
                 color=PALETTE["blue"], pad=4)

    steps_b = [
        (1.0, 3.2, "Collect\ndata", PALETTE["muted"]),
        (3.0, 3.2, "Run model\n(scheduled)", PALETTE["blue"]),
        (5.0, 3.2, "Store\nresults", PALETTE["green"]),
        (3.0, 1.5, "Send\nbatch emails\nnext morning", PALETTE["amber"]),
    ]
    for x, y, lbl, col in steps_b:
        r = mpatches.FancyBboxPatch((x - 0.7, y - 0.4), 1.4, 0.8,
                                     boxstyle="round,pad=0.05",
                                     linewidth=1.0, edgecolor=col,
                                     facecolor=col + "22")
        ax.add_patch(r)
        ax.text(x, y, lbl, ha="center", va="center",
                fontsize=7, color=col, fontweight="bold")

    ax.annotate("", xy=(2.3, 3.2), xytext=(1.7, 3.2),
                arrowprops=dict(arrowstyle="->", color=PALETTE["muted"], lw=1.1))
    ax.annotate("", xy=(4.3, 3.2), xytext=(3.7, 3.2),
                arrowprops=dict(arrowstyle="->", color=PALETTE["muted"], lw=1.1))
    ax.annotate("", xy=(3.0, 1.9), xytext=(3.0, 2.8),
                arrowprops=dict(arrowstyle="->", color=PALETTE["amber"], lw=1.1))
    ax.text(3.0, 0.7, "Low latency requirement\nHigh throughput",
            ha="center", fontsize=7, color=PALETTE["muted"], fontstyle="italic")

    # Right: Real-time prediction
    ax = axes[1]
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("Real-Time (Online) Prediction", fontsize=9, fontweight="bold",
                 color=PALETTE["red"], pad=4)

    steps_r = [
        (1.0, 3.2, "Request\narrives", PALETTE["muted"]),
        (3.0, 3.2, "Model API\n(always on)", PALETTE["red"]),
        (5.0, 3.2, "Prediction\nin ms", PALETTE["green"]),
    ]
    for x, y, lbl, col in steps_r:
        r = mpatches.FancyBboxPatch((x - 0.7, y - 0.4), 1.4, 0.8,
                                     boxstyle="round,pad=0.05",
                                     linewidth=1.0, edgecolor=col,
                                     facecolor=col + "22")
        ax.add_patch(r)
        ax.text(x, y, lbl, ha="center", va="center",
                fontsize=7, color=col, fontweight="bold")

    ax.annotate("", xy=(2.3, 3.2), xytext=(1.7, 3.2),
                arrowprops=dict(arrowstyle="->", color=PALETTE["muted"], lw=1.1))
    ax.annotate("", xy=(4.3, 3.2), xytext=(3.7, 3.2),
                arrowprops=dict(arrowstyle="->", color=PALETTE["muted"], lw=1.1))

    ax.text(3.0, 0.7, "High latency requirement\n(milliseconds matter)",
            ha="center", fontsize=7, color=PALETTE["muted"], fontstyle="italic")

    fig.suptitle(
        "Batch vs real-time: trade freshness for complexity and cost",
        fontsize=9, fontweight="bold", color=PALETTE["ink"]
    )
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_batch_vs_realtime.png"), dpi=150)
    plt.close(fig)
    print("fig_batch_vs_realtime.png saved")


if __name__ == "__main__":
    fig_eda_pubsub()
    fig_vcs_generations()
    fig_model_registry()
    fig_batch_vs_realtime()
    print("All figures done.")
