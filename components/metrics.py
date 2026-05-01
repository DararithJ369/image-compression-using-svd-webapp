"""Four metric cards display."""
import streamlit as st


def render_metrics(psnr: float, ratio: float, saved_pct: float, 
                   k: int, max_k: int, comp_bytes: int, orig_bytes: int) -> None:
    """Render the 4 metric cards."""
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card c1">
            <div class="metric-label">Compression Ratio</div>
            <div class="metric-value">{ratio:.1f}×</div>
            <div class="metric-sub">lower k → higher ratio</div>
        </div>
        <div class="metric-card c2">
            <div class="metric-label">PSNR</div>
            <div class="metric-value">{psnr:.1f}<span style="font-size:14px;font-weight:400"> dB</span></div>
            <div class="metric-sub">&gt;40 dB ≈ excellent quality</div>
        </div>
        <div class="metric-card c3">
            <div class="metric-label">Space Saved</div>
            <div class="metric-value">{saved_pct:.0f}<span style="font-size:14px;font-weight:400">%</span></div>
            <div class="metric-sub">{comp_bytes:,} vs {orig_bytes:,} values</div>
        </div>
        <div class="metric-card c4">
            <div class="metric-label">Rank Used</div>
            <div class="metric-value">{k}<span style="font-size:14px;font-weight:400">/{max_k}</span></div>
            <div class="metric-sub">{k/max_k*100:.1f}% of full rank</div>
        </div>
    </div>
    """, unsafe_allow_html=True)