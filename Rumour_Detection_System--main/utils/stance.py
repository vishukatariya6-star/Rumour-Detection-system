import re

DEBUNK_PHRASES = [
    "fact check", "fact-check", "factcheck",
    "debunk", "debunked",
    "hoax", "misleading",
    "false claim", "claim is false", "claims are false",
    "rumour is false", "rumor is false",
    "no evidence", "not true",
    "denies", "denied", "deny",
    "viral claim is false", "viral post is false",
    "fake news", "fake claim", "news is fake", "post is fake", "message is fake"
]

AUTH_REPORT_VERBS = [
    "declares", "declared", "flags", "flagged", "releases", "released",
    "issues", "issued", "warns", "warned", "publishes", "published",
    "shares", "shared", "lists", "listed", "names", "named", "identifies", "identified",
    "busts", "busted", "raids", "raid", "exposes", "exposed"
]

FAKE_OBJECT_WORDS = [
    "university", "universities", "college", "colleges", "institute", "institutions",
    "degree", "certificate", "diploma",
    "website", "app", "account", "profile",
    "currency", "note", "notes",
    "job", "recruitment", "admission", "scholarship",
    "id", "ids", "documents", "document",
    "caller", "call", "helpline", "loan"
]

def stance_from_text(title: str, snippet: str = "") -> str:
    text = f"{title} {snippet}".lower().strip()

    if any(p in text for p in DEBUNK_PHRASES):
        return "CONTRADICT"

    has_fake = re.search(r"\bfake\b", text) is not None
    if has_fake:
        if any(v in text for v in AUTH_REPORT_VERBS) and any(o in text for o in FAKE_OBJECT_WORDS):
            return "SUPPORT"

        if ("is fake" in text and ("claim" in text or "news" in text or "post" in text or "message" in text or "video" in text)) \
           or ("fake claim" in text) or ("fake news" in text):
            return "CONTRADICT"

        return "UNCLEAR"

    if any(w in text for w in ["reportedly", "allegedly", "may", "might", "could", "unverified"]):
        return "UNCLEAR"

    return "SUPPORT"