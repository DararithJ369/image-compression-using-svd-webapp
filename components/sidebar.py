"""
components/sidebar.py
Sidebar: file uploader, rank-k slider, and info panel.

Uses st.sidebar.xxx directly (not the `with st.sidebar:` context manager)
which is the most reliable way to render sidebar content across all
Streamlit versions.
"""

from __future__ import annotations

import numpy as np
import streamlit as st
from PIL import Image


def render_sidebar() -> tuple[object | None, np.ndarray | None, int | None]:
    """
    Render the sidebar controls.

    Returns
    -------
    uploaded_file : UploadedFile | None
    img_array     : np.ndarray | None   — RGB uint8 array
    k             : int | None          — selected rank
    """
    st.sidebar.markdown(
        """
        <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:800;
                    color:#00e5ff; padding:0.5rem 0 1rem;">⟁ Controls</div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.sidebar.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"],
        label_visibility="visible",
    )

    if uploaded_file is None:
        return None, None, None

    # ── Image loaded ──────────────────────────────────────────────────────────
    img       = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)
    h, w      = img_array.shape[:2]
    max_k     = min(h, w)

    st.sidebar.markdown("---")

    k = st.sidebar.slider(
        "Rank k  (singular values to keep)",
        min_value=1,
        max_value=max_k,
        value=max(1, int(max_k * 0.1)),
        help="Lower = more compression.  Higher = closer to original.",
    )

    # Quick energy estimate on the red channel (single cheap SVD)
    _, S, _ = np.linalg.svd(
        img_array[:, :, 0].astype(np.float64), full_matrices=False
    )
    energy_pct = float(np.cumsum(S)[k - 1] / np.sum(S) * 100)
    pct_k      = k / max_k * 100

    st.sidebar.markdown(
        f"""
        <div class="sidebar-info">
            <b>Image size:</b> {w} × {h} px<br>
            <b>Max rank:</b> {max_k}<br>
            <b>Using:</b> {pct_k:.1f}% of components<br>
            <b>Energy retained (R ch):</b> {energy_pct:.1f}%
        </div>
        """,
        unsafe_allow_html=True,
    )

    return uploaded_file, img_array, k