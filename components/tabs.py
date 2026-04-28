"""
components/tabs.py
Three analysis tabs: Compare · Analysis · Difference
"""

from __future__ import annotations

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from .charts import make_sv_energy_chart, make_error_heatmap
from utils   import get_singular_values, image_to_bytes


def render_tabs(
    img_array:      np.ndarray,
    compressed_img: np.ndarray,
    metrics:        dict,
    k:              int,
    filename:       str,
) -> None:
    tab1, tab2, tab3 = st.tabs(["  COMPARE  ", "  ANALYSIS  ", "  DIFFERENCE  "])

    with tab1:
        _tab_compare(img_array, compressed_img, metrics, k, filename)

    with tab2:
        _tab_analysis(img_array, k, metrics["max_k"])

    with tab3:
        _tab_difference(img_array, compressed_img)


def _tab_compare(
    img_array:      np.ndarray,
    compressed_img: np.ndarray,
    metrics:        dict,
    k:              int,
    filename:       str,
) -> None:
    orig_bytes = metrics["orig_bytes"]
    comp_bytes = metrics["comp_bytes"]
    h, w       = metrics["h"], metrics["w"]
    ratio      = metrics["ratio"]

    col1, col2 = st.columns(2)

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
        stem = filename.rsplit(".", 1)[0]
        st.download_button(
            label="↓  Download compressed image",
            data=image_to_bytes(compressed_img),
            file_name=f"svd_k{k}_{stem}.png",
            mime="image/png",
        )


def _tab_analysis(img_array: np.ndarray, k: int, max_k: int) -> None:
    st.markdown("""
    <div style="font-size:12px; color:#4a5578; margin-bottom:1rem; line-height:1.8;">
        The chart shows how much <b style="color:#00e5ff">cumulative energy</b>
        is captured as more singular values are included.
        The yellow dashed line marks the current <b style="color:#fbbf24">k</b>.
        A steep early rise means the image is highly compressible.
    </div>
    """, unsafe_allow_html=True)

    sv_list = get_singular_values(img_array)
    fig     = make_sv_energy_chart(sv_list, k, max_k)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Top-10 σ value pills
    st.markdown("""
    <div style="font-size:11px; letter-spacing:2px; text-transform:uppercase;
                color:#4a5578; margin:1.5rem 0 .5rem;">Top singular values (Red channel)</div>
    """, unsafe_allow_html=True)

    top_sv = sv_list[0][:10]
    total  = float(np.sum(sv_list[0]))
    cols   = st.columns(10)

    for i, (col, sv) in enumerate(zip(cols, top_sv)):
        pct = sv / total * 100
        with col:
            st.markdown(f"""
            <div style="background:#111520; border:1px solid #1f2a45; border-radius:6px;
                        padding:10px 6px; text-align:center;">
                <div style="font-size:9px; color:#4a5578; margin-bottom:4px;">σ<sub>{i+1}</sub></div>
                <div style="font-size:11px; color:#00e5ff; font-weight:600;">{sv:.0f}</div>
                <div style="font-size:9px; color:#4a5578; margin-top:3px;">{pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)


def _tab_difference(original: np.ndarray, compressed: np.ndarray) -> None:
    st.markdown("""
    <div style="font-size:12px; color:#4a5578; margin-bottom:1rem; line-height:1.8;">
        Bright pixels indicate large per-pixel errors.
        Edges and fine textures are typically the last features captured by SVD.
    </div>
    """, unsafe_allow_html=True)

    _, col_center, _ = st.columns([2, 3, 2])
    with col_center:
        fig = make_error_heatmap(original, compressed)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # Per-channel MAE bars
    st.markdown("""
    <div style="font-size:11px; letter-spacing:2px; text-transform:uppercase;
                color:#4a5578; margin:1.5rem 0 .5rem;">Mean Absolute Error per channel</div>
    """, unsafe_allow_html=True)

    ch_colors = ["#ff6b6b", "#34d399", "#00e5ff"]
    ch_labels = ["Red", "Green", "Blue"]

    for col, color, label, i in zip(st.columns(3), ch_colors, ch_labels, range(3)):
        mae     = float(np.mean(np.abs(
            original[:, :, i].astype(np.float64) - compressed[:, :, i].astype(np.float64)
        )))
        bar_pct = min(100, mae / 50 * 100)
        with col:
            st.markdown(f"""
            <div style="background:#111520; border:1px solid #1f2a45;
                        border-radius:8px; padding:14px 16px;">
                <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase;
                            color:#4a5578; margin-bottom:6px;">{label}</div>
                <div style="font-size:22px; font-weight:700; color:{color};
                            font-family:'Syne',sans-serif;">{mae:.2f}</div>
                <div style="font-size:10px; color:#4a5578; margin-bottom:8px;">
                    avg pixel error / 255
                </div>
                <div class="quality-bar-wrap">
                    <div class="quality-bar-fill"
                         style="width:{bar_pct:.0f}%; background:{color}; opacity:.7;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)