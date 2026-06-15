"""
Figures for SEML Session 4 – Quality Attributes & Architecture
Run from the session4-architecture folder or via build_pdf.py.
"""
import os, sys

# Find figstyle in the make-lecture-kit scripts folder
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = "/Users/jayakrishnanj/mtech/.claude/skills/make-lecture-kit"
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
# Also try relative paths as fallback
for up in ("../../../.claude/skills/make-lecture-kit/scripts",
           "../../../../.claude/skills/make-lecture-kit/scripts",
           "../../../scripts", "../../scripts"):
    p = os.path.normpath(os.path.join(HERE, up))
    if os.path.isdir(p):
        sys.path.insert(0, p)
        break

import figstyle as F
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ------------------------------------------------------------------
# Figure 1: QA Spider / Comparison bars for Flipkart vs Hotstar
# ------------------------------------------------------------------
labels = ["Performance", "Scalability", "Availability", "Fault\nTolerance", "Monitoring"]
flipkart = [2, 1, 2, 1, 1]   # scores 1-5
hotstar  = [5, 5, 5, 4, 5]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 4))
F.use_house_style()
bars1 = ax.bar(x - width/2, flipkart, width, label="Flipkart 2014",
               color="#B23A48", alpha=0.85, edgecolor="white", linewidth=0.5)
bars2 = ax.bar(x + width/2, hotstar, width, label="Hotstar 2019",
               color="#2E7D52", alpha=0.85, edgecolor="white", linewidth=0.5)
ax.set_ylim(0, 6)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel("Readiness (1=low, 5=high)", fontsize=9)
ax.set_title("QA Readiness: Flipkart 2014 vs Hotstar 2019",
             fontsize=11, fontweight="bold", color="#21355E")
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
for bar in bars2:
    ax.annotate(f'{bar.get_height()}',
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 2), textcoords="offset points",
                ha='center', va='bottom', fontsize=8, color="#2E7D52")
plt.tight_layout()
out1 = os.path.join(HERE, "fig_qa_comparison.png")
plt.savefig(out1, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved {out1}")

# ------------------------------------------------------------------
# Figure 2: SMART QA attributes radial diagram (bar chart version)
# ------------------------------------------------------------------
smart_labels = ["Specific", "Measurable", "Attainable", "Relevant", "Time-sensitive"]
good_qa   = [5, 5, 4, 5, 5]   # SMART QA
vague_qa  = [1, 1, 3, 2, 1]   # Vague "the system should be fast"

x2 = np.arange(len(smart_labels))
fig2, ax2 = plt.subplots(figsize=(8, 4))
F.use_house_style()
ax2.bar(x2 - 0.2, vague_qa, 0.35, label='Vague QA (not SMART)',
        color="#B23A48", alpha=0.8)
ax2.bar(x2 + 0.2, good_qa, 0.35, label='SMART QA',
        color="#2C5AA0", alpha=0.8)
ax2.set_ylim(0, 6)
ax2.set_xticks(x2)
ax2.set_xticklabels(smart_labels, fontsize=9)
ax2.set_ylabel("Score (1=poor, 5=excellent)", fontsize=9)
ax2.set_title("A SMART Quality Attribute vs a Vague One",
             fontsize=11, fontweight="bold", color="#21355E")
ax2.legend(fontsize=9)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
plt.tight_layout()
out2 = os.path.join(HERE, "fig_smart_qa.png")
plt.savefig(out2, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved {out2}")

# ------------------------------------------------------------------
# Figure 3: ML-specific QAs – horizontal bar chart
# ------------------------------------------------------------------
ml_qas = ["Reproducibility", "Model Drift\nMonitoring", "Data Drift\nAdaptability",
          "Fairness", "Security &\nPrivacy", "Maintainability",
          "Robustness", "Explainability", "Reliability",
          "Scalability", "Accuracy"]
importance = [3, 4, 4, 4, 5, 4, 5, 4, 5, 5, 5]
colors_ml = ["#6A4C93" if v >= 5 else "#2C5AA0" if v >= 4 else "#8A5A1E"
             for v in importance]

fig3, ax3 = plt.subplots(figsize=(8, 5))
F.use_house_style()
y3 = np.arange(len(ml_qas))
ax3.barh(y3, importance, color=colors_ml, alpha=0.85, edgecolor="white")
ax3.set_yticks(y3)
ax3.set_yticklabels(ml_qas, fontsize=8)
ax3.set_xlim(0, 6)
ax3.set_xlabel("Typical importance in production ML (1=low, 5=critical)", fontsize=8)
ax3.set_title("Quality Attributes Specific to ML Systems",
              fontsize=11, fontweight="bold", color="#21355E")
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
legend_patches = [
    mpatches.Patch(color="#6A4C93", alpha=0.85, label="Critical (5)"),
    mpatches.Patch(color="#2C5AA0", alpha=0.85, label="Important (4)"),
    mpatches.Patch(color="#8A5A1E", alpha=0.85, label="Notable (3)"),
]
ax3.legend(handles=legend_patches, fontsize=8, loc="lower right")
plt.tight_layout()
out3 = os.path.join(HERE, "fig_ml_qas.png")
plt.savefig(out3, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved {out3}")

# ------------------------------------------------------------------
# Figure 4: System Architecture layers (horizontal flow)
# ------------------------------------------------------------------
fig4, ax4 = plt.subplots(figsize=(10, 3.5))
F.use_house_style()
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 3.5)
ax4.axis("off")
ax4.set_title("System Architecture: Five Layers Working Together",
              fontsize=11, fontweight="bold", color="#21355E")

layers = [
    ("Hardware\n& Network", "#21355E"),
    ("Infrastructure\n(Cloud/K8s)", "#2C5AA0"),
    ("Software\nComponents", "#2E7D52"),
    ("ML\nComponents", "#8A5A1E"),
    ("Data\nComponents", "#6A4C93"),
]
box_w, box_h = 1.6, 1.4
gap = 0.35
start_x = 0.4
y_center = 1.5

for i, (label, color) in enumerate(layers):
    x = start_x + i * (box_w + gap)
    rect = mpatches.FancyBboxPatch((x, y_center - box_h/2), box_w, box_h,
                                    boxstyle="round,pad=0.08",
                                    facecolor=color, edgecolor="white",
                                    linewidth=1.5, alpha=0.9)
    ax4.add_patch(rect)
    ax4.text(x + box_w/2, y_center, label, ha="center", va="center",
             fontsize=8.5, fontweight="bold", color="white",
             multialignment="center")
    # Arrow between boxes
    if i < len(layers) - 1:
        ax_x = x + box_w + 0.02
        ax4.annotate("", xy=(ax_x + gap - 0.04, y_center),
                     xytext=(ax_x, y_center),
                     arrowprops=dict(arrowstyle="->", color="#21355E",
                                     lw=1.5))

plt.tight_layout()
out4 = os.path.join(HERE, "fig_arch_layers.png")
plt.savefig(out4, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved {out4}")

# ------------------------------------------------------------------
# Figure 5: Pipe-and-Filter NLP pipeline diagram
# ------------------------------------------------------------------
fig5, ax5 = plt.subplots(figsize=(10, 3.2))
F.use_house_style()
ax5.set_xlim(0, 10)
ax5.set_ylim(0, 3.2)
ax5.axis("off")
ax5.set_title("Pipe-and-Filter: NLP Sentiment Pipeline",
              fontsize=11, fontweight="bold", color="#21355E")

filters = [
    ("Data\nSource\n(raw text)", "#21355E"),
    ("Filter 1\nTokenise", "#2C5AA0"),
    ("Filter 2\nStopword\nRemoval", "#2C5AA0"),
    ("Filter 3\nVectorise\n(BoW/TF-IDF)", "#2C5AA0"),
    ("Filter 4\nModel\nInference", "#2E7D52"),
    ("Data\nSink\n(prediction)", "#6A4C93"),
]
box_w2, box_h2 = 1.35, 1.6
gap2 = 0.18
start_x2 = 0.15
y2 = 1.4

for i, (label, color) in enumerate(filters):
    x = start_x2 + i * (box_w2 + gap2)
    rect = mpatches.FancyBboxPatch((x, y2 - box_h2/2), box_w2, box_h2,
                                    boxstyle="round,pad=0.07",
                                    facecolor=color, edgecolor="white",
                                    linewidth=1.5, alpha=0.88)
    ax5.add_patch(rect)
    ax5.text(x + box_w2/2, y2, label, ha="center", va="center",
             fontsize=7.5, fontweight="bold", color="white",
             multialignment="center")
    if i < len(filters) - 1:
        arrow_x = x + box_w2 + 0.01
        ax5.annotate("", xy=(arrow_x + gap2 - 0.03, y2),
                     xytext=(arrow_x, y2),
                     arrowprops=dict(arrowstyle="->", color="#21355E", lw=1.5))
    # Pipe label
    if 0 < i < len(filters) - 1:
        ax5.text(x + box_w2/2, y2 - box_h2/2 - 0.22,
                 "pipe", ha="center", fontsize=6.5, color="#6B7280",
                 style="italic")

plt.tight_layout()
out5 = os.path.join(HERE, "fig_pipe_filter.png")
plt.savefig(out5, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved {out5}")

print("All figures done.")
