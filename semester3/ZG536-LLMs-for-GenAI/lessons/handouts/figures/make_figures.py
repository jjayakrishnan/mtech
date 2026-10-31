#!/usr/bin/env python3
"""Figures for the ZG536 Session 1 companion: Foundations of Large Language
Models. Run from the skill root so `import figstyle` resolves:
    python3 figures/make_figures.py   (invoked automatically by build_pdf.py)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))
import figstyle  # noqa: E402

HERE = os.path.dirname(__file__)


def out(name):
    return os.path.join(HERE, name)


def fig_pipeline():
    figstyle.flow(
        ["Raw text\n(a sentence)",
         "Tokenizer\n(BPE: text ->\ntoken IDs)",
         "Embedding +\npositional encoding\n(IDs -> vectors)",
         "Transformer\nstack\n(attention + FFN)",
         "LM head ->\nnext-token\nprobabilities"],
        "The pipeline every sentence travels through, once per generated token",
        direction="lr",
        out=out("fig_pipeline.png"),
    )


def fig_ngram_probs():
    figstyle.bars(
        ["mailman", "cat"],
        [0.67, 0.33],
        "Tiny n-gram model: P(next word | 'the dog barked at the ___')",
        xlabel="candidate next word",
        ylabel="probability",
        fmt="{:.2f}",
        out=out("fig_ngram_probs.png"),
    )


def fig_bpe_merge_counts():
    figstyle.bars(
        ["(e, r)", "(er, _)", "(l, o)", "(n, e)"],
        [11, 11, 9, 6],
        "BPE merge step 1: pair frequencies across the toy corpus",
        xlabel="adjacent symbol pair",
        ylabel="count across corpus",
        fmt="{:.0f}",
        out=out("fig_bpe_merge_counts.png"),
    )


def fig_next_token_pmf():
    figstyle.pmf_bar(
        ["great", "good", "slow", "long", "boring"],
        [0.44, 0.28, 0.13, 0.10, 0.05],
        "LM head output: P(next word | 'The dog movie was really ___')",
        xlabel="candidate next token",
        ylabel="probability",
        out=out("fig_next_token_pmf.png"),
    )


def fig_embedding_space():
    figstyle.vectors2d(
        [(0.9, 0.1, "dog", figstyle.PALETTE["accent"]),
         (0.8, 0.2, "cat", figstyle.PALETTE["light"]),
         (0.1, 0.9, "car", figstyle.PALETTE["high"])],
        "Toy embedding space: 'dog' sits near 'cat', far from 'car'",
        out=out("fig_embedding_space.png"),
    )


if __name__ == "__main__":
    fig_pipeline()
    fig_ngram_probs()
    fig_bpe_merge_counts()
    fig_next_token_pmf()
    fig_embedding_space()
    print("figures written to", HERE)
