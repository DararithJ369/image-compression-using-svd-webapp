"""Hero banner and overview expander."""
import streamlit as st


def render_hero() -> None:
    """Render the hero header section."""
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


def render_app_intro() -> None:
    """Render a short landing-page description for the web app."""
    st.markdown(
        """
        <div class="hero-copy">
            <p>
                This web app shows image compression through Singular Value Decomposition (SVD)
                in a visual, interactive way. It keeps the strongest image patterns and removes
                the less important detail so you can see the trade-off between quality and size.
            </p>
            <p>
                Upload a JPG or PNG from the main page or the sidebar, then choose a rank <b>k</b>
                to control how many singular values are preserved. Lower values create stronger
                compression, while higher values keep the reconstruction closer to the original.
            </p>
            <p>
                The app also reports PSNR, compression ratio, retained energy, and side-by-side
                comparison views so you can study how the approximation changes across color channels.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview() -> None:
    """Render the SVD explanation expander."""
    with st.expander("How SVD Compression Works", expanded=False):
        st.markdown("""
        <div class="overview-box">
            <b>Singular Value Decomposition (SVD)</b> factorizes any matrix <b>A</b> into three matrices:<br>
            <span class="math-pill">A = U · Σ · Vᵀ</span><br><br>
            For an image of size <b>h × w</b>, each color channel is treated as a matrix.
            SVD decomposes it into <b>U</b> (h×h), <b>Σ</b> (diagonal, h×w), and <b>Vᵀ</b> (w×w),
            where the singular values in <b>Σ</b> are sorted in descending order of importance.<br><br>
            By keeping only the top <b>k</b> singular values, we reconstruct an approximation:<br>
            <span class="math-pill">Aₖ = Uₖ · Σₖ · Vₖᵀ</span><br><br>
            <b>Memory trade-off:</b> Original image needs <b>h × w</b> values per channel.
            The rank-k approximation needs only <b>k(h + w + 1)</b> values — a significant
            reduction when k is small relative to min(h, w).
        </div>
        """, unsafe_allow_html=True)