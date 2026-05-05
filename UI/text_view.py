# =========================
# UI/text_view.py
# =========================
import streamlit as st


def render_text_view(get_voice_input, analyze_and_render):
    st.markdown("<h3 class='zig-t'><span>Analyze by Article / Text</span></h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🎤", key="mic_btn"):
            voice_text = get_voice_input()
            if voice_text:
                st.session_state.voice_text = voice_text

    user_input_text = st.text_area(
        "Enter Article Text to analyze (or paste full news)",
        value=st.session_state.voice_text,
        height=180
    )

    if user_input_text:
        st.session_state.user_input = user_input_text

    st.session_state.voice_text = ""

    if st.button("Analyze News (Text)", use_container_width=True, key="verify_text_btn"):
        analyze_and_render(st.session_state.user_input)