"""Matplotlib figure builders for analysis tabs."""
import numpy as np
import matplotlib.pyplot as plt


def make_sv_chart(sv_list: list[np.ndarray], k: int, max_k: int) -> plt.Figure:
    """Create singular value cumulative energy chart."""
    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor('#161c2d')
    ax.set_facecolor('#111520')

    colors = ['#00e5ff', '#ff6b6b', '#a78bfa']
    labels = ['Red', 'Green', 'Blue'] if len(sv_list) == 3 else ['Gray']
    
    for idx, (sv, label) in enumerate(zip(sv_list, labels)):
        cumulative = np.cumsum(sv) / np.sum(sv) * 100
        x = np.arange(1, len(sv) + 1)
        ax.plot(x, cumulative, color=colors[idx], lw=1.5,
                alpha=0.9, label=label)

    # k marker
    ax.axvline(x=k, color='#fbbf24', lw=1.5, linestyle='--', alpha=0.8)
    ax.text(k + max_k * 0.01, 10, f'k={k}',
            color='#fbbf24', fontsize=9, va='bottom', fontfamily='monospace')

    ax.set_xlim(1, max_k)
    ax.set_ylim(0, 102)
    ax.set_xlabel('Rank k', color='#4a5578', fontsize=9, fontfamily='monospace')
    ax.set_ylabel('Cumulative energy %', color='#4a5578', fontsize=9, fontfamily='monospace')
    ax.tick_params(colors='#4a5578', labelsize=8)
    for spine in ax.spines.values():
        spine.set_color('#1f2a45')
    ax.grid(True, color='#1f2a45', lw=0.5, alpha=0.7)
    ax.legend(framealpha=0, labelcolor='#c9d1e8', fontsize=9)
    fig.tight_layout()
    return fig


def make_error_map(original: np.ndarray, compressed: np.ndarray) -> plt.Figure:
    """Create absolute difference heatmap."""
    diff = np.abs(original.astype(np.float64) - compressed.astype(np.float64))
    if len(diff.shape) == 3:
        diff = diff.mean(axis=2)
    
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor('#161c2d')
    ax.set_facecolor('#111520')
    
    im = ax.imshow(diff, cmap='inferno', vmin=0, vmax=80)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(colors='#4a5578', labelsize=8)
    cbar.outline.set_edgecolor('#1f2a45')
    ax.axis('off')
    ax.set_title('Pixel Error Map', color='#c9d1e8', fontsize=10, fontfamily='monospace', pad=8)
    fig.tight_layout()
    return fig