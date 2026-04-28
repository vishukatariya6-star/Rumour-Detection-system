import re
from langdetect import detect
from deep_translator import GoogleTranslator

from utils.text_utils import clean_text
from utils.news_search import (
    search_trusted_rss,
    google_news_rss_search,
    detect_official_domains,
    search_official_sites_via_google_news,
)
from utils.scoring import (
    build_conflict,
    compute_evidence_strength,
    final_label_merge,
)


def _safe_detect_lang(text: str) -> str:
    try:
        return detect(text)
    except:
        return "en"


def _safe_translate_to_en(text: str, lang: str) -> str:
    try:
        if lang != "en":
            return GoogleTranslator(source="auto", target="en").translate(text)
        return text
    except:
        return text


def _ml_predict(model, vectorizer, translated_text: str):
    cleaned = clean_text(translated_text)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]

    confidence = 50.0
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(vectorized)[0]
        try:
            cls_list = list(model.classes_)
            idx_fake = cls_list.index(0)
            idx_real = cls_list.index(1)
        except:
            idx_fake, idx_real = 0, 1

        fake_prob = float(proba[idx_fake])
        real_prob = float(proba[idx_real])
        confidence = (real_prob if prediction == 1 else fake_prob) * 100.0

    confidence = round(float(confidence), 2)
    ml_label = "REAL" if prediction == 1 else "FAKE"
    return ml_label, confidence, cleaned


def analyze_news(
    user_input: str,
    model,
    vectorizer,
    trusted_sources: list,
    max_hits: int = 10,
    per_domain_hits: int = 5,
):
    """
    Pure analysis engine:
    - language detect + translate
    - ML predict
    - RSS searches
    - official site check
    - scoring + final merge
    Returns a dict for UI rendering.
    """

    user_input = (user_input or "").strip()
    if not user_input:
        return {"ok": False, "error": "EMPTY_INPUT"}

    lang = _safe_detect_lang(user_input)
    translated = _safe_translate_to_en(user_input, lang)

    # ML
    ml_label, ml_conf, cleaned = _ml_predict(model, vectorizer, translated)

    # keywords for search
    keywords = " ".join((translated or "").split()[:12])
    keywords = re.sub(r"[^a-zA-Z0-9\s]", "", keywords).strip()

    # evidence searches
    trusted_hits = search_trusted_rss(keywords, max_hits=max_hits)
    google_hits = google_news_rss_search(keywords, max_hits=max_hits)

    official_domains = detect_official_domains(translated)
    official_hits = (
        search_official_sites_via_google_news(keywords, official_domains, per_domain_hits=per_domain_hits)
        if official_domains
        else []
    )

    trusted_domains_set = set([d.lower().replace("www.", "") for d in trusted_sources])

    combined_evidence = []
    combined_evidence.extend(trusted_hits)
    combined_evidence.extend(google_hits)

    conflict = build_conflict(combined_evidence, trusted_domains_set)
    evidence_strength = compute_evidence_strength(trusted_hits, google_hits, official_hits, trusted_domains_set)
    final_label, bullets = final_label_merge(ml_label, ml_conf, conflict, evidence_strength, official_hits)

    return {
        "ok": True,
        "lang": lang,
        "translated": translated,
        "cleaned": cleaned,
        "keywords": keywords,
        "ml_label": ml_label,
        "ml_conf": ml_conf,
        "trusted_hits": trusted_hits,
        "google_hits": google_hits,
        "official_domains": official_domains,
        "official_hits": official_hits,
        "trusted_domains_set": trusted_domains_set,
        "conflict": conflict,
        "evidence_strength": evidence_strength,
        "final_label": final_label,
        "bullets": bullets,
    }