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
                This web app turns Singular Value Decomposition (SVD) into an interactive visual
                playground. It keeps the strongest image patterns and removes the less important
                detail so you can see the trade-off between quality and size in real time.
            </p>
            <p>
                Use the main upload card for the fastest start, or try the built-in demo scene to
                explore the app immediately. Then choose a rank <b>k</b> to control how many
                singular values are preserved. Lower values create stronger compression, while
                higher values keep the reconstruction closer to the original.
            </p>
            <p>
                The app also reports PSNR, compression ratio, retained energy, and side-by-side
                comparison views so you can study how the approximation changes across color
                channels.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_start() -> None:
    """Render a compact three-step getting-started section."""
    st.markdown(
        """
        <div class="section-header">
            <div class="section-dot"></div>
            <div class="section-title">Quick Start</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="start-grid">
            <div class="start-card">
                <div class="start-step">01</div>
                <div class="start-title">Upload</div>
                <div class="start-text">Drop a JPG or PNG on the main page or launch the demo scene.</div>
            </div>
            <div class="start-card">
                <div class="start-step">02</div>
                <div class="start-title">Choose k</div>
                <div class="start-text">Use the sidebar slider or the preset buttons to tune compression.</div>
            </div>
            <div class="start-card">
                <div class="start-step">03</div>
                <div class="start-title">Compare</div>
                <div class="start-text">Inspect PSNR, ratio, energy, and the reconstructed image panels.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_main_upload_panel() -> tuple[object | None, bool]:
    """Render the main-page upload card and return the uploaded file and demo action."""
    st.markdown(
        """
        <div class="section-header">
            <div class="section-dot"></div>
            <div class="section-title">Upload Image</div>
        </div>
        <div class="upload-card upload-card-hero upload-card-shimmer">
            <div class="upload-card-title">Main page uploader</div>
            <div class="upload-card-text">
                Use this uploader for the fastest start. You can also try the demo scene if you want
                to explore the charts and compression controls without uploading a file first.
            </div>
            <div class="upload-tip-chip">
                Switch between upload and demo mode whenever you want.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    use_demo = st.radio(
        "Start mode",
        options=["Upload image", "Demo scene"],
        horizontal=True,
        key="main_page_mode",
        help="Switch to the demo scene if you want to explore without uploading first.",
    )
    if use_demo == "Demo scene":
        st.markdown(
            """
            <div class="upload-tip-chip">Demo scene ready — charts and controls stay active.</div>
            """,
            unsafe_allow_html=True,
        )
        return None, True

    return st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png"],
        key="main_page_uploader",
        label_visibility="visible",
        help="Drag and drop an image here, or browse files to upload.",
    ), False


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