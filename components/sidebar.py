"""Sidebar controls: file upload and k slider."""
import streamlit as st
import numpy as np
from PIL import Image


def render_sidebar():
    """
    Render sidebar controls.
    
    Returns:
        tuple: (uploaded_file, img_array, k, h, w, max_k) or (None, None, None, None, None, None)
    """
    st.sidebar.markdown("""
    <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:800;
                color:#00e5ff; padding: 0.5rem 0 1rem;">⟁ Controls</div>
    """, unsafe_allow_html=True)

    uploaded_file = st.sidebar.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"],
        label_visibility="visible"
    )

    if uploaded_file is None:
        return None, None, None, None, None, None

    img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)
    h, w = img_array.shape[:2]
    max_k = min(h, w)

    st.sidebar.markdown("---")
    k = st.sidebar.slider(
        "Rank k  (singular values to keep)",
        min_value=1,
        max_value=max_k,
        value=max(1, int(max_k * 0.1)),
        help="Lower = more compression. Higher = closer to original."
    )

    # Energy retained at k (using red channel as proxy)
    _, S, _ = np.linalg.svd(img_array[:, :, 0].astype(np.float64), full_matrices=False)
    energy_pct = np.cumsum(S)[k - 1] / np.sum(S) * 100
    pct_k = k / max_k * 100

    st.sidebar.markdown(f"""
    <div class="sidebar-info">
        <b>Image size:</b> {w} × {h} px<br>
        <b>Max rank:</b> {max_k}<br>
        <b>Using:</b> {pct_k:.1f}% of components<br>
        <b>Energy retained (R ch):</b> {energy_pct:.1f}%
    </div>
    """, unsafe_allow_html=True)

    return uploaded_file, img_array, k, h, w, max_k