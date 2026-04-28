import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_analysis_result(
    result: dict,
    render_bullets_bold,
    stance_from_text,
    domain_from_url,
    trusted_rss_feeds: dict,
    model_agreement_line,
):
    """
    Renders:
    - Final Verdict cards
    - Evidence meter
    - Why bullets
    - Official check
    - Trusted RSS hits
    - Google News hits
    - Evidence breakdown table
    Also updates st.session_state.history
    """

    final_label = result["final_label"]
    evidence_strength = result["evidence_strength"]
    ml_label = result["ml_label"]
    confidence = result["ml_conf"]

    official_hits = result["official_hits"]
    official_domains = result["official_domains"]
    trusted_hits = result["trusted_hits"]
    google_hits = result["google_hits"]
    trusted_domains_set = result["trusted_domains_set"]
    conflict = result["conflict"]
    bullets = result["bullets"]

    
    st.subheader("✨ Final Analysis Result")

   
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Final Label", final_label)
    with c2:
        st.metric("Evidence Strength", f"{evidence_strength}%")
    with c3:
        st.metric("Official Check", "FOUND ✅" if len(official_hits) > 0 else "NOT FOUND ⚠️")

  
    
    if "Likely Real" in final_label:
        st.success(f"✅ FINAL: {final_label}")
    elif "Fake" in final_label or "Misleading" in final_label:
        st.error(f"❌ FINAL: {final_label}")
    else:
        st.warning(f"⚠️ FINAL: {final_label}")

   
    st.info(model_agreement_line(final_label, ml_label))

    fig_ev = go.Figure(go.Indicator(
        mode="gauge+number",
        value=evidence_strength,
        title={"text": "Evidence Strength Meter"},
        gauge={"axis": {"range": [0, 100]}}
    ))
    st.plotly_chart(fig_ev, use_container_width=True)

    st.markdown("### 🧾 Why (Explainable)")
    render_bullets_bold(bullets, limit=8)

    st.warning("⚠️ Please verify once manually using the links below before believing/sharing.")
    st.markdown("---")

    with st.expander("🧠 Model Signal Details (Secondary - for transparency)", expanded=False):
        st.write("This is NOT the final verdict. Final decision above is evidence-first.")
        st.markdown(f"**Model Signal:** `{ml_label}`  |  **Model Confidence:** `{confidence}%`")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            title={"text": "Model Confidence"},
            gauge={"axis": {"range": [0, 100]}}
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏛️ Official Website Check (Auto)")
    if official_domains:
        st.info("Detected official domains: " + ", ".join(official_domains))
    else:
        st.info("No official authority detected in text (UGC/RBI/PIB/WHO/CDC/gov).")

    if official_hits:
        st.success("Official-related results found (via site:domain search):")
        for it in official_hits[:10]:
            st.markdown(f"✅ **[{it['title']}]({it['link']})**  _(Domain: {it['domain']})_")
    else:
        st.write("No official post found from detected authority sites (this is NOT proof of fake).")

    st.subheader("📰 Trusted Evidence Matches (From Publisher RSS)")
    if trusted_hits:
        for item in trusted_hits:
            stance = stance_from_text(item.get("title", ""))
            badge = "✅ SUPPORT" if stance == "SUPPORT" else ("❌ CONTRADICT" if stance == "CONTRADICT" else "⚠️ UNCLEAR")
            st.markdown(
                f"{badge} — **[{item['title']}]({item['link']})**  "
                f"_(Source: {item['source']}, Match: {item['score']}%)_"
            )
    else:
        st.write("No strong matches found in trusted RSS feeds.")

    st.info(f"Trusted RSS hits: {len(trusted_hits)} | Checked Feeds: {len(trusted_rss_feeds)}")

    st.subheader("🌐 Google News (Live Search Results)")
    if google_hits:
        for item in google_hits:
            pub_dom = domain_from_url(item.get("publisher_url", "")) or domain_from_url(item.get("link", ""))
            is_trusted_dom = pub_dom in trusted_domains_set
            stance = stance_from_text(item.get("title", ""))

            if stance == "SUPPORT":
                s_badge = "✅ SUPPORT"
            elif stance == "CONTRADICT":
                s_badge = "❌ CONTRADICT"
            else:
                s_badge = "⚠️ UNCLEAR"

            if is_trusted_dom:
                st.markdown(
                    f"✅ **[TRUSTED] {s_badge} — [{item['title']}]({item['link']})**  "
                    f"_(Publisher: {item.get('source','Google News')}, Domain: {pub_dom if pub_dom else 'unknown'})_"
                )
            else:
                st.markdown(
                    f"🔗 **{s_badge} — [{item['title']}]({item['link']})**  "
                    f"_(Publisher: {item.get('source','Google News')}, Domain: {pub_dom if pub_dom else 'unknown'})_"
                )
    else:
        st.write("Google News returned no results (temporary / network / rate-limit).")

    df_conf = pd.DataFrame(conflict.get("rows", []))
    if not df_conf.empty:
        with st.expander("🔍 See evidence stance breakdown (Support / Contradict / Unclear)"):
            st.dataframe(df_conf, use_container_width=True)

    st.markdown("---")
    st.warning("""
⚠️ **Important Notice – Manual Verification Required**

This system provides an AI-based prediction using machine learning techniques.  
It may not always be 100% accurate.

🔎 Please verify the news using trusted sources before sharing or believing it.  
❗ Do not rely solely on the AI model's output.
""")

    st.session_state.history.insert(0, {
        "headline": (result.get("translated") or "")[:120],
        "result": final_label,
        "confidence": evidence_strength
    })
    st.session_state.history = st.session_state.history[:10]