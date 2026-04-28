import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_history():
    st.divider()
    st.subheader("Recent Searches")

    if not st.session_state.get("history"):
        st.info("No searches yet.")
        return

    df = pd.DataFrame(st.session_state.history)

    real_count = df[df["result"].str.contains("Real", case=False)].shape[0]
    fake_count = df[df["result"].str.contains("Fake|Misleading", case=False, regex=True)].shape[0]
    uncertain_count = df[df["result"].str.contains("Mixed|Unclear", case=False, regex=True)].shape[0]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=["REAL"], y=[real_count], marker_color="blue", name="REAL"))
    fig_bar.add_trace(go.Bar(x=["FAKE"], y=[fake_count], marker_color="red", name="FAKE"))
    if uncertain_count > 0:
        fig_bar.add_trace(go.Bar(x=["UNCERTAIN"], y=[uncertain_count], marker_color="orange", name="UNCERTAIN"))

    fig_bar.update_layout(
        showlegend=True,
        title="Prediction Distribution",
        xaxis_title="Category",
        yaxis_title="Count"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    for item in st.session_state.history:
        st.write(f"{item['headline']} → {item['result']} (Evidence Strength: {item['confidence']}%)")