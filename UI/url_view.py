# =========================
# UI/url_view.py
# =========================
import streamlit as st


def render_url_view(fetch_news_from_url, analyze_and_render):
    st.markdown("<h3 class='zig-u'><span>Analyze by URL (Extract Article Automatically)</span></h3>", unsafe_allow_html=True)

    url_input = st.text_input("Paste News URL to analyze", value=st.session_state.url_input)
    st.session_state.url_input = url_input

    colA, colB = st.columns(2)

    with colA:
        if st.button("Extract Article", use_container_width=True, key="extract_btn"):
            if url_input.strip():
                with st.spinner("Extracting article..."):
                    extracted_text = fetch_news_from_url(url_input)

                if extracted_text:
                    st.session_state.extracted_text = extracted_text
                    st.success("✅ Article extracted. Now analyze below (no copy/paste needed).")
                else:
                    st.session_state.extracted_text = ""
                    st.error("Could not extract article.")
            else:
                st.warning("Please paste a URL first.")

    with colB:
        if st.button("Analyze this Article (URL)", use_container_width=True, key="verify_url_btn"):
            if st.session_state.extracted_text.strip():
                analyze_and_render(st.session_state.extracted_text)
            else:
                st.warning("Please extract the article first.")

    if st.session_state.extracted_text.strip():
        with st.expander("📄 View Extracted Article (Click to expand)", expanded=False):
            st.text_area("Extracted Article", st.session_state.extracted_text, height=250)