from utils.text_utils import domain_from_url, dedupe_items
from utils.stance import stance_from_text


def build_conflict(evidence_items: list, trusted_domains_set: set):
    evidence_items = dedupe_items(evidence_items)

    support = contradict = unclear = 0
    trusted_support = trusted_contradict = 0
    rows = []

    for it in evidence_items:
        title = it.get("title", "") or ""
        link = it.get("link", "") or ""
        src = it.get("source", "") or ""
        pub_url = it.get("publisher_url", "") or ""

        dom = domain_from_url(pub_url) or domain_from_url(link)
        is_trusted = dom in trusted_domains_set

        stance = stance_from_text(title, it.get("snippet", ""))

        if stance == "SUPPORT":
            support += 1
            if is_trusted:
                trusted_support += 1
        elif stance == "CONTRADICT":
            contradict += 1
            if is_trusted:
                trusted_contradict += 1
        else:
            unclear += 1

        rows.append({
            "source": src,
            "domain": dom if dom else "(unknown)",
            "trusted_domain": "YES" if is_trusted else "NO",
            "stance": stance,
            "title": title[:170],
            "link": link
        })

    reasons = []
    if trusted_contradict >= 2:
        verdict = "Likely Fake / Misleading"
        reasons.append("Multiple trusted sources show debunk/contradiction signals.")
    elif trusted_support >= 2 and trusted_contradict == 0:
        verdict = "Likely Real"
        reasons.append("Multiple trusted sources support it and no trusted contradictions were found.")
    elif contradict > 0 and support > 0:
        verdict = "Mixed / Unclear"
        reasons.append("Evidence includes both support and contradiction signals.")
    elif contradict > support and contradict >= 1:
        verdict = "Likely Fake / Misleading"
        reasons.append("Contradiction signals are stronger than support signals in evidence.")
    elif support > contradict and support >= 1:
        verdict = "Likely Real"
        reasons.append("Support signals are stronger than contradiction signals in evidence.")
    else:
        verdict = "Mixed / Unclear"
        reasons.append("Not enough strong stance signals in evidence.")

    reasons.append(
        f"Support: {support} (trusted: {trusted_support}) | "
        f"Contradict: {contradict} (trusted: {trusted_contradict}) | "
        f"Unclear: {unclear}"
    )

    return {
        "verdict": verdict,
        "reasons": reasons,
        "trusted_support": trusted_support,
        "trusted_contradict": trusted_contradict,
        "rows": rows
    }


def compute_evidence_strength(trusted_hits: list, google_hits: list, official_hits: list, trusted_domains_set: set):
    def _count(items):
        s = c = u = 0
        ts = tc = 0
        for it in items or []:
            title = it.get("title", "") or ""
            link = it.get("link", "") or ""
            pub_url = it.get("publisher_url", "") or ""

            dom = domain_from_url(pub_url) or domain_from_url(link)
            is_trusted = dom in trusted_domains_set
            stance = stance_from_text(title, it.get("snippet", ""))

            if stance == "SUPPORT":
                s += 1
                if is_trusted:
                    ts += 1
            elif stance == "CONTRADICT":
                c += 1
                if is_trusted:
                    tc += 1
            else:
                u += 1
        return s, c, u, ts, tc

    rss_s, rss_c, rss_u, rss_ts, rss_tc = _count(trusted_hits)
    g_s, g_c, g_u, g_ts, g_tc = _count(google_hits)
    official_count = len(official_hits or [])

    evidence_exists = (len(trusted_hits or []) + len(google_hits or []) + official_count) > 0
    score = 10.0 if evidence_exists else 0.0

    score += min(official_count, 5) * 18.0
    score += min(rss_s, 8) * 10.0
    score -= min(rss_c, 6) * 14.0
    score += min(g_ts, 6) * 6.0
    score += min(max(g_s - g_ts, 0), 6) * 2.0
    score -= min(g_tc, 6) * 10.0
    score -= min(max(g_c - g_tc, 0), 6) * 4.0

    score = max(0.0, min(100.0, score))
    if score > 95:
        score = 95.0

    return round(score, 2)


def final_label_merge(ml_label: str, ml_conf: float, conflict: dict, evidence_strength: float, official_hits: list):
    ev_verdict = conflict.get("verdict", "Mixed / Unclear")
    tc = int(conflict.get("trusted_contradict", 0))
    off_ct = len(official_hits or [])

    bullets = []
    bullets.append(f"Evidence Strength: {evidence_strength}% (RSS + Google + Official check).")
    if off_ct > 0:
        bullets.append(f"Official site confirmation: Found {off_ct} related result(s). ✅")
    else:
        bullets.append("Official site confirmation: Not found (not proof of fake). ⚠️")
    bullets.append(f"Evidence Verdict: {ev_verdict}")
    bullets.append(f"Model Prediction (Secondary): {ml_label} ({ml_conf}%).")

    if off_ct >= 1 and tc == 0 and evidence_strength >= 55:
        final = "Likely Real"
        bullets.append("Official confirmation found → final leans Real.")
        return final, bullets

    if tc >= 2:
        final = "Likely Fake / Misleading"
        bullets.append("Trusted debunk/contradictions are strong → final leans Fake.")
        return final, bullets

    if evidence_strength >= 70:
        if "fake" in ev_verdict.lower():
            final = "Likely Fake / Misleading"
        elif "real" in ev_verdict.lower():
            final = "Likely Real"
        else:
            final = "Mixed / Unclear"
        bullets.append("Evidence is strong → evidence-first decision.")
        return final, bullets

    if evidence_strength <= 30:
        if ml_label == "FAKE" and ml_conf >= 65:
            final = "Likely Fake / Misleading"
            bullets.append("Evidence is weak but model signal is strong → leaning Fake.")
        else:
            final = "Mixed / Unclear"
            bullets.append("Evidence is weak → keeping it cautious.")
        return final, bullets

    if "fake" in ev_verdict.lower():
        final = "Likely Fake / Misleading"
    elif "real" in ev_verdict.lower():
        final = "Likely Real"
    else:
        final = "Mixed / Unclear"

    bullets.append("Medium evidence → following evidence verdict.")
    return final, bullets


def model_agreement_line(final_label: str, ml_label: str):
    final_is_real = "real" in (final_label or "").lower()
    final_is_fake = "fake" in (final_label or "").lower()
    ml_is_real = (ml_label == "REAL")
    ml_is_fake = (ml_label == "FAKE")

    if (final_is_real and ml_is_real) or (final_is_fake and ml_is_fake):
        return "✅ Model agrees with the final verdict."
    if (final_is_real and ml_is_fake) or (final_is_fake and ml_is_real):
        return "⚠️ Model DISAGREES with the final verdict (final decision is evidence-first)."
    return "ℹ️ Model signal is neutral vs final verdict."