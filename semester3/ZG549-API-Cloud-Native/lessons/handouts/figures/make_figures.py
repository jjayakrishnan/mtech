#!/usr/bin/env python3
"""Figures for the ZG549 Session 1 companion: API Basics. Run from the skill
root so `import figstyle` resolves:
    python3 figures/make_figures.py   (invoked automatically by build_pdf.py)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))
import figstyle  # noqa: E402

HERE = os.path.dirname(__file__)


def out(name):
    return os.path.join(HERE, name)


def fig_api_layer():
    figstyle.flow(
        ["PawPatrol app\n(the client)",
         "The API\n(the contract:\nverbs + URLs)",
         "The server\n(implementation\nhidden)",
         "Database or\nanother service"],
        "An API is a layer: the client only ever talks to the contract",
        direction="lr",
        out=out("fig_api_layer.png"),
    )


def fig_lifecycle():
    figstyle.flow(
        ["Requirements\n(what should\nit do?)",
         "Design\n(pick endpoints\n+ verbs)",
         "Configure &\npublish the\ncontract",
         "Develop,\ntest, deploy"],
        "From idea to running API: the seven-stage build lifecycle",
        direction="lr",
        out=out("fig_lifecycle.png"),
    )


def fig_n_plus_one():
    figstyle.flow(
        ["1 request:\nget walker\nprofile",
         "+1 request:\nget walker's\nbookings",
         "+1 request\nPER booking:\nget its review",
         "= 1 + 1 + N\nrequests"],
        "REST's N+1 problem: one profile, its bookings, every booking's review",
        direction="lr",
        out=out("fig_n_plus_one.png"),
    )


if __name__ == "__main__":
    fig_api_layer()
    fig_lifecycle()
    fig_n_plus_one()
    print("figures written to", HERE)
