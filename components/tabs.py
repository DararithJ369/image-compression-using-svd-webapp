"""Three-tab interface: Compare, Analysis, Difference."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from utils.svd import get_singular_values
from utils.io import image_to_bytes
from components.charts import make_sv_chart, make_error_map


def render_tabs(img_array: np.ndarray, compressed_img: np.ndarray, 
                k: int, max_k: int, psnr: float, ratio: float,
                uploaded_file, comp_bytes: int, orig_bytes: int,
                h: int, w: int) -> None:
    """Render the three main tabs."""
    tab1, tab2, tab3 = st.tabs(["  COMPARE  ", "  ANALYSIS  ", "  DIFFERENCE  "])

    # ── TAB 1 · Side-by-side ──────────────────────────────────────────────────
    with tab1:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("""
            <div class="img-panel-title">
                <span>Original</span>
                <span class="badge">FULL RANK</span>
            </div>
            """, unsafe_allow_html=True)
            st.image(img_array, use_container_width=True)
            st.markdown(f"""
            <div style="font-size:11px; color:#4a5578; margin-top:6px; text-align:center;">
                {w} × {h} · {orig_bytes:,} values/channel
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="img-panel-title">
                <span>Compressed</span>
                <span class="badge red">k = {k}</span>
            </div>
            """, unsafe_allow_html=True)
            st.image(compressed_img, use_container_width=True)
            st.markdown(f"""
            <div style="font-size:11px; color:#4a5578; margin-top:6px; text-align:center;">
                {comp_bytes:,} values/channel · {ratio:.1f}× smaller
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            st.download_button(
                label="↓  Download compressed image",
                data=image_to_bytes(compressed_img),
                file_name=f"svd_k{k}_{uploaded_file.name.split('.')[0]}.png",
                mime="image/png",
            )

    # ── TAB 2 · Singular value analysis ──────────────────────────────────────
    with tab2:
        st.markdown("""
        <div style="font-size:12px; color:#4a5578; margin-bottom:1rem; line-height:1.8;">
            The chart below shows how much <b style="color:#00e5ff">cumulative energy</b>
            is captured as we include more singular values.
            The yellow dashed line marks the currently selected <b style="color:#fbbf24">k</b>.
            A steep early rise means the image is highly compressible.
        </div>
        """, unsafe_allow_html=True)

        sv_list = get_singular_values(img_array)
        fig = make_sv_chart(sv_list, k, max_k)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # Top-10 singular values table
        st.markdown("""
        <div style="font-size:11px; letter-spacing:2px; text-transform:uppercase;
                    color:#4a5578; margin:1.5rem 0 .5rem;">Top singular values (Red channel)</div>
        """, unsafe_allow_html=True)
        top_sv = sv_list[0][:10]
        total = np.sum(sv_list[0])
        top_rows = [top_sv[i:i + 5] for i in range(0, len(top_sv), 5)]
        for row_index, row in enumerate(top_rows):
            cols = st.columns(len(row), gap="medium")
            for i, (col, sv) in enumerate(zip(cols, row), start=row_index * 5):
                with col:
                    pct = sv / total * 100
                    st.markdown(f"""
                    <div style="background:#111520; border:1px solid #1f2a45; border-radius:8px;
                                padding:12px 8px; text-align:center; min-height:88px;">
                        <div style="font-size:9px; color:#4a5578; margin-bottom:4px;">σ<sub>{i+1}</sub></div>
                        <div style="font-size:12px; color:#00e5ff; font-weight:600;">{sv:.0f}</div>
                        <div style="font-size:9px; color:#4a5578; margin-top:3px;">{pct:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── TAB 3 · Difference map ───────────────────────────────────────────────
    with tab3:
        st.markdown("""
        <div style="font-size:12px; color:#4a5578; margin-bottom:1rem; line-height:1.8;">
            Bright pixels indicate large per-pixel errors between the original and compressed images.
            Edges and fine textures are typically the last to be captured by SVD.
        </div>
        """, unsafe_allow_html=True)

        fig2 = make_error_map(img_array, compressed_img)
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

        # Per-channel MAE
        st.markdown("""
        <div style="font-size:11px; letter-spacing:2px; text-transform:uppercase;
                    color:#4a5578; margin:1.5rem 0 .5rem;">Mean Absolute Error per channel</div>
        """, unsafe_allow_html=True)
        ch_colors = ['#ff6b6b', '#34d399', '#00e5ff']
        ch_labels = ['Red', 'Green', 'Blue']
        ch_cols = st.columns(3, gap="large")
        for i, (col, color, label) in enumerate(zip(ch_cols, ch_colors, ch_labels)):
            mae = np.mean(np.abs(
                img_array[:, :, i].astype(np.float64) - compressed_img[:, :, i].astype(np.float64)
            ))
            bar_pct = min(100, mae / 50 * 100)
            with col:
                st.markdown(f"""
                <div style="background:#111520; border:1px solid #1f2a45; border-radius:8px; padding:14px 16px;">
                    <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase;
                                color:#4a5578; margin-bottom:6px;">{label}</div>
                    <div style="font-size:22px; font-weight:700; color:{color}; font-family:'Syne',sans-serif;">
                        {mae:.2f}
                    </div>
                    <div style="font-size:10px; color:#4a5578; margin-bottom:8px;">avg pixel error / 255</div>
                    <div class="quality-bar-wrap">
                        <div class="quality-bar-fill"
                             style="width:{bar_pct:.0f}%; background:{color}; opacity:.7;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)