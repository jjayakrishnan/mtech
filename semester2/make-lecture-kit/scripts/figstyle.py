#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""House matplotlib style for ISM Companion figures.

This module is the single source of truth for what the companion's figures
look like. Per-lecture figure scripts (the little ``*.py`` files that live in
a lecture's ``figures/`` folder) import it and call the helpers below, so every
plot across every session shares one muted, slide-friendly look.

Pure matplotlib + numpy + stdlib. No other third-party dependencies.

----------------------------------------------------------------------
How a per-lecture figure script uses this (the host agent writes these)
----------------------------------------------------------------------

    # figures/fig_bernoulli.py  -- run from anywhere; saves next to the .tex
    import os
    from figstyle import use_house_style, pmf_bar, PALETTE

    use_house_style()                      # set the global look once
    here = os.path.dirname(os.path.abspath(__file__))
    out  = os.path.join(here, "fig_bernoulli.png")

    pmf_bar(
        xs=[0, 1],
        ps=[0.4, 0.6],
        title="Bernoulli(p=0.6): one shot, two outcomes",
        xlabel="outcome", ylabel="probability",
        out=out,                           # <-- writing the PNG is what matters
    )

The build orchestrator (``build_pdf.py``) discovers and runs every ``*.py`` in
the figures folder, so each script only needs to *save* its PNG. The functions
also RETURN the Matplotlib figure, which is handy for interactive tinkering.

Design notes (kept deliberately close to the gold-standard PDF):
  * muted palette that matches the five callout-box colours in the .tex
  * thin, de-emphasised top/right spines; soft horizontal grid only
  * a short BOLD title baked into the plot itself (the slides have these)
  * sizes tuned for full-textwidth A4 (~ 7.0 x 3.2 inches) at dpi 150
  * tight_layout so nothing is clipped when \includegraphics scales it
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, Mapping, Optional, Sequence, Tuple

import matplotlib

# Use a non-interactive backend so this works headless (sandboxes, CI, servers).
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (must come after backend choice)
import numpy as np  # noqa: E402


# ---------------------------------------------------------------------------
# (b) Palette -- one muted colour per callout-box family in the companion.
#     Frame colours mirror the .tex taxonomy so figures and boxes feel unified.
# ---------------------------------------------------------------------------
PALETTE: Dict[str, str] = {
    # the five teaching colours (match the tcolorbox pill tabs)
    "blue":   "#2C5AA0",  # The intuition
    "green":  "#2E7D52",  # Worked example
    "amber":  "#C8881E",  # Everyday picture  (a touch deeper than #8A5A1E for lines)
    "red":    "#B23A48",  # Watch out
    "purple": "#6A4C93",  # Key takeaway
    # supporting tones
    "ink":    "#21355E",  # the navy banner / heading colour -> use for titles
    "muted":  "#5B6470",  # secondary text, secondary lines
    "grid":   "#D9DEE8",  # soft grid lines
    "fill":   "#EAF0F7",  # very light wash for shaded regions / soft bars
}

# A stable, muted cycle for multi-series ``curve`` plots.
_CYCLE: Tuple[str, ...] = (
    PALETTE["blue"], PALETTE["green"], PALETTE["amber"],
    PALETTE["red"], PALETTE["purple"], PALETTE["muted"],
)


# ---------------------------------------------------------------------------
# (a) The house style.
# ---------------------------------------------------------------------------
def use_house_style() -> None:
    """Set global matplotlib rcParams to match the gold-standard figures.

    Idempotent: call it once at the top of every figure script (calling it
    again is harmless). It tweaks only rcParams, so it never opens a window.
    """
    plt.rcParams.update({
        # --- canvas / output ---
        "figure.figsize": (7.0, 3.2),   # full A4 textwidth, slide-friendly aspect
        "figure.dpi": 150,              # crisp without bloating the PDF
        "savefig.dpi": 150,
        "savefig.bbox": "tight",        # belt-and-braces against clipped labels
        "savefig.pad_inches": 0.04,
        "figure.facecolor": "white",
        "axes.facecolor": "white",

        # --- typography (readable, neutral sans; degrades gracefully) ---
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial", "sans-serif"],
        "font.size": 10.5,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlepad": 9.0,
        "axes.labelsize": 10.5,
        "axes.labelcolor": PALETTE["ink"],
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,

        # --- spines: keep left+bottom, drop top+right, soften colour ---
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": PALETTE["muted"],
        "axes.linewidth": 0.8,
        "axes.titlecolor": PALETTE["ink"],

        # --- ticks: short, quiet ---
        "xtick.color": PALETTE["muted"],
        "ytick.color": PALETTE["muted"],
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,

        # --- grid: faint horizontal guide lines only ---
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.8,
        "grid.alpha": 0.9,

        # --- legend: clean, frameless-ish ---
        "legend.frameon": False,
        "legend.handlelength": 1.6,
        "legend.borderaxespad": 0.4,

        # --- lines ---
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
    })


def _new_axes(figsize: Optional[Tuple[float, float]] = None):
    """Create a fig/ax pair under the house style and return ``(fig, ax)``."""
    use_house_style()
    fig, ax = plt.subplots(figsize=figsize or plt.rcParams["figure.figsize"])
    return fig, ax


def _finish(fig, ax, title: str, out: Optional[str]):
    """Apply the shared title + layout, optionally save, and return ``fig``."""
    if title:
        ax.set_title(title, color=PALETTE["ink"], fontweight="bold")
    # de-emphasise the kept spines a touch more
    for side in ("left", "bottom"):
        if side in ax.spines:
            ax.spines[side].set_color(PALETTE["muted"])
    fig.tight_layout()
    if out:
        fig.savefig(out)
        # free memory when batch-rendering many figures in one process
        plt.close(fig)
    return fig


# ---------------------------------------------------------------------------
# (c) Reusable plotters.
#     Each returns the figure and, when given ``out``, saves a PNG to it.
# ---------------------------------------------------------------------------
def pmf_bar(
    xs: Sequence,
    ps: Sequence[float],
    title: str,
    *,
    xlabel: str = "outcome",
    ylabel: str = "probability",
    color: str = PALETTE["blue"],
    annotate: bool = True,
    out: Optional[str] = None,
):
    """Bar chart of a probability mass function (discrete distribution).

    Parameters
    ----------
    xs        : the outcomes / support (any labels; cast to str on the axis).
    ps        : matching probabilities (same length as ``xs``).
    title     : short bold title baked into the plot.
    xlabel/ylabel : axis labels.
    color     : bar colour (defaults to the 'blue' teaching tone).
    annotate  : write each probability above its bar.
    out       : if given, save a PNG there.

    Example
    -------
    >>> pmf_bar([0, 1], [0.4, 0.6], "Bernoulli(p=0.6): one shot, two outcomes")
    """
    xs = list(xs)
    ps = [float(p) for p in ps]
    if len(xs) != len(ps):
        raise ValueError("pmf_bar: xs and ps must have the same length")

    fig, ax = _new_axes()
    positions = np.arange(len(xs))
    bars = ax.bar(positions, ps, width=0.6, color=color,
                  edgecolor="white", linewidth=0.8, zorder=3)

    ax.set_xticks(positions)
    ax.set_xticklabels([str(x) for x in xs])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    top = max(ps) if ps else 1.0
    ax.set_ylim(0, top * 1.18 if top > 0 else 1.0)

    if annotate:
        for rect, p in zip(bars, ps):
            ax.annotate(
                f"{p:.2f}",
                xy=(rect.get_x() + rect.get_width() / 2, rect.get_height()),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom",
                fontsize=9.5, color=PALETTE["ink"], fontweight="bold",
            )

    return _finish(fig, ax, title, out)


def curve(
    x: Sequence[float],
    ys_dict: Mapping[str, Sequence[float]],
    title: str,
    *,
    xlabel: str = "x",
    ylabel: str = "y",
    colors: Optional[Mapping[str, str]] = None,
    fill_below: Optional[str] = None,
    out: Optional[str] = None,
):
    """Line plot of one or more curves sharing an x-axis.

    Parameters
    ----------
    x         : shared x-values.
    ys_dict   : ``{label: y_values}`` -- one line per entry, auto-legended
                (the legend is hidden when there is only one unlabeled line).
    title     : short bold title.
    xlabel/ylabel : axis labels.
    colors    : optional ``{label: colour}`` overrides; otherwise a muted cycle.
    fill_below: if set to one of the labels, lightly shade under that curve.
    out       : if given, save a PNG there.

    Example
    -------
    >>> import numpy as np
    >>> x = np.linspace(0, 10, 200)
    >>> curve(x, {"lambda=1": np.exp(-x), "lambda=0.5": np.exp(-0.5*x)},
    ...       "Exponential densities for two rates", xlabel="t", ylabel="f(t)")
    """
    x = np.asarray(x, dtype=float)
    fig, ax = _new_axes()

    labels = list(ys_dict.keys())
    for i, label in enumerate(labels):
        y = np.asarray(ys_dict[label], dtype=float)
        if colors and label in colors:
            c = colors[label]
        else:
            c = _CYCLE[i % len(_CYCLE)]
        ax.plot(x, y, color=c, label=label, zorder=3)
        if fill_below is not None and label == fill_below:
            ax.fill_between(x, y, color=c, alpha=0.12, zorder=2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Only show a legend when it carries information (multiple / named series).
    show_legend = len(labels) > 1 or (
        len(labels) == 1 and not str(labels[0]).startswith("_")
    )
    if show_legend:
        ax.legend(loc="best")

    return _finish(fig, ax, title, out)


def shaded_normal(
    mu: float,
    sigma: float,
    lo: float,
    hi: float,
    title: str,
    *,
    xlabel: str = "x",
    ylabel: str = "density",
    color: str = PALETTE["blue"],
    shade: str = PALETTE["blue"],
    label_area: bool = True,
    out: Optional[str] = None,
):
    """Normal (Gaussian) density curve with the area on ``[lo, hi]`` shaded.

    This is the classic "probability = area under the curve" picture. The
    shaded slice's probability is computed exactly with the error function and
    written onto the plot, so worked examples line up with the figure.

    Parameters
    ----------
    mu, sigma : mean and standard deviation (sigma > 0).
    lo, hi    : shade the region between these x-values (use +/- math.inf for tails).
    title     : short bold title.
    xlabel/ylabel : axis labels.
    color     : curve colour.
    shade     : fill colour for the highlighted slice.
    label_area: annotate the shaded probability P(lo < X < hi).
    out       : if given, save a PNG there.

    Example
    -------
    >>> shaded_normal(0, 1, -1, 1, "Standard normal: about 68% within 1 sigma")
    """
    if sigma <= 0:
        raise ValueError("shaded_normal: sigma must be positive")
    if lo > hi:
        lo, hi = hi, lo

    fig, ax = _new_axes()

    # Plot the full curve across +/- 4 sigma.
    left, right = mu - 4 * sigma, mu + 4 * sigma
    xs = np.linspace(left, right, 400)
    pdf = (1.0 / (sigma * math.sqrt(2 * math.pi))) * np.exp(
        -0.5 * ((xs - mu) / sigma) ** 2
    )
    ax.plot(xs, pdf, color=color, zorder=3)

    # Shade the requested slice (clip the +/-inf tails to the drawn window).
    s_lo = left if lo == -math.inf else max(lo, left)
    s_hi = right if hi == math.inf else min(hi, right)
    mask = (xs >= s_lo) & (xs <= s_hi)
    ax.fill_between(xs[mask], pdf[mask], color=shade, alpha=0.22, zorder=2)

    # Thin guide lines at the slice edges (skip infinite ones).
    for edge in (lo, hi):
        if math.isfinite(edge) and left <= edge <= right:
            ax.axvline(edge, color=PALETTE["muted"], linewidth=0.9,
                       linestyle=(0, (4, 3)), zorder=1)

    # Exact area via the standard-normal CDF (error function -> no SciPy needed).
    def _cdf(v: float) -> float:
        if v == -math.inf:
            return 0.0
        if v == math.inf:
            return 1.0
        return 0.5 * (1.0 + math.erf((v - mu) / (sigma * math.sqrt(2))))

    area = _cdf(hi) - _cdf(lo)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)

    if label_area:
        cx = np.clip((s_lo + s_hi) / 2.0, left, right)
        ax.annotate(
            f"area = {area:.3f}",
            xy=(cx, ax.get_ylim()[1] * 0.45),
            ha="center", va="center",
            fontsize=10, color=PALETTE["ink"], fontweight="bold",
        )

    return _finish(fig, ax, title, out)


# ---------------------------------------------------------------------------
# Self-test: ``python3 figstyle.py [outdir]`` renders one of each plotter.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    import sys

    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)

    pmf_bar([0, 1], [0.4, 0.6],
            "Bernoulli(p=0.6): one shot, two outcomes",
            out=os.path.join(outdir, "demo_pmf.png"))

    x = np.linspace(0, 8, 240)
    curve(x, {"rate 1.0": np.exp(-x), "rate 0.5": np.exp(-0.5 * x)},
          "Exponential densities for two rates",
          xlabel="t", ylabel="f(t)", fill_below="rate 1.0",
          out=os.path.join(outdir, "demo_curve.png"))

    shaded_normal(0, 1, -1, 1,
                  "Standard normal: about 68% within one sigma",
                  out=os.path.join(outdir, "demo_normal.png"))

    print("figstyle self-test wrote 3 PNGs to:", os.path.abspath(outdir))
