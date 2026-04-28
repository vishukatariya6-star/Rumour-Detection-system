import feedparser
from urllib.parse import quote_plus

from utils.text_utils import normalize_text
from utils.config import TRUSTED_RSS_FEEDS, OFFICIAL_AUTHORITIES


def search_trusted_rss(query_keywords: str, max_hits: int = 10):
    q = normalize_text(query_keywords)
    q_words = set(q.split())

    results = []
    for source, feed_url in TRUSTED_RSS_FEEDS.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:30]:
                title = entry.get("title", "")
                link = entry.get("link", "")
                t = normalize_text(title)
                t_words = set(t.split())

                if not q_words:
                    continue
                overlap = len(q_words.intersection(t_words))
                score = overlap / max(len(q_words), 1)

                if score >= 0.25:
                    results.append({
                        "source": source,
                        "title": title,
                        "link": link,
                        "score": round(score * 100, 2),
                        "publisher_url": link
                    })
        except:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_hits]


def google_news_rss_search(query: str, max_hits: int = 10):
    q = (query or "").strip()
    if not q:
        return []

    rss_url = (
        "https://news.google.com/rss/search?q="
        + quote_plus(q)
        + "&hl=en-IN&gl=IN&ceid=IN:en"
    )

    out = []
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries[:max_hits]:
            title = entry.get("title", "") or ""
            link = entry.get("link", "") or ""

            publisher_url = ""
            src = "Google News"
            try:
                if hasattr(entry, "source") and entry.source:
                    src = getattr(entry.source, "title", "Google News") or "Google News"
                    publisher_url = getattr(entry.source, "href", "") or ""
            except:
                pass

            out.append({
                "source": src,
                "title": title,
                "link": link,
                "score": 0,
                "publisher_url": publisher_url
            })
    except:
        return []

    return out


def detect_official_domains(query_text: str):
    t = (query_text or "").lower()
    domains = []
    for key, doms in OFFICIAL_AUTHORITIES.items():
        if key in t:
            domains.extend(doms)

    seen = set()
    out = []
    for d in domains:
        d = d.lower().replace("www.", "")
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def search_official_sites_via_google_news(keywords: str, domains: list, per_domain_hits: int = 5):
    hits = []
    kw = (keywords or "").strip()
    if not kw or not domains:
        return hits

    for d in domains:
        q = f'{kw} site:{d}'
        res = google_news_rss_search(q, max_hits=per_domain_hits)
        for it in res:
            hits.append({
                "domain": d,
                "title": it.get("title", ""),
                "link": it.get("link", ""),
                "source": it.get("source", "Official")
            })
    return hits