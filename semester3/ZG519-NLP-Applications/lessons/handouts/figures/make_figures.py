#!/usr/bin/env python3
"""Figures for the ZG519 Session 1 companion: Course Overview and NLP
Applications. Run from the skill root so `import figstyle` resolves:
    python3 figures/make_figures.py   (invoked automatically by build_pdf.py)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))
import figstyle  # noqa: E402

HERE = os.path.dirname(__file__)


def out(name):
    return os.path.join(HERE, name)


def fig_difficulty():
    labels = ["Spell\ncheck", "Lang\nID", "Sentim.", "Summary", "NER",
              "MT", "QA /\nConv AI", "RAG", "Agentic\nRAG", "Scale &\neffic."]
    values = [1, 2, 3, 4, 5, 6, 7, 8.5, 9.5, 8]
    figstyle.bars(
        labels, values,
        "Ten applications, ranked easiest to hardest (illustrative)",
        ylabel="relative difficulty & cost",
        annotate=False,
        out=out("fig_difficulty.png"),
    )


def fig_codeswitch():
    tokens = ["Bro,", "idhu", "kashtam", "but", "deadline", "tmrw"]
    tags = ["EN", "TA", "TA", "EN", "EN", "EN"]
    figstyle.annotated_sequence(
        tokens,
        "Language ID on a code-switched message: tagging each word EN or TA",
        tags=tags,
        highlight=[1, 2],
        out=out("fig_codeswitch.png"),
    )


def fig_ner():
    tokens = ["Google", "acquired", "DeepMind", "in", "2014", "for",
              "Rs.", "4,000", "crore."]
    tags = ["ORG", "", "ORG", "", "DATE", "", "MONEY", "MONEY", ""]
    figstyle.annotated_sequence(
        tokens,
        "Information extraction: entities (ORG, DATE, MONEY) tagged on a sentence",
        tags=tags,
        highlight=[0, 2, 4, 6, 7],
        out=out("fig_ner.png"),
    )


def fig_agentic_rag():
    figstyle.flow(
        ["Question\narrives",
         "Reason:\nwhat fact is\nstill missing?",
         "Retrieve\none more\nfact",
         "Enough\nevidence?\nif not, loop",
         "Generate\nthe grounded\nanswer"],
        "Agentic RAG: retrieval is a decision the system makes, not a fixed step",
        direction="lr",
        out=out("fig_agentic_rag.png"),
    )


if __name__ == "__main__":
    fig_difficulty()
    fig_codeswitch()
    fig_ner()
    fig_agentic_rag()
    print("figures written to", HERE)
