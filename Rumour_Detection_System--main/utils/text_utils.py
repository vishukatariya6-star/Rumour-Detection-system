import re
from urllib.parse import urlparse

# =====================================================
# ---------------- TEXT CLEANING ----------------------
# =====================================================

def clean_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_text(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# =====================================================
# ---------------- DOMAIN UTIL ------------------------
# =====================================================

def domain_from_url(u: str) -> str:
    try:
        return urlparse(u).netloc.lower().replace("www.", "")
    except:
        return ""


# =====================================================
# ---------------- DEDUPLICATION ----------------------
# =====================================================

def dedupe_items(items: list):
    seen = set()
    out = []

    for it in items or []:
        title = normalize_text(it.get("title", ""))
        dom = domain_from_url(it.get("publisher_url", "")) or domain_from_url(it.get("link", ""))
        key = (title[:140], dom)

        if key in seen:
            continue

        seen.add(key)
        out.append(it)

    return out