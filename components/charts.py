"""
components/charts.py
Matplotlib figure builders — no Streamlit calls, just return Figure objects.
"""

import numpy as np
import matplotlib.pyplot as plt


# ── Colour palette (matches CSS theme) ───────────────────────────────────────
BG_DARK   = "#161c2d"
BG_DARKER = "#111520"
BORDER    = "#1f2a45"
MUTED     = "#4a5578"
TEXT      = "#c9d1e8"
CYAN      = "#00e5ff"
RED       = "#ff6b6b"
PURPLE    = "#a78bfa"
YELLOW    = "#fbbf24"
GREEN     = "#34d399"

CH_COLORS = [RED, GREEN, CYAN]


def make_sv_energy_chart(
    sv_list: list[np.ndarray],
    k: int,
    max_k: int,
) -> plt.Figure:
    """
    Cumulative singular-value energy curves (one per RGB channel)
    with a dashed vertical line at the selected rank k.
    """
    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARKER)

    labels = ["Red", "Green", "Blue"] if len(sv_list) == 3 else ["Gray"]

    for sv, color, label in zip(sv_list, CH_COLORS, labels):
        cumulative = np.cumsum(sv) / np.sum(sv) * 100
        x = np.arange(1, len(sv) + 1)
        ax.plot(x, cumulative, color=color, lw=1.5, alpha=0.9, label=label)

    # k marker
    ax.axvline(x=k, color=YELLOW, lw=1.5, linestyle="--", alpha=0.8)
    ax.text(
        k + max_k * 0.01, 10, f"k={k}",
        color=YELLOW, fontsize=9, va="bottom", fontfamily="monospace",
    )

    ax.set_xlim(1, max_k)
    ax.set_ylim(0, 102)
    ax.set_xlabel("Rank k",               color=MUTED, fontsize=9, fontfamily="monospace")
    ax.set_ylabel("Cumulative energy %",  color=MUTED, fontsize=9, fontfamily="monospace")
    ax.tick_params(colors=MUTED, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    ax.grid(True, color=BORDER, lw=0.5, alpha=0.7)
    ax.legend(framealpha=0, labelcolor=TEXT, fontsize=9)
    fig.tight_layout()
    return fig


def make_error_heatmap(
    original: np.ndarray,
    compressed: np.ndarray,
) -> plt.Figure:
    """
    Absolute per-pixel difference rendered as an inferno heatmap.
    Bright areas = high reconstruction error.
    """
    diff = np.abs(original.astype(np.float64) - compressed.astype(np.float64))
    if len(diff.shape) == 3:
        diff = diff.mean(axis=2)

    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARKER)

    im   = ax.imshow(diff, cmap="inferno", vmin=0, vmax=80)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(colors=MUTED, labelsize=8)
    cbar.outline.set_edgecolor(BORDER)

    ax.axis("off")
    ax.set_title(
        "Pixel Error Map",
        color=TEXT, fontsize=10, fontfamily="monospace", pad=8,
    )
    fig.tight_layout()
    return fig