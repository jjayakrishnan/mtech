"""
Figure scripts for SEML Session 3 companion PDF.
All figures use figstyle.py helpers where applicable,
with plain matplotlib fallbacks.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Find the skill's scripts/ folder which contains figstyle.py
for rel in ("../../../scripts", "../../../../.claude/skills/make-lecture-kit/scripts"):
    p = os.path.normpath(os.path.join(HERE, rel))
    if os.path.isdir(p):
        sys.path.insert(0, p)
        break

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ---- house style constants ----
NAVY   = "#21355E"
BLUE   = "#2C5AA0"
GREEN  = "#2E7D52"
AMBER  = "#8A5A1E"
RED    = "#B23A48"
PURPLE = "#6A4C93"
LIGHT  = "#F4F7FC"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})


# ===========================================================================
# Figure 1 — When to Use ML vs Rules
# ===========================================================================
def fig_when_to_use_ml():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axis("off")
    fig.patch.set_facecolor("white")

    title = "When to Use ML vs. Rule-Based Systems"
    fig.suptitle(title, fontsize=13, fontweight="bold", color=NAVY, y=0.97)

    # Three columns: Rule-based | Decision | ML
    headers = ["Rule-Based\n(if/else)", "Use if…", "Machine Learning"]
    header_colors = [GREEN, NAVY, BLUE]
    col_x = [0.12, 0.5, 0.85]

    for x, h, c in zip(col_x, headers, header_colors):
        ax.text(x, 0.88, h, ha="center", va="center",
                fontsize=10, fontweight="bold", color="white",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=c, edgecolor="none"))

    cases = [
        ("Simple, stable,\ndeterministic rules",   "Rules can be\nhand-written",      "Language understanding\n(sarcasm, context, nuance)"),
        ("Button 3 → Cola\nAge < 18 → Block",       "Problem is too large\nor too complex",   "Song recommendation\n(100M tracks × 500M users)"),
        ("—",                                       "Problem changes\nover time",             "Fraud detection\n(patterns shift weekly)"),
    ]
    row_y = [0.65, 0.42, 0.18]
    for (left, mid, right), y in zip(cases, row_y):
        ax.text(col_x[0], y, left, ha="center", va="center",
                fontsize=8.5, color="#333",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#e8f5e9", edgecolor=GREEN, lw=0.7))
        ax.text(col_x[1], y, mid, ha="center", va="center",
                fontsize=8.5, color="white", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=NAVY, edgecolor="none"))
        ax.text(col_x[2], y, right, ha="center", va="center",
                fontsize=8.5, color="#333",
                bbox=dict(boxstyle="round,pad=0.3", facecolor=LIGHT, edgecolor=BLUE, lw=0.7))

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = os.path.join(HERE, "fig_when_to_use_ml.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {out}")


# ===========================================================================
# Figure 2 — Goal Hierarchy
# ===========================================================================
def fig_goal_hierarchy():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axis("off")
    fig.patch.set_facecolor("white")
    fig.suptitle("The Four Levels of Goals in an ML System",
                 fontsize=13, fontweight="bold", color=NAVY, y=0.97)

    levels = [
        ("Organisational Goals",  "cost · revenue · compliance · growth",      NAVY,   "#dce7f3"),
        ("User Goals",            "satisfaction · trust · speed · ease of use", BLUE,   "#e8f0fb"),
        ("System Goals",          "latency · availability · throughput",        GREEN,  "#e8f5ec"),
        ("Model Goals",           "AUC · F1 · precision · recall",              AMBER,  "#fdf3e6"),
    ]

    box_h = 0.17
    gap   = 0.04
    start_y = 0.82

    for i, (label, sub, fc, bg) in enumerate(levels):
        y = start_y - i * (box_h + gap)
        rect = FancyBboxPatch((0.05, y - box_h / 2), 0.9, box_h,
                              boxstyle="round,pad=0.01",
                              facecolor=bg, edgecolor=fc, linewidth=1.2)
        ax.add_patch(rect)
        ax.text(0.08, y, label, va="center", ha="left",
                fontsize=10, fontweight="bold", color=fc)
        ax.text(0.92, y, sub, va="center", ha="right",
                fontsize=8.5, color="#555")

    # Arrows between levels
    for i in range(len(levels) - 1):
        y_top = start_y - i * (box_h + gap) - box_h / 2
        y_bot = y_top - gap
        ax.annotate("", xy=(0.5, y_bot), xytext=(0.5, y_top),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = os.path.join(HERE, "fig_goal_hierarchy.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {out}")


# ===========================================================================
# Figure 3 — GR4ML Three Views
# ===========================================================================
def fig_gr4ml_views():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.axis("off")
    fig.patch.set_facecolor("white")
    fig.suptitle("GR4ML: Three Aligned Views",
                 fontsize=13, fontweight="bold", color=NAVY, y=0.97)

    views = [
        ("Business View\n(Why?)",          "Actors · Goals · Decisions\nIndicators · Insights",   NAVY,   "#dce7f3"),
        ("Analytics Design View\n(What?)", "Analytics Goals · Algorithms\nSoftGoals · Trade-offs", BLUE,   "#e8f0fb"),
        ("Data Preparation View\n(How?)",  "Entities · Tasks · Operators\nData Flows · Pipelines", GREEN,  "#e8f5ec"),
    ]

    box_w = 0.26
    gap   = 0.04
    start_x = 0.04
    box_y = 0.18
    box_h = 0.60

    for i, (title, body, fc, bg) in enumerate(views):
        x = start_x + i * (box_w + gap)
        rect = FancyBboxPatch((x, box_y), box_w, box_h,
                              boxstyle="round,pad=0.02",
                              facecolor=bg, edgecolor=fc, linewidth=1.4)
        ax.add_patch(rect)
        ax.text(x + box_w / 2, box_y + box_h * 0.72, title,
                ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=fc,
                multialignment="center")
        ax.text(x + box_w / 2, box_y + box_h * 0.33, body,
                ha="center", va="center",
                fontsize=8, color="#444",
                multialignment="center")

    # Arrows
    for i in range(len(views) - 1):
        x_tip = start_x + (i + 1) * (box_w + gap)
        x_tail = x_tip - gap
        y_mid = box_y + box_h / 2
        ax.annotate("", xy=(x_tip, y_mid), xytext=(x_tail, y_mid),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.8))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = os.path.join(HERE, "fig_gr4ml_views.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {out}")


# ===========================================================================
# Figure 4 — Analytics View: Goal types and algorithm families
# ===========================================================================
def fig_analytics_view():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.axis("off")
    fig.patch.set_facecolor("white")
    fig.suptitle("Analytics Goal Types and Their Algorithm Families",
                 fontsize=13, fontweight="bold", color=NAVY, y=0.97)

    cols = [
        ("PredictionGoal",    "Forecast future\nor unknown value",
         "Logistic Regression\nRandom Forest\nXGBoost · Neural Nets",
         BLUE, "#e8f0fb"),
        ("DescriptionGoal",   "Understand or\nsummarise existing data",
         "K-Means Clustering\nPCA · t-SNE\nTopic Models (LDA)",
         GREEN, "#e8f5ec"),
        ("PrescriptionGoal",  "Recommend\noptimal action",
         "Reinforcement Learning\nBandit Algorithms\nLinear Optimisation",
         PURPLE, "#f0ebf9"),
    ]

    box_w = 0.28
    gap   = 0.03
    start_x = 0.03
    box_h = 0.70
    box_y = 0.12

    for i, (title, desc, algos, fc, bg) in enumerate(cols):
        x = start_x + i * (box_w + gap)
        rect = FancyBboxPatch((x, box_y), box_w, box_h,
                              boxstyle="round,pad=0.02",
                              facecolor=bg, edgecolor=fc, linewidth=1.4)
        ax.add_patch(rect)
        ax.text(x + box_w / 2, box_y + box_h * 0.88, title,
                ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=fc)
        ax.text(x + box_w / 2, box_y + box_h * 0.65, desc,
                ha="center", va="center",
                fontsize=8.5, color="#444", multialignment="center")
        ax.plot([x + 0.02, x + box_w - 0.02],
                [box_y + box_h * 0.52, box_y + box_h * 0.52],
                color=fc, lw=0.8, linestyle="--")
        ax.text(x + box_w / 2, box_y + box_h * 0.30, algos,
                ha="center", va="center",
                fontsize=8, color="#555", multialignment="center")

    # SoftGoal banner at bottom
    ax.text(0.5, 0.05, "SoftGoals narrow the choice within each family: interpretability · fairness · speed · cost",
            ha="center", va="center", fontsize=8.5, color=AMBER,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#fdf3e6", edgecolor=AMBER, lw=0.8))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = os.path.join(HERE, "fig_analytics_view.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {out}")


# ===========================================================================
# Figure 5 — Data Preparation Pipeline
# ===========================================================================
def fig_data_prep_pipeline():
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.axis("off")
    fig.patch.set_facecolor("white")
    fig.suptitle("Data Preparation Pipeline for Credit Risk Model",
                 fontsize=13, fontweight="bold", color=NAVY, y=0.97)

    steps_data = [
        ("Raw Data\n3 tables\n80 columns\n100K rows", NAVY, "#dce7f3"),
        ("Cleaning\nRemove/impute\nmissing values\n→ 96.8K rows", BLUE, "#e8f0fb"),
        ("Reduction\nDrop low-signal\ncolumns\n→ 58 cols", GREEN, "#e8f5ec"),
        ("Normalise\nMin-max scale\n3 numeric\nfeatures", AMBER, "#fdf3e6"),
        ("Encode\nOne-hot encode\ncategorical\n→ 70 features", PURPLE, "#f0ebf9"),
        ("Model\nInput\n97K rows\n70 features\n✓ Ready", RED, "#fdf0f1"),
    ]

    box_w = 0.13
    box_h = 0.62
    gap = 0.015
    start_x = 0.01
    box_y = 0.18

    for i, (label, fc, bg) in enumerate(steps_data):
        x = start_x + i * (box_w + gap)
        rect = FancyBboxPatch((x, box_y), box_w, box_h,
                              boxstyle="round,pad=0.015",
                              facecolor=bg, edgecolor=fc, linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + box_w / 2, box_y + box_h / 2, label,
                ha="center", va="center",
                fontsize=7.8, color=fc, fontweight="bold",
                multialignment="center")
        if i < len(steps_data) - 1:
            x_arrow = x + box_w + gap / 2
            ax.annotate("", xy=(x_arrow + 0.001, box_y + box_h / 2),
                        xytext=(x_arrow - 0.001, box_y + box_h / 2),
                        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = os.path.join(HERE, "fig_data_prep_pipeline.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {out}")


# ===========================================================================
# Figure 6 — Measures Hierarchy (Goal to Measure)
# ===========================================================================
def fig_measures_hierarchy():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axis("off")
    fig.patch.set_facecolor("white")
    fig.suptitle("Goal-to-Measure Hierarchy: Chatbot Usefulness Example",
                 fontsize=13, fontweight="bold", color=NAVY, y=0.97)

    # Root goal
    ax.text(0.5, 0.90, "Goal: Improve Chatbot Usefulness",
            ha="center", va="center", fontsize=11, fontweight="bold",
            color="white",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=NAVY, edgecolor="none"))

    measures = [
        ("Task success rate\n≥ 80 % of sessions", 0.12, GREEN),
        ("Satisfaction score\n≥ 4.0 stars (1–5)",  0.37, BLUE),
        ("Completion rate\n≥ 70 % of sessions",    0.62, AMBER),
        ("Escalation rate\n≤ 15 % (lower = better)", 0.87, PURPLE),
    ]

    for label, x, c in measures:
        ax.annotate("", xy=(x, 0.72), xytext=(0.5, 0.82),
                    arrowprops=dict(arrowstyle="->", color=c, lw=1.3))
        ax.text(x, 0.60, label, ha="center", va="center",
                fontsize=8.5, fontweight="bold", color=c, multialignment="center",
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                          edgecolor=c, lw=1.0))

    # Note at bottom
    ax.text(0.5, 0.18,
            "Model metric alone (AUC, F1) is not enough.\n"
            "Business measures must be tracked in production.",
            ha="center", va="center", fontsize=9, color=RED,
            multialignment="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fdf0f1",
                      edgecolor=RED, lw=0.8))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = os.path.join(HERE, "fig_measures_hierarchy.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {out}")


# ===========================================================================
# Figure 7 — Accuracy vs Precision (darts board analogy)
# ===========================================================================
def fig_accuracy_precision():
    fig, axes = plt.subplots(2, 2, figsize=(7, 7))
    fig.patch.set_facecolor("white")
    fig.suptitle("Accuracy vs Precision: The Darts Analogy",
                 fontsize=13, fontweight="bold", color=NAVY)

    titles = [
        ("Accurate AND Precise\n(ideal)", GREEN),
        ("Precise, NOT Accurate\n(systematic bias)", AMBER),
        ("Accurate, NOT Precise\n(high variance)", BLUE),
        ("Neither Accurate\nNOR Precise (worst)", RED),
    ]

    dart_configs = [
        # (cluster_cx, cluster_cy, scatter)
        (0.0, 0.0, 0.08),   # ideal: tight, on bullseye
        (0.5, 0.5, 0.07),   # precise but off-centre
        (0.0, 0.0, 0.28),   # accurate but scattered
        (0.4, -0.35, 0.30),  # neither
    ]

    rng = np.random.default_rng(42)

    for ax, (title, color), (cx, cy, sc) in zip(axes.flat, titles, dart_configs):
        # Draw concentric rings
        for r, alpha in [(0.9, 0.07), (0.65, 0.10), (0.45, 0.14),
                         (0.25, 0.18), (0.10, 0.25)]:
            circle = plt.Circle((0, 0), r, color="gray", fill=True,
                                 alpha=alpha, linewidth=0)
            ax.add_patch(circle)
            circle2 = plt.Circle((0, 0), r, color="gray", fill=False,
                                  linewidth=0.5, alpha=0.4)
            ax.add_patch(circle2)

        # Bullseye
        bull = plt.Circle((0, 0), 0.07, color=RED, fill=True, alpha=0.7)
        ax.add_patch(bull)

        # Darts
        xs = rng.normal(cx, sc, 7)
        ys = rng.normal(cy, sc, 7)
        ax.scatter(xs, ys, s=60, color=color, zorder=5,
                   edgecolors="white", linewidths=0.8)

        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=9, fontweight="bold", color=color,
                     multialignment="center")

    plt.tight_layout()
    out = os.path.join(HERE, "fig_accuracy_precision.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {out}")


# ===========================================================================
# Figure 8 — Business View Chain Diagram
# ===========================================================================
def fig_business_view_chain():
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.axis("off")
    fig.patch.set_facecolor("white")
    fig.suptitle("GR4ML Business View: Credit Risk Prediction Chain",
                 fontsize=13, fontweight="bold", color=NAVY, y=0.97)

    chain = [
        ("StrategicGoal\n\nMake good\nlending decisions", NAVY, "#dce7f3"),
        ("DecisionGoal\n\nApprove or reject\nthis loan", BLUE, "#e8f0fb"),
        ("QuestionGoal\n\nWhat is the\ncredit risk?", GREEN, "#e8f5ec"),
        ("Insight\n\nRisk score: 0.73\n(high risk)", AMBER, "#fdf3e6"),
        ("Indicator\n\nDefault rate (%)\ntracked monthly", PURPLE, "#f0ebf9"),
    ]

    box_w = 0.16
    box_h = 0.60
    gap = 0.02
    start_x = 0.02
    box_y = 0.20

    for i, (label, fc, bg) in enumerate(chain):
        x = start_x + i * (box_w + gap)
        rect = FancyBboxPatch((x, box_y), box_w, box_h,
                              boxstyle="round,pad=0.015",
                              facecolor=bg, edgecolor=fc, linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + box_w / 2, box_y + box_h / 2, label,
                ha="center", va="center",
                fontsize=7.8, color=fc, fontweight="bold",
                multialignment="center")
        if i < len(chain) - 1:
            x_arrow = x + box_w + gap / 2
            ax.annotate("", xy=(x_arrow + 0.005, box_y + box_h / 2),
                        xytext=(x_arrow - 0.005, box_y + box_h / 2),
                        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))

    # Actor annotation
    ax.text(0.02 + box_w / 2, 0.10, "Actor:\nCase Worker",
            ha="center", va="center", fontsize=7.5, color=NAVY,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#dce7f3", edgecolor=NAVY, lw=0.8))
    ax.annotate("", xy=(0.02 + box_w / 2, box_y),
                xytext=(0.02 + box_w / 2, 0.17),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.0, linestyle="dashed"))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = os.path.join(HERE, "fig_business_view_chain.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Saved: {out}")


if __name__ == "__main__":
    print("Generating Session 3 figures...")
    fig_when_to_use_ml()
    fig_goal_hierarchy()
    fig_gr4ml_views()
    fig_analytics_view()
    fig_data_prep_pipeline()
    fig_measures_hierarchy()
    fig_accuracy_precision()
    fig_business_view_chain()
    print("All figures done.")
