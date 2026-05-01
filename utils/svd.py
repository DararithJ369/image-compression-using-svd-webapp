"""SVD mathematics: compression, PSNR, metrics."""
import numpy as np
import math


def compress_image(arr: np.ndarray, k_val: int) -> np.ndarray:
    """Reconstruct image using top-k singular values."""
    if len(arr.shape) == 3 and arr.shape[2] >= 3:
        compressed_channels = []
        for i in range(3):
            U, S, Vt = np.linalg.svd(arr[:, :, i].astype(np.float64), full_matrices=False)
            chan = U[:, :k_val] @ np.diag(S[:k_val]) @ Vt[:k_val, :]
            compressed_channels.append(chan)
        out = np.stack(compressed_channels, axis=2)
    else:
        if len(arr.shape) == 3:
            arr = arr[:, :, 0]
        U, S, Vt = np.linalg.svd(arr.astype(np.float64), full_matrices=False)
        out = U[:, :k_val] @ np.diag(S[:k_val]) @ Vt[:k_val, :]
    return np.clip(out, 0, 255).astype(np.uint8)


def compute_psnr(original: np.ndarray, compressed: np.ndarray) -> float:
    """Peak Signal-to-Noise Ratio in dB."""
    mse = np.mean((original.astype(np.float64) - compressed.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(mse))


def compute_compression_ratio(h: int, w: int, k: int, channels: int = 3) -> float:
    """Calculate compression ratio: original_size / compressed_size."""
    original = h * w * channels
    compressed = k * (h + w + 1) * channels
    return original / compressed


def get_singular_values(arr: np.ndarray) -> list[np.ndarray]:
    """Return singular values for each channel."""
    svs = []
    if len(arr.shape) == 3:
        for i in range(3):
            _, S, _ = np.linalg.svd(arr[:, :, i].astype(np.float64), full_matrices=False)
            svs.append(S)
    else:
        _, S, _ = np.linalg.svd(arr.astype(np.float64), full_matrices=False)
        svs.append(S)
    return svs


def compute_metrics(original: np.ndarray, compressed: np.ndarray, 
                   h: int, w: int, k: int, channels: int = 3) -> dict:
    """Compute all compression metrics in one call."""
    psnr_val = compute_psnr(original, compressed)
    ratio = compute_compression_ratio(h, w, k, channels)
    orig_bytes = h * w * channels
    comp_bytes = k * (h + w + 1) * channels
    saved_pct = max(0, (1 - comp_bytes / orig_bytes) * 100)
    
    return {
        "psnr": psnr_val,
        "ratio": ratio,
        "saved_pct": saved_pct,
        "orig_bytes": orig_bytes,
        "comp_bytes": comp_bytes,
    }