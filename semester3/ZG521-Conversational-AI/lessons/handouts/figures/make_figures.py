#!/usr/bin/env python3
"""Figures for the ZG521 Session 1 companion: Foundations of Conversational
and Agentic AI. Run from the skill root so `import figstyle` resolves:
    python3 figures/make_figures.py   (invoked automatically by build_pdf.py)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))
import figstyle  # noqa: E402

HERE = os.path.dirname(__file__)


def out(name):
    return os.path.join(HERE, name)


def fig_evolution():
    figstyle.flow(
        ["Eliza / Alice\n(hand-written\nrules)",
         "Retrieval / ML\nchatbots\n(best-match reply)",
         "LLM assistants\n(fresh text,\none-shot)",
         "Autonomous agents\n(loop + tools\n+ memory)"],
        "Four eras of the same idea: a system that talks back",
        direction="lr",
        out=out("fig_evolution.png"),
    )


def fig_react_loop():
    figstyle.flow(
        ["Reason\n(what should\nI do next?)",
         "Act\n(call one tool)",
         "Observe\n(read the\ntool's result)",
         "Repeat, or\ngive the\nfinal answer"],
        "The ReAct loop: one cycle of an agent's turn",
        direction="lr",
        out=out("fig_react_loop.png"),
    )


def fig_architecture():
    figstyle.flow(
        ["User message\narrives",
         "Orchestrator\n(the controller)",
         "Picks: call the LLM /\ncall a tool /\nread memory",
         "Reply is sent,\nstate is saved"],
        "System architecture, zoomed out: who calls whom",
        direction="lr",
        out=out("fig_architecture.png"),
    )


if __name__ == "__main__":
    fig_evolution()
    fig_react_loop()
    fig_architecture()
    print("figures written to", HERE)
