import streamlit as st

def render_bullets_bold(bullets, limit=8):
    for b in (bullets or [])[:limit]:
        st.markdown(
            f"""
            <div style="font-size:18px; font-weight:700; margin-bottom:6px; color:#6b21a8;">
                • {b}
            </div>
            """,
            unsafe_allow_html=True
        )