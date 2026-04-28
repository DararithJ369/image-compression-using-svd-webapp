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

from pathlib import Path

import streamlit as st

from utils import compress_image, compute_metrics, load_css
from components import (
    render_hero,
    render_overview,
    render_empty_state,
    render_sidebar,
    render_metrics,
    render_tabs,
)

st.set_page_config(
    page_title="SVD Compression Lab",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS_PATH = Path(__file__).parent / "styles" / "theme.css"
st.markdown(f"<style>{load_css(CSS_PATH)}</style>", unsafe_allow_html=True)

render_hero()
render_overview()

uploaded_file, img_array, k = render_sidebar()

if uploaded_file is None or img_array is None or k is None:
    render_empty_state()
    st.stop()

with st.spinner("Decomposing…"):
    compressed_img = compress_image(img_array, k)

metrics = compute_metrics(img_array, compressed_img, k)

render_metrics(metrics, k)
render_tabs(img_array, compressed_img, metrics, k, uploaded_file.name)