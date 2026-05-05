# =========================
# UI/headline_view.py
# =========================
import streamlit as st


def render_headline_view(analyze_and_render):
    st.markdown("<h3 class='zig-h'><span>Analyze by Headline</span></h3>", unsafe_allow_html=True)

    headline = st.text_input(
        "Enter the headline to analyze",
        value=st.session_state.headline_input,
        placeholder="e.g., Trump Tariffs Live Updates: ...",
    )
    st.session_state.headline_input = headline

    if st.button("Analyze Headline", use_container_width=True, key="verify_headline_btn"):
        analyze_and_render(st.session_state.headline_input)