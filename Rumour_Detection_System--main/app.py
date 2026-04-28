# =========================
# Rumour Detection System - Streamlit App
# =========================
import streamlit as st
import pickle
import speech_recognition as sr

from UI.theme import apply_theme
from UI.home import render_home_selector, render_back_button
from UI.components import render_bullets_bold
from UI.result_view import render_analysis_result
from UI.history_view import render_history

from UI.headline_view import render_headline_view
from UI.text_view import render_text_view
from UI.url_view import render_url_view

from utils.config import TRUSTED_SOURCES, TRUSTED_RSS_FEEDS
from utils.text_utils import domain_from_url
from utils.article_extractor import fetch_news_from_url
from utils.stance import stance_from_text
from utils.scoring import model_agreement_line
from utils.analysis_engine import analyze_news


# =====================================================
# ---------------- PAGE CONFIG ------------------------
# =====================================================

st.set_page_config(page_title="Rumour Detection System", page_icon="logo.png", layout="wide")
apply_theme()

st.markdown("""
<style>
.zig-h span{
    text-decoration-line: underline;
    text-decoration-style: wavy;
    text-decoration-color: #6C7A52;   /* dark of #D7E4C1 */
    text-underline-offset: 6px;
}
.zig-t span{
    text-decoration-line: underline;
    text-decoration-style: wavy;
    text-decoration-color: #2D5A7A;   /* dark of #D6EFFF */
    text-underline-offset: 6px;
}
.zig-u span{
    text-decoration-line: underline;
    text-decoration-style: wavy;
    text-decoration-color: #B08B2D;   /* dark of #FFFACD */
    text-underline-offset: 6px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# ---------------- LOAD MODEL -------------------------
# =====================================================

@st.cache_resource
def load_model():
    model_local = pickle.load(open("model/model.pkl", "rb"))
    vectorizer_local = pickle.load(open("model/tfidf.pkl", "rb"))
    return model_local, vectorizer_local

try:
    model, vectorizer = load_model()
except:
    st.error("Model files not found.")
    st.stop()


# =====================================================
# ---------------- SESSION STATE ----------------------
# =====================================================

st.session_state.setdefault("history", [])
st.session_state.setdefault("voice_text", "")
st.session_state.setdefault("user_input", "")
st.session_state.setdefault("headline_input", "")
st.session_state.setdefault("extracted_text", "")
st.session_state.setdefault("url_input", "")
st.session_state.setdefault("mode", None)


# =====================================================
# ---------------- HELPERS ----------------------------
# =====================================================

def get_voice_input():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        return r.recognize_google(audio, language="en-IN")
    except:
        st.warning("Voice input failed.")
        return ""


def analyze_and_render(user_input: str):
    if not (user_input or "").strip():
        st.warning("Please enter text or extract article.")
        return

    with st.spinner("Analyzing..."):
        result = analyze_news(
            user_input=user_input,
            model=model,
            vectorizer=vectorizer,
            trusted_sources=TRUSTED_SOURCES,
            max_hits=10,
            per_domain_hits=5,
        )

    if not result.get("ok"):
        st.error("Analysis failed.")
        return

    render_analysis_result(
        result=result,
        render_bullets_bold=render_bullets_bold,
        stance_from_text=stance_from_text,
        domain_from_url=domain_from_url,
        trusted_rss_feeds=TRUSTED_RSS_FEEDS,
        model_agreement_line=model_agreement_line,
    )


# =====================================================
# ---------------- UI -------------------------------
# =====================================================

mode = render_home_selector()
if mode is not None:
    render_back_button()

if mode == "headline":
    render_headline_view(analyze_and_render=analyze_and_render)

elif mode == "text":
    render_text_view(get_voice_input=get_voice_input, analyze_and_render=analyze_and_render)

elif mode == "url":
    render_url_view(fetch_news_from_url=fetch_news_from_url, analyze_and_render=analyze_and_render)

# HISTORY
render_history()
