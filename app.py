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
from utils.io import load_css, image_to_bytes
from components.header import render_hero, render_app_intro, render_overview
from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.tabs import render_tabs


def load_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    max_k = min(height, width)
    return img_array, height, width, max_k

# ── Custom CSS ────────────────────────────────────────────────────────────
css_content = load_css("styles/theme.css")
if css_content:
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# ── Hero + Overview ───────────────────────────────────────────────────────────
render_hero()
render_app_intro()
render_overview()

# ── Main-page upload ───────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="section-header">
        <div class="section-dot"></div>
        <div class="section-title">Quick Upload</div>
    </div>
    <div class="upload-card">
        <div class="upload-card-title">Upload on the main page</div>
        <div class="upload-card-text">
            Drag and drop a JPG or PNG here to start exploring image compression.
            You can still use the sidebar uploader and controls if you prefer that layout.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
main_uploaded_file = st.file_uploader(
    "Upload file on the main page",
    type=["jpg", "jpeg", "png"],
    key="main_page_uploader",
    label_visibility="visible",
    help="Click Browse files to upload an image from the main page.",
)

# ── Sidebar Controls ──────────────────────────────────────────────────────────
sidebar_uploaded_file, sidebar_img_array, sidebar_k, sidebar_h, sidebar_w, sidebar_max_k = render_sidebar()

uploaded_file = main_uploaded_file or sidebar_uploaded_file

# ── Main content ──────────────────────────────────────────────────────────────
if uploaded_file is None:
    # Drop zone hint
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center;
                justify-content:center; height:380px; margin-top:2rem;
                background:#111520; border:2px dashed #1f2a45; border-radius:16px;">
        <div style="font-size:48px; margin-bottom:16px; opacity:.4">⬡</div>
        <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:600;
                    color:#4a5578; letter-spacing:2px;">
            Upload an image to begin
        </div>
        <div style="font-size:12px; color:#2a3455; margin-top:8px; font-family:'JetBrains Mono',monospace;">
            JPG · PNG  —  use the sidebar uploader
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if main_uploaded_file is not None:
    img_array, h, w, max_k = load_image(main_uploaded_file)
    k = st.slider(
        "Rank k  (singular values to keep)",
        min_value=1,
        max_value=max_k,
        value=max(1, int(max_k * 0.1)),
        help="Lower = more compression. Higher = closer to original.",
        key="main_page_rank_slider",
    )
else:
    img_array, h, w, max_k, k = sidebar_img_array, sidebar_h, sidebar_w, sidebar_max_k, sidebar_k

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