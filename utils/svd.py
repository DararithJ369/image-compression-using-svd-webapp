"""
utils/svd.py
Core SVD compression mathematics — no Streamlit dependencies.
"""

import math
import numpy as np


def compress_image(arr: np.ndarray, k: int) -> np.ndarray:
    """
    Reconstruct an image using only the top-k singular values per channel.

    Parameters
    ----------
    arr : np.ndarray  — uint8 image array, shape (H, W) or (H, W, 3)
    k   : int         — number of singular components to keep

    Returns
    -------
    np.ndarray  — uint8 compressed image, same shape as `arr`
    """
    if len(arr.shape) == 3 and arr.shape[2] >= 3:
        channels = []
        for i in range(3):
            U, S, Vt = np.linalg.svd(arr[:, :, i].astype(np.float64), full_matrices=False)
            channel  = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
            channels.append(channel)
        out = np.stack(channels, axis=2)
    else:
        src = arr[:, :, 0] if len(arr.shape) == 3 else arr
        U, S, Vt = np.linalg.svd(src.astype(np.float64), full_matrices=False)
        out = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

    return np.clip(out, 0, 255).astype(np.uint8)


def get_singular_values(arr: np.ndarray) -> list[np.ndarray]:
    """
    Return the singular value vectors for each channel.

    Returns
    -------
    list of 1-D arrays — one per channel (3 for RGB, 1 for grayscale)
    """
    if len(arr.shape) == 3:
        result = []
        for i in range(3):
            _, S, _ = np.linalg.svd(arr[:, :, i].astype(np.float64), full_matrices=False)
            result.append(S)
        return result
    else:
        _, S, _ = np.linalg.svd(arr.astype(np.float64), full_matrices=False)
        return [S]


def compute_psnr(original: np.ndarray, compressed: np.ndarray) -> float:
    """Peak Signal-to-Noise Ratio in dB. Higher is better (>40 dB ≈ excellent)."""
    mse = np.mean((original.astype(np.float64) - compressed.astype(np.float64)) ** 2)
    if mse == 0:
        return float("inf")
    return 20 * math.log10(255.0 / math.sqrt(mse))


def compute_compression_ratio(h: int, w: int, k: int, channels: int = 3) -> float:
    """Theoretical storage ratio: original_values / compressed_values."""
    original   = h * w * channels
    compressed = k * (h + w + 1) * channels
    return original / compressed


def compute_metrics(img_array: np.ndarray, compressed: np.ndarray, k: int) -> dict:
    """
    Bundle all scalar metrics into one dict for easy passing between modules.
    """
    h, w   = img_array.shape[:2]
    ch     = 3 if len(img_array.shape) == 3 else 1
    max_k  = min(h, w)

    orig_bytes = h * w * ch
    comp_bytes = k * (h + w + 1) * ch
    saved_pct  = max(0.0, (1 - comp_bytes / orig_bytes) * 100)

    return {
        "h":          h,
        "w":          w,
        "channels":   ch,
        "max_k":      max_k,
        "orig_bytes": orig_bytes,
        "comp_bytes": comp_bytes,
        "ratio":      compute_compression_ratio(h, w, k, ch),
        "psnr":       compute_psnr(img_array, compressed),
        "saved_pct":  saved_pct,
    }