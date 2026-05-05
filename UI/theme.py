import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #f3e8ff; }
        section.main > div { background-color: #f3e8ff; }

        div.stButton > button {
            background-color: #ffffff;
            border: 1px solid #d8b4fe;
            border-radius: 10px;
            font-weight: 600;
        }
        div.stButton > button:hover {
            background-color: #ede9fe;
            border: 1px solid #a855f7;
        }

        .stTextInput > div > div > input,
        .stTextArea textarea {
            background-color: #ffffff;
            border: 1px solid #d8b4fe;
        }
        </style>
    """, unsafe_allow_html=True)