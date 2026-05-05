# =====================================================
# ---------------- TRUSTED SOURCES --------------------
# =====================================================

TRUSTED_SOURCES = [
    "reuters.com", "apnews.com", "bbc.com", "bbc.co.uk", "theguardian.com",
    "ft.com", "wsj.com", "nytimes.com", "washingtonpost.com", "bloomberg.com",
    "aljazeera.com", "dw.com", "france24.com",

    "thehindu.com", "indianexpress.com", "hindustantimes.com", "livemint.com",
    "ndtv.com", "indiatoday.in", "economictimes.indiatimes.com",
    "timesofindia.indiatimes.com", "business-standard.com", "scroll.in",
    "theprint.in", "firstpost.com", "news18.com",

    "pib.gov.in", "rbi.org.in", "gov.in", "who.int", "cdc.gov"
]

# =====================================================
# ---------------- TRUSTED RSS FEEDS ------------------
# =====================================================

TRUSTED_RSS_FEEDS = {
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
    "India Today": "https://www.indiatoday.in/rss/home",
    "Indian Express": "https://indianexpress.com/feed/",
    "Hindustan Times": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
    "Livemint": "https://www.livemint.com/rss/news",
    "Business Standard": "https://www.business-standard.com/rss/latest.rss",
}

# =====================================================
# ---------------- OFFICIAL AUTHORITIES ---------------
# =====================================================

OFFICIAL_AUTHORITIES = {
    "ugc": ["ugc.ac.in"],
    "university grants commission": ["ugc.ac.in"],

    "pib": ["pib.gov.in"],
    "press information bureau": ["pib.gov.in"],

    "rbi": ["rbi.org.in"],
    "reserve bank of india": ["rbi.org.in"],

    "who": ["who.int"],
    "world health organization": ["who.int"],

    "cdc": ["cdc.gov"],
    "centers for disease control": ["cdc.gov"],

    "gov": ["gov.in"],
    "government": ["gov.in"],
}