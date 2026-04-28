"""
utils/io.py
File I/O helpers — image encoding and CSS loading.
"""

import io
from pathlib import Path

import numpy as np
from PIL import Image


def image_to_bytes(img_array: np.ndarray) -> bytes:
    """Encode a numpy uint8 array as PNG bytes for st.download_button."""
    buf = io.BytesIO()
    Image.fromarray(img_array).save(buf, format="PNG")
    return buf.getvalue()


def load_css(path: str | Path) -> str:
    """Read a .css file and return its contents as a string."""
    return Path(path).read_text(encoding="utf-8")