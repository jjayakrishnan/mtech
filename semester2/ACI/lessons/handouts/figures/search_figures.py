"""
ACI Session 2 — Intelligent Agents & Environments
Figure script for search-algorithms.tex companion
Run from the make-lecture-kit root so figstyle is importable.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for up in ("../../../.claude/skills/make-lecture-kit/scripts",
           "../../../../.claude/skills/make-lecture-kit/scripts",
           "../../../../../.claude/skills/make-lecture-kit/scripts"):
    p = os.path.normpath(os.path.join(HERE, up))
    if os.path.isdir(p):
        sys.path.insert(0, p)
        break

# Also try the known absolute path
known = "/Users/jayakrishnanj/mtech/.claude/skills/make-lecture-kit/scripts"
if os.path.isdir(known) and known not in sys.path:
    sys.path.insert(0, known)

import figstyle as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# ---------------------------------------------------------------------------
# Figure 1 — PEAS comparison table (bar chart of PEAS dimensions)
# Shows three worked examples side-by-side: medical diagnosis, part-picking
# robot, taxi driver — mapped to their environment properties
# ---------------------------------------------------------------------------
def fig_env_properties():
    """
    A grouped bar / comparison figure showing environment property values
    for three task environments from the lecture table (slide 13).
    Encoded as numeric scores: 1 = first option, 0 = second option.
    """
    import matplotlib.ticker as ticker

    tasks    = ["Crossword\npuzzle", "Chess\n(clock)", "Poker", "Taxi\ndriving",
                "Medical\ndiagnosis", "Image\nanalysis"]
    # Encode: Observable 1=Fully, 0=Partially
    obs    = [1, 1, 0, 0, 0, 1]
    determ = [1, 1, 0, 0, 0, 1]   # 1=Deterministic, 0=Stochastic
    epis   = [0, 0, 0, 0, 0, 1]   # 1=Episodic, 0=Sequential
    static = [1, 0, 1, 0, 0, 0]   # 1=Static, 0=Dynamic/Semi

    x = np.arange(len(tasks))
    w = 0.18
    fig, ax = plt.subplots(figsize=(10, 4.2))
    F.use_house_style()

    palette_keys = ["blue", "green", "amber", "red"]
    colors = [F.PALETTE[k] for k in palette_keys]
    bars = [
        ax.bar(x - 1.5*w, obs,    w, label="Observable\n(1=Full, 0=Partial)", color=colors[0], alpha=0.85),
        ax.bar(x - 0.5*w, determ, w, label="Deterministic\n(1=Det, 0=Stoch)",  color=colors[1], alpha=0.85),
        ax.bar(x + 0.5*w, epis,   w, label="Episodic\n(1=Epis, 0=Seq)",        color=colors[2], alpha=0.85),
        ax.bar(x + 1.5*w, static, w, label="Static\n(1=Static, 0=Dynamic)",    color=colors[3], alpha=0.85),
    ]

    ax.set_xticks(x)
    ax.set_xticklabels(tasks, fontsize=8)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["No / 2nd option", "Yes / 1st option"], fontsize=8)
    ax.set_ylim(-0.15, 1.4)
    ax.legend(loc="upper right", fontsize=7, ncol=2)
    ax.set_title("Environment Properties for Six Task Environments\n"
                 "Each bar answers: does this environment have the first option for that property?",
                 fontweight="bold", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out = os.path.join(HERE, "fig_env_properties.png")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


# ---------------------------------------------------------------------------
# Figure 2 — Agent architecture ladder (flow diagram)
# Simple Reflex -> Model-based -> Goal-based -> Utility -> Learning
# ---------------------------------------------------------------------------
def fig_agent_ladder():
    F.flow(
        ["Simple Reflex Agent\n(reacts to current percept)",
         "Model-Based Agent\n(keeps internal state)",
         "Goal-Based Agent\n(considers future states)",
         "Utility-Based Agent\n(maximises happiness score)",
         "Learning Agent\n(improves over time)"],
        title="Five Agent Architectures — each step adds one new capability",
        out=os.path.join(HERE, "fig_agent_ladder.png")
    )
    print(f"Saved fig_agent_ladder.png")


# ---------------------------------------------------------------------------
# Figure 3 — Problem formulation components (flow / labelled boxes)
# ---------------------------------------------------------------------------
def fig_problem_formulation():
    F.flow(
        ["Initial State\n(where we start — e.g. In(Arad))",
         "Possible Actions\n(what we can do from each state)",
         "Transition Model\n(RESULT(s, a) — where action takes us)",
         "Goal Test\n(IsGoal(s)? — are we done?)",
         "Path Cost\n(cost(s, a) — how expensive is this path?)"],
        title="Five Components of a Problem Formulation\nEvery search problem is fully described by these five pieces",
        out=os.path.join(HERE, "fig_problem_formulation.png")
    )
    print(f"Saved fig_problem_formulation.png")


# ---------------------------------------------------------------------------
# Figure 4 — Search strategy taxonomy (comparison bar)
# Two categories: Uninformed vs Informed, with sub-algorithms
# ---------------------------------------------------------------------------
def fig_search_taxonomy():
    """
    A simple horizontal comparison figure showing the two search families
    and their member algorithms.
    """
    fig, ax = plt.subplots(figsize=(9, 3.5))
    F.use_house_style()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    # Uninformed box
    uninf_box = mpatches.FancyBboxPatch((0.3, 0.4), 4.0, 3.2,
        boxstyle="round,pad=0.15", linewidth=1.5,
        edgecolor="#B23A48", facecolor="#FBF1F2")
    ax.add_patch(uninf_box)
    ax.text(2.3, 3.35, "Uninformed (Blind)", fontsize=10,
            fontweight="bold", color="#B23A48", ha="center")
    uninf_algs = ["BFS — shallowest node first (FIFO)",
                  "DFS — deepest node first (LIFO)",
                  "UCS — cheapest node first (priority queue)",
                  "IDS — depth-limited + iterative deepening",
                  "Bi-directional search"]
    for i, txt in enumerate(uninf_algs):
        ax.text(0.55, 2.85 - i*0.52, f"• {txt}", fontsize=8.2, color="#1A202C")

    # Informed box
    inf_box = mpatches.FancyBboxPatch((5.5, 0.4), 4.1, 3.2,
        boxstyle="round,pad=0.15", linewidth=1.5,
        edgecolor="#2C5AA0", facecolor="#F4F7FC")
    ax.add_patch(inf_box)
    ax.text(7.55, 3.35, "Informed (Heuristic)", fontsize=10,
            fontweight="bold", color="#2C5AA0", ha="center")
    inf_algs = ["Best-First Search — uses h(n) only",
                "A* — uses f(n) = g(n) + h(n)",
                "AO* — AND-OR graphs"]
    for i, txt in enumerate(inf_algs):
        ax.text(5.72, 2.85 - i*0.52, f"• {txt}", fontsize=8.2, color="#1A202C")

    # Arrow between them
    ax.annotate("", xy=(5.4, 2.0), xytext=(4.4, 2.0),
                arrowprops=dict(arrowstyle="->", color="#6B7280", lw=1.5))
    ax.text(4.9, 2.15, "add\nheuristic", fontsize=7.5, ha="center", color="#6B7280")

    ax.set_title("Search Strategy Taxonomy\n"
                 "Uninformed strategies explore blindly; informed strategies use domain knowledge (a heuristic)",
                 fontweight="bold", fontsize=9, pad=6)

    out = os.path.join(HERE, "fig_search_taxonomy.png")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


# ---------------------------------------------------------------------------
# Figure 5 — Vacuum world state space (8 states)
# 2 locations × 2 dirt states × 2 agent positions = 8 states
# ---------------------------------------------------------------------------
def fig_vacuum_states():
    """
    Shows the 8 possible states of the vacuum world as a grid.
    Each cell: agent position (A or B), dirt in A (d/c), dirt in B (d/c).
    """
    fig, axes = plt.subplots(2, 4, figsize=(9, 4.0))
    F.use_house_style()

    # State = (agent_pos, dirt_A, dirt_B)  0=clean, 1=dirty
    states = [
        ("A", 1, 1, "State 1\nA-dirty, B-dirty\nAgent at A"),
        ("B", 1, 1, "State 2\nA-dirty, B-dirty\nAgent at B"),
        ("A", 0, 1, "State 3\nA-clean, B-dirty\nAgent at A"),
        ("B", 0, 1, "State 4\nA-clean, B-dirty\nAgent at B"),
        ("A", 1, 0, "State 5\nA-dirty, B-clean\nAgent at A"),
        ("B", 1, 0, "State 6\nA-dirty, B-clean\nAgent at B"),
        ("A", 0, 0, "State 7\nA-clean, B-clean\nAgent at A\n(GOAL)"),
        ("B", 0, 0, "State 8\nA-clean, B-clean\nAgent at B\n(GOAL)"),
    ]

    for idx, (agent, dA, dB, label) in enumerate(states):
        row, col = divmod(idx, 4)
        ax = axes[row][col]
        ax.set_xlim(0, 2)
        ax.set_ylim(0, 1)
        ax.axis("off")

        # Draw two cells
        for cx in [0, 1]:
            color = "#FBF1F2" if (cx == 0 and dA) or (cx == 1 and dB) else "#F1F8F3"
            rect = mpatches.FancyBboxPatch((cx + 0.05, 0.1), 0.85, 0.75,
                boxstyle="round,pad=0.03", linewidth=1,
                edgecolor="#6B7280", facecolor=color)
            ax.add_patch(rect)
            cell_label = "A" if cx == 0 else "B"
            ax.text(cx + 0.47, 0.75, cell_label, ha="center", va="center",
                    fontsize=7, color="#6B7280")
            # Show dirt
            if (cx == 0 and dA) or (cx == 1 and dB):
                ax.text(cx + 0.47, 0.42, "dirt", ha="center", va="center",
                        fontsize=6.5, color="#B23A48", style="italic")

        # Agent
        ag_x = 0.47 if agent == "A" else 1.47
        ax.text(ag_x, 0.25, "V", ha="center", va="center", fontsize=10,
                fontweight="bold", color="#2C5AA0")

        is_goal = (dA == 0 and dB == 0)
        bg = "#F4F0F9" if is_goal else "white"
        ax.set_facecolor(bg)
        ax.text(1.0, -0.05, label, ha="center", va="top", fontsize=6.0,
                color="#2E7D52" if is_goal else "#1A202C",
                fontweight="bold" if is_goal else "normal")

    fig.suptitle("Vacuum World: all 8 possible states  (V = vacuum agent, red = dirty cell, green border = goal)",
                 fontweight="bold", fontsize=8.5, y=1.01)
    out = os.path.join(HERE, "fig_vacuum_states.png")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


# ---------------------------------------------------------------------------
# Figure 6 — PEAS structure: four boxes around a central "Agent" node
# ---------------------------------------------------------------------------
def fig_peas_structure():
    """
    Shows the four PEAS components as boxes feeding into/from the Agent box.
    Performance and Environment surround the agent conceptually.
    Actuators are outputs; Sensors are inputs.
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    F.use_house_style()
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)
    ax.axis("off")

    # Central agent box
    agent_box = mpatches.FancyBboxPatch((3.1, 1.4), 1.8, 1.2,
        boxstyle="round,pad=0.1", linewidth=1.5,
        edgecolor="#21355E", facecolor="#F4F7FC")
    ax.add_patch(agent_box)
    ax.text(4.0, 2.0, "Agent", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#21355E")

    # Sensors box (left — input)
    sens_box = mpatches.FancyBboxPatch((0.2, 1.4), 2.0, 1.2,
        boxstyle="round,pad=0.1", linewidth=1.2,
        edgecolor="#2C5AA0", facecolor="#EBF0FA")
    ax.add_patch(sens_box)
    ax.text(1.2, 2.15, "Sensors", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="#2C5AA0")
    ax.text(1.2, 1.78, "(inputs: camera,\nkeyboard, GPS)", ha="center",
            va="center", fontsize=7.5, color="#1A202C")
    ax.annotate("", xy=(3.1, 2.0), xytext=(2.2, 2.0),
                arrowprops=dict(arrowstyle="->", color="#2C5AA0", lw=1.5))
    ax.text(2.65, 2.1, "percepts", ha="center", fontsize=7, color="#2C5AA0")

    # Actuators box (right — output)
    act_box = mpatches.FancyBboxPatch((5.8, 1.4), 2.0, 1.2,
        boxstyle="round,pad=0.1", linewidth=1.2,
        edgecolor="#2E7D52", facecolor="#EBF5EF")
    ax.add_patch(act_box)
    ax.text(6.8, 2.15, "Actuators", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="#2E7D52")
    ax.text(6.8, 1.78, "(outputs: screen,\narm, wheels)", ha="center",
            va="center", fontsize=7.5, color="#1A202C")
    ax.annotate("", xy=(5.8, 2.0), xytext=(4.9, 2.0),
                arrowprops=dict(arrowstyle="->", color="#2E7D52", lw=1.5))
    ax.text(5.35, 2.1, "actions", ha="center", fontsize=7, color="#2E7D52")

    # Performance box (top)
    perf_box = mpatches.FancyBboxPatch((2.8, 3.0), 2.4, 0.8,
        boxstyle="round,pad=0.1", linewidth=1.2,
        edgecolor="#6A4C93", facecolor="#F4F0F9")
    ax.add_patch(perf_box)
    ax.text(4.0, 3.42, "Performance measure", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="#6A4C93")
    ax.text(4.0, 3.13, "(score: how good is the agent?)", ha="center",
            va="center", fontsize=7.5, color="#1A202C")
    ax.annotate("", xy=(4.0, 2.6), xytext=(4.0, 3.0),
                arrowprops=dict(arrowstyle="-", color="#6A4C93", lw=1.2,
                                linestyle="dashed"))

    # Environment box (bottom)
    env_box = mpatches.FancyBboxPatch((2.8, 0.2), 2.4, 0.9,
        boxstyle="round,pad=0.1", linewidth=1.2,
        edgecolor="#8A5A1E", facecolor="#FDF3E7")
    ax.add_patch(env_box)
    ax.text(4.0, 0.72, "Environment", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="#8A5A1E")
    ax.text(4.0, 0.40, "(world the agent lives in)", ha="center",
            va="center", fontsize=7.5, color="#1A202C")
    ax.annotate("", xy=(4.0, 1.4), xytext=(4.0, 1.1),
                arrowprops=dict(arrowstyle="-", color="#8A5A1E", lw=1.2,
                                linestyle="dashed"))

    ax.set_title("PEAS — the four-part task description for any AI agent\n"
                 "Sensors feed in; Actuators act out; Performance scores; Environment surrounds",
                 fontweight="bold", fontsize=8.5)

    out = os.path.join(HERE, "fig_peas_structure.png")
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    fig_env_properties()
    fig_agent_ladder()
    fig_problem_formulation()
    fig_search_taxonomy()
    fig_vacuum_states()
    fig_peas_structure()
    print("All figures done.")
