import streamlit as st
import base64


def ensure_mode_state():
    if "mode" not in st.session_state:
        st.session_state.mode = None


def set_mode(m: str):
    st.session_state.mode = m


def go_home():
    st.session_state.mode = None


def _img_to_base64(path: str) -> str:
    """Convert local image to base64 so we can place it in HTML (mobile-safe)."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def render_home_selector():
    ensure_mode_state()

    st.markdown("""
        <style>
        .zigzag span {
            text-decoration-line: underline;
            text-decoration-style: wavy;
            text-decoration-color: #8000FF;  /* Strong Purple */
            text-underline-offset: 6px;
        }
        .block-container {
            padding-top: 0.5rem !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # 🎨 Background control
    if st.session_state.mode == "headline":
        st.markdown("<style>[data-testid='stAppViewContainer']{background-color:#D7E4C1 !important;}</style>", unsafe_allow_html=True)
    elif st.session_state.mode == "text":
        st.markdown("<style>[data-testid='stAppViewContainer']{background-color:#D6EFFF !important;}</style>", unsafe_allow_html=True)
    elif st.session_state.mode == "url":
        st.markdown("<style>[data-testid='stAppViewContainer']{background-color:#FFFACD !important;}</style>", unsafe_allow_html=True)

   
    logo_left = _img_to_base64("logo.png")
    logo_right = _img_to_base64("RDS.png")

    st.markdown("""
    <style>
      .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-top: 6px;
      }
      .topbar img {
        height: 160px;   /*  LOGO SIZE HERE */
        width: auto;
      }
    </style>
    """, unsafe_allow_html=True)

    if logo_left and logo_right:
        st.markdown(f"""
        <div class="topbar">
          <img src="data:image/png;base64,{logo_left}" alt="logo" />
          <img src="data:image/png;base64,{logo_right}" alt="RDS_logo" />
        </div>
        """, unsafe_allow_html=True)
    else:
       
        colL, colC, colR = st.columns([1, 2, 1])
        with colL:
            st.image("logo.png", width=140)
        with colC:
            st.write("")
        with colR:
            st.image("RDS_logo.png", width=140)

   
    st.markdown("""
    <div style="text-align:center; margin-top:-10px;">
        <div style="
            display:inline-block;
            background: linear-gradient(135deg, #1f2937, #111827);
            padding: 14px 28px;
            border-radius: 50px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.35);
        ">
            <h1 style="
                margin:0;
                font-size:36px;
                color:white;
                letter-spacing:0.5px;
            ">
                Rumour Detection System
            </h1>
            <div style="
                font-size:14px;
                margin-top:4px;
                color:#e5e7eb;
                letter-spacing:0.5px;
            ">
                AI + Source Transparency
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.session_state.mode is None:
        st.markdown(
            "<div style='text-align:center; font-size:18px; margin-top:15px; margin-bottom:15px;'>Choose what you want to analyze</div>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3, gap="large")

        with c1:
            st.markdown("<h3>📰 <span class='zigzag'><span>Headline</span></span></h3>", unsafe_allow_html=True)
            st.write("Analyze News Tone & Authenticity")
            st.button(
                "Select Headline",
                key="btn_headline",
                use_container_width=True,
                on_click=set_mode,
                args=("headline",)
            )

        with c2:
            st.markdown("<h3>📝 <span class='zigzag'><span>Article / Text</span></span></h3>", unsafe_allow_html=True)
            st.write("Paste full article or use voice input.")
            st.button(
                "Select Text",
                key="btn_text",
                use_container_width=True,
                on_click=set_mode,
                args=("text",)
            )

        with c3:
            st.markdown("<h3>🔗 <span class='zigzag'><span>URL</span></span></h3>", unsafe_allow_html=True)
            st.write("Paste URL → extract article automatically.")
            st.button(
                "Select URL",
                key="btn_url",
                use_container_width=True,
                on_click=set_mode,
                args=("url",)
            )

    return st.session_state.mode


def render_back_button():
    ensure_mode_state()
    if st.session_state.mode is not None:
        colA, colB = st.columns([1, 5])
        with colA:
            st.button("⬅ Back", use_container_width=True, on_click=go_home, key="btn_back")
        with colB:
            st.write("")
        st.divider()

