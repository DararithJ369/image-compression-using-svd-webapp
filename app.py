"""
app.py
──────
Entry point for the SVD Compression Lab.

Run with:
    streamlit run app.py

Project layout
──────────────
svd_lab/
├── app.py                   ← you are here (orchestrator)
├── styles/
│   └── theme.css            ← all custom CSS
├── utils/
│   ├── __init__.py
│   ├── svd.py               ← SVD math (compress, PSNR, metrics)
│   └── io.py                ← image ↔ bytes, CSS loader
└── components/
    ├── __init__.py
    ├── header.py            ← hero banner + overview expander
    ├── sidebar.py           ← file upload + k slider
    ├── metrics.py           ← 4 stat cards
    ├── charts.py            ← matplotlib figure builders
    └── tabs.py              ← Compare / Analysis / Difference tabs
"""
import streamlit as st
import numpy as np
from PIL import Image

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SVD Compression Lab",
    layout="wide",
    initial_sidebar_state="expanded",  # Forces open on load
)

# ── Imports ───────────────────────────────────────────────────────────────────
from utils.svd import compress_image, compute_psnr, compute_compression_ratio
from utils.io import load_css
from components.header import (
    render_hero,
    render_app_intro,
    render_quick_start,
    render_main_upload_panel,
    render_overview,
)
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.tabs import render_tabs


def load_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    max_k = min(height, width)
    return img_array, height, width, max_k


def build_demo_image(height: int = 720, width: int = 960) -> np.ndarray:
    y, x = np.mgrid[0:height, 0:width]
    x_norm = x / max(1, width - 1)
    y_norm = y / max(1, height - 1)

    red = 255 * (0.55 * x_norm + 0.45 * np.sin(3.5 * np.pi * y_norm) ** 2)
    green = 255 * (0.55 * y_norm + 0.45 * np.cos(2.8 * np.pi * x_norm) ** 2)
    blue = 255 * (0.5 * (np.sin(2.2 * np.pi * (x_norm + y_norm)) + 1.0))

    image = np.dstack([red, green, blue]).astype(np.uint8)

    center_x, center_y = int(width * 0.68), int(height * 0.35)
    radius = int(min(height, width) * 0.16)
    circle = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius**2
    image[circle] = [245, 120, 70]

    band = np.abs((x - y * 0.72) % 120 - 60) < 12
    image[band] = np.clip(image[band] * np.array([0.72, 1.12, 1.25]), 0, 255)
    return image


def ensure_state():
    defaults = {
        "active_image": None,
        "active_name": None,
        "active_source": None,
        "ui_mode": "upload",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ── Custom CSS ────────────────────────────────────────────────────────────
css_content = load_css("styles/theme.css")
if css_content:
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

ensure_state()

# ── Hero + Overview ───────────────────────────────────────────────────────────
render_hero()
render_app_intro()
render_quick_start()
render_overview()

main_uploaded_file, use_demo_scene = render_main_upload_panel()
if use_demo_scene:
    st.session_state.active_image = build_demo_image()
    st.session_state.active_name = "demo-scene.png"
    st.session_state.active_source = "demo"
    st.session_state.ui_mode = "demo"
elif main_uploaded_file is not None:
    st.session_state.active_image, main_h, main_w, main_max_k = load_image(main_uploaded_file)
    st.session_state.active_name = main_uploaded_file.name
    st.session_state.active_source = "upload"
    st.session_state.ui_mode = "upload"
elif st.session_state.ui_mode == "upload" and st.session_state.active_source == "demo":
    st.session_state.active_image = None
    st.session_state.active_name = None
    st.session_state.active_source = None

# ── Sidebar Controls ──────────────────────────────────────────────────────────
sidebar_uploaded_file, sidebar_img_array, sidebar_k, sidebar_h, sidebar_w, sidebar_max_k = render_sidebar(
    active_image=st.session_state.active_image
)

if st.session_state.active_image is None and sidebar_uploaded_file is not None:
    st.session_state.active_image, main_h, main_w, main_max_k = load_image(sidebar_uploaded_file)
    st.session_state.active_name = sidebar_uploaded_file.name
    st.session_state.active_source = "upload"
    st.session_state.ui_mode = "upload"

uploaded_file = main_uploaded_file or sidebar_uploaded_file

# ── Main content ──────────────────────────────────────────────────────────────
if st.session_state.active_image is None:
    # Drop zone hint
    st.markdown("""
    <div class="empty-upload-state">
        <div class="empty-upload-icon">⬡</div>
        <div class="empty-upload-title">Upload an image to begin</div>
        <div class="empty-upload-text">
            Use the large upload panel above or the sidebar chooser to load a JPG or PNG.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

img_array = st.session_state.active_image
h, w = img_array.shape[:2]
max_k = min(h, w)
k = sidebar_k
uploaded_file = uploaded_file or type("UploadProxy", (), {"name": st.session_state.active_name or "image.png"})()

source_label = "Demo scene" if st.session_state.active_source == "demo" else (st.session_state.active_name or "Uploaded image")
st.markdown(
    f"""
    <div class="status-strip">
        <span class="status-chip">{source_label}</span>
        <span>·</span>
        <span>{w} × {h}px</span>
        <span>·</span>
        <span>k = {k}</span>
        <span>·</span>
        <span>compression insights are ready below</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Compute ───────────────────────────────────────────────────────────────────
with st.spinner("Decomposing…"):
    compressed_img = compress_image(img_array, k)

psnr = compute_psnr(img_array, compressed_img)
ratio = compute_compression_ratio(h, w, k)
channels = 3 if len(img_array.shape) == 3 else 1
orig_bytes = h * w * channels
comp_bytes = k * (h + w + 1) * channels
saved_pct = max(0, (1 - comp_bytes / orig_bytes) * 100)

# ── Metric Cards ─────────────────────────────────────────────────────────────
render_metrics(psnr, ratio, saved_pct, k, max_k, comp_bytes, orig_bytes)

# ── Tabs Interface ────────────────────────────────────────────────────────────
render_tabs(
    img_array=img_array,
    compressed_img=compressed_img,
    k=k,
    max_k=max_k,
    psnr=psnr,
    ratio=ratio,
    uploaded_file=uploaded_file,
    comp_bytes=comp_bytes,
    orig_bytes=orig_bytes,
    h=h,
    w=w
)