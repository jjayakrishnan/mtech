#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure scripts for SEML Session 5: CQRS, RAG, Monolith & Microservices.

Run by build_pdf.py from the figures/ directory.
Each call saves a PNG to the figures/ folder.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Find the skill's scripts/ directory (two levels up from figures/)
for up in ("../../../.claude/skills/make-lecture-kit/scripts",
           "../../../../.claude/skills/make-lecture-kit/scripts",
           "../../../../../.claude/skills/make-lecture-kit/scripts",
           "../../../../../../.claude/skills/make-lecture-kit/scripts"):
    p = os.path.normpath(os.path.join(HERE, up))
    if os.path.isdir(p):
        sys.path.insert(0, p)
        break

# Also try relative: scripts/ is 3 levels above session5-patterns/figures/
# Path: mtech/.claude/skills/make-lecture-kit/scripts
for candidate in [
    os.path.normpath(os.path.join(HERE, "../../../../.claude/skills/make-lecture-kit/scripts")),
    os.path.normpath(os.path.join(HERE, "../../../../../.claude/skills/make-lecture-kit/scripts")),
]:
    if os.path.isdir(candidate) and candidate not in sys.path:
        sys.path.insert(0, candidate)

import figstyle as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------------------------------------------------------------------------
# Figure 1: CQRS split — commands vs queries
# A bar chart showing that commands change state and queries read state.
# ---------------------------------------------------------------------------
F.bars(
    labels=["GET\n(query)", "POST\n(command)", "PUT\n(command)", "DELETE\n(command)"],
    values=[0, 1, 1, 1],
    title="CQRS: queries only read, commands only write",
    ylabel="Changes state? (1=yes, 0=no)",
    colors=[F.PALETTE["blue"], F.PALETTE["red"], F.PALETTE["amber"], F.PALETTE["purple"]],
    annotate=False,
    fmt="{:.0f}",
    out=os.path.join(HERE, "fig_cqrs_http.png"),
)

# ---------------------------------------------------------------------------
# Figure 2: CQRS architecture flow — write store vs read store
# A flow diagram showing the separation of command and query sides.
# ---------------------------------------------------------------------------
F.use_house_style()
fig, ax = plt.subplots(figsize=(7.0, 3.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis("off")

def box(ax, x, y, w, h, text, color, tcolor="white"):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.05",
        fc=color, ec=F.PALETTE["ink"], lw=1.2, zorder=3))
    ax.text(x, y, text, ha="center", va="center",
            fontsize=9.0, color=tcolor, fontweight="bold", zorder=4,
            wrap=True)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=F.PALETTE["muted"], lw=1.5))

# Client
box(ax, 1.0, 1.5, 1.4, 0.6, "Client", F.PALETTE["ink"])

# Command side
box(ax, 3.2, 2.2, 1.5, 0.5, "Command\n(write)", F.PALETTE["red"], "white")
box(ax, 5.5, 2.2, 1.5, 0.5, "Write\nStore", F.PALETTE["amber"], "white")

# Query side
box(ax, 3.2, 0.8, 1.5, 0.5, "Query\n(read)", F.PALETTE["blue"], "white")
box(ax, 5.5, 0.8, 1.5, 0.5, "Read\nStore", F.PALETTE["green"], "white")

# Sync
box(ax, 7.8, 1.5, 1.2, 0.5, "Sync /\nEvents", F.PALETTE["purple"], "white")

# Arrows
arrow(ax, 1.7, 1.8, 2.45, 2.2)  # client -> command
arrow(ax, 1.7, 1.2, 2.45, 0.8)  # client -> query
arrow(ax, 3.95, 2.2, 4.75, 2.2) # command -> write store
arrow(ax, 3.95, 0.8, 4.75, 0.8) # query -> read store
arrow(ax, 6.25, 2.0, 7.2, 1.7)  # write store -> sync
arrow(ax, 7.2, 1.3, 6.25, 1.0)  # sync -> read store

ax.set_title("CQRS: write and read stores are kept separate",
             color=F.PALETTE["ink"], fontweight="bold", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_cqrs_arch.png"))
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 3: Eventual Consistency timeline
# Shows a timeline of a model rollout reaching different regions at different times.
# ---------------------------------------------------------------------------
F.use_house_style()
fig, ax = plt.subplots(figsize=(7.0, 2.8))
ax.set_xlim(-0.2, 6.5)
ax.set_ylim(-0.5, 4.5)
ax.axis("off")

regions = ["Central registry", "US-East servers", "EU servers", "Asia-Pacific", "Edge caches"]
times   = [0.0, 0.5, 1.2, 2.0, 3.5]
colors  = [F.PALETTE["green"], F.PALETTE["blue"], F.PALETTE["blue"],
           F.PALETTE["amber"], F.PALETTE["red"]]

# Time axis
ax.annotate("", xy=(6.3, -0.3), xytext=(-0.1, -0.3),
            arrowprops=dict(arrowstyle="-|>", color=F.PALETTE["ink"], lw=1.5))
ax.text(3.1, -0.48, "Time after model release", ha="center", va="top",
        fontsize=9.5, color=F.PALETTE["muted"])

for i, (region, t, col) in enumerate(zip(regions, times, colors)):
    y = i * 0.75 + 0.2
    ax.plot([t, 6.2], [y, y], color=col, lw=1.5, ls="--", alpha=0.5)
    ax.scatter([t], [y], color=col, s=80, zorder=5)
    ax.text(t + 0.1, y + 0.12, f"+{t:.1f} min", fontsize=8.5,
            color=F.PALETTE["ink"], fontweight="bold")
    ax.text(-0.1, y, region, ha="right", va="center",
            fontsize=9.0, color=F.PALETTE["ink"])

ax.set_title("Eventual consistency: each region updates at a different time",
             color=F.PALETTE["ink"], fontweight="bold", fontsize=10.5)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_eventual_consistency.png"))
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 4: RAG pipeline — ingestion side and query side
# Two vertical flow diagrams side by side.
# ---------------------------------------------------------------------------
F.use_house_style()
fig, axes = plt.subplots(1, 2, figsize=(7.0, 4.0))

ingestion_steps = ["Documents", "Extraction", "Chunking",
                   "Embedding\nGeneration", "Indexing", "Vector Store"]
query_steps = ["User Query", "Query\nEmbedding", "Semantic\nSearch",
               "Context\nRetrieval", "LLM Prompt\nConstruction", "Answer\nGeneration"]

for ax_i, (steps, title, col) in enumerate([
    (ingestion_steps, "Ingestion pipeline\n(command / write side)", F.PALETTE["amber"]),
    (query_steps,     "Query pipeline\n(query / read side)",         F.PALETTE["blue"]),
]):
    ax_s = axes[ax_i]
    ax_s.set_xlim(0, 1)
    ax_s.set_ylim(0, 1)
    ax_s.axis("off")
    ax_s.set_title(title, color=F.PALETTE["ink"], fontweight="bold", fontsize=9.5)
    k = len(steps)
    slot = 0.92 / k
    for i, s in enumerate(steps):
        cy = 0.96 - slot * (i + 0.5)
        ax_s.add_patch(mpatches.FancyBboxPatch(
            (0.1, cy - slot*0.30), 0.80, slot*0.60,
            boxstyle="round,pad=0.01",
            fc=F.PALETTE["fill"], ec=col, lw=1.4, zorder=3))
        ax_s.text(0.5, cy, s, ha="center", va="center",
                  fontsize=8.5, color=F.PALETTE["ink"], zorder=4)
        if i < k - 1:
            ax_s.annotate("",
                xy=(0.5, cy - slot*0.31),
                xytext=(0.5, cy - slot*0.30 + 0.001),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.3))

fig.suptitle("RAG maps onto two CQRS pipelines",
             color=F.PALETTE["ink"], fontweight="bold", fontsize=11, y=1.01)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_rag_pipeline.png"), bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 5: Embedding types comparison — qualitative feature chart
# ---------------------------------------------------------------------------
import numpy as np

embedding_types = ["GloVe", "BERT", "Sentence-BERT", "DPR", "OpenAI"]
# Features scored 0-3: contextual, semantic, retrieval-optimised, sentence-level
contextual  = [0, 3, 3, 3, 3]
semantic    = [2, 3, 3, 2, 3]
retrieval   = [1, 2, 2, 3, 2]
sentence_lv = [0, 1, 3, 2, 3]

x = np.arange(len(embedding_types))
width = 0.2

F.use_house_style()
fig, ax = plt.subplots(figsize=(7.0, 3.4))
ax.bar(x - 1.5*width, contextual,  width, label="Contextual",         color=F.PALETTE["blue"])
ax.bar(x - 0.5*width, semantic,    width, label="Semantic",            color=F.PALETTE["green"])
ax.bar(x + 0.5*width, retrieval,   width, label="Retrieval-optimised", color=F.PALETTE["amber"])
ax.bar(x + 1.5*width, sentence_lv, width, label="Sentence-level",      color=F.PALETTE["purple"])

ax.set_xticks(x)
ax.set_xticklabels(embedding_types, fontsize=9.5)
ax.set_ylabel("Score (0=none, 3=strong)")
ax.legend(loc="upper left", fontsize=8.5)
ax.set_title("Embedding types: key strengths at a glance",
             color=F.PALETTE["ink"], fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_embedding_types.png"))
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 6: ChromaDB internals — collection structure
# ---------------------------------------------------------------------------
F.flow(
    ["Document\nText", "Chunking", "Embedding\n(vector)", "ChromaDB\nCollection",
     "SQLite\n(storage)", "HNSW\nIndex"],
    "ChromaDB stores text in SQLite and embeddings in an HNSW index",
    direction="lr",
    color=F.PALETTE["purple"],
    out=os.path.join(HERE, "fig_chromadb_flow.png"),
)

# ---------------------------------------------------------------------------
# Figure 7: Monolith vs Microservices — deployment comparison
# ---------------------------------------------------------------------------
F.use_house_style()
fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))

mono_components = ["UI", "Auth", "Orders", "Payments", "Notifications", "DB"]
micro_components = ["UI\nService", "Auth\nService", "Order\nService",
                    "Payment\nService", "Notify\nService", "Shared\nDB"]

for ax_i, (comps, title, col, grouped) in enumerate([
    (mono_components,  "Monolith: one deployment unit", F.PALETTE["amber"], True),
    (micro_components, "Microservices: independent units", F.PALETTE["blue"], False),
]):
    ax_s = axes[ax_i]
    ax_s.set_xlim(0, 1)
    ax_s.set_ylim(0, 1)
    ax_s.axis("off")
    ax_s.set_title(title, color=F.PALETTE["ink"], fontweight="bold", fontsize=9.5)

    if grouped:
        # Draw a big outer box
        ax_s.add_patch(mpatches.FancyBboxPatch(
            (0.05, 0.05), 0.90, 0.88,
            boxstyle="round,pad=0.02",
            fc=col + "22", ec=col, lw=2.0, zorder=1))
        ax_s.text(0.5, 0.95, "Single WAR/deployment", ha="center", va="top",
                  fontsize=8.0, color=col, style="italic")
        # mini boxes inside
        positions = [(0.25, 0.73), (0.75, 0.73),
                     (0.25, 0.50), (0.75, 0.50),
                     (0.25, 0.27), (0.75, 0.27)]
        for (cx, cy), label in zip(positions, comps):
            ax_s.add_patch(mpatches.FancyBboxPatch(
                (cx-0.18, cy-0.10), 0.36, 0.20,
                boxstyle="round,pad=0.01",
                fc="white", ec=col, lw=1.2, zorder=3))
            ax_s.text(cx, cy, label, ha="center", va="center",
                      fontsize=8.5, color=F.PALETTE["ink"], zorder=4)
    else:
        # Separate boxes (each its own island)
        positions = [(0.25, 0.73), (0.75, 0.73),
                     (0.25, 0.50), (0.75, 0.50),
                     (0.25, 0.27), (0.75, 0.27)]
        for (cx, cy), label in zip(positions, comps):
            ax_s.add_patch(mpatches.FancyBboxPatch(
                (cx-0.18, cy-0.10), 0.36, 0.20,
                boxstyle="round,pad=0.01",
                fc=F.PALETTE["fill"], ec=col, lw=1.5, zorder=3))
            ax_s.text(cx, cy, label, ha="center", va="center",
                      fontsize=8.0, color=F.PALETTE["ink"], zorder=4)

fig.suptitle("Monolith packs everything together; microservices split it apart",
             color=F.PALETTE["ink"], fontweight="bold", fontsize=10, y=1.01)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_mono_vs_micro.png"), bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 8: Microservices ML demo — 3-service system
# ---------------------------------------------------------------------------
F.flow(
    ["Client\nRequest", "Gateway\n:8000\n(routing)", "Model Service\n:8001\n(inference)",
     "Logging Service\n:8002\n(observability)"],
    "Three-service ML system: each service has one job",
    direction="lr",
    color=F.PALETTE["green"],
    out=os.path.join(HERE, "fig_microservices_ml.png"),
)

print("All figures written to:", HERE)
