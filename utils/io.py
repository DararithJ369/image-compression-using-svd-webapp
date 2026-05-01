"""I/O utilities: image ↔ bytes, CSS loader."""
import io
import numpy as np
from PIL import Image
from pathlib import Path


def image_to_bytes(img_array: np.ndarray) -> bytes:
    """Convert numpy image array to PNG bytes."""
    buf = io.BytesIO()
    Image.fromarray(img_array).save(buf, format="PNG")
    return buf.getvalue()


def load_css(css_path: str = "styles/theme.css") -> str:
    """Load CSS file content for Streamlit injection."""
    css_file = Path(css_path)
    if css_file.exists():
        return css_file.read_text(encoding="utf-8")
    return ""