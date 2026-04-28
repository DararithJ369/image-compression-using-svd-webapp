"""
components/header.py
Hero banner and collapsible SVD overview.
"""

import streamlit as st


def render_hero() -> None:
    """Full-width hero title block."""
    st.markdown("""
    <div style="padding: 2.5rem 0 1rem;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:11px;
                    letter-spacing:4px; color:#4a5578; text-transform:uppercase;
                    margin-bottom:8px;">
            LINEAR ALGEBRA · IMAGE PROCESSING
        </div>
        <div style="font-family:'Syne',sans-serif; font-size:42px; font-weight:800;
                    color:#c9d1e8; line-height:1; margin-bottom:6px;">
            SVD Compression <span style="color:#00e5ff;">Lab</span>
        </div>
        <div style="font-size:13px; color:#4a5578; font-family:'JetBrains Mono',monospace;">
            Singular Value Decomposition · Real-time image reconstruction
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_overview() -> None:
    """Collapsible math explainer."""
    with st.expander("▸  How SVD Compression Works", expanded=False):
        st.markdown("""
        <div class="overview-box">
            <b>Singular Value Decomposition (SVD)</b> factorizes any matrix <b>A</b> into three matrices:<br>
            <span class="math-pill">A = U · Σ · Vᵀ</span><br><br>
            For an image of size <b>h × w</b>, each color channel is treated as a matrix.
            SVD decomposes it into <b>U</b> (h×h), <b>Σ</b> (diagonal, h×w), and <b>Vᵀ</b> (w×w),
            where the singular values in <b>Σ</b> are sorted in descending order of importance.<br><br>
            By keeping only the top <b>k</b> singular values, we reconstruct an approximation:<br>
            <span class="math-pill">Aₖ = Uₖ · Σₖ · Vₖᵀ</span><br><br>
            <b>Memory trade-off:</b> The original image needs <b>h × w</b> values per channel.
            The rank-k approximation needs only <b>k(h + w + 1)</b> values — a significant
            reduction when k is small relative to min(h, w).
        </div>
        """, unsafe_allow_html=True)


def render_empty_state() -> None:
    """Placeholder shown before an image is uploaded."""
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center;
                justify-content:center; height:380px; margin-top:2rem;
                background:#111520; border:2px dashed #1f2a45; border-radius:16px;">
        <div style="font-size:48px; margin-bottom:16px; opacity:.4">⬡</div>
        <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:600;
                    color:#4a5578; letter-spacing:2px;">
            Upload an image to begin
        </div>
        <div style="font-size:12px; color:#2a3455; margin-top:8px;
                    font-family:'JetBrains Mono',monospace;">
            JPG · PNG  —  use the sidebar uploader
        </div>
    </div>
    """, unsafe_allow_html=True)