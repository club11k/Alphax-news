import feedparser
from config import COINTELEGRAPH_RSS_URL


def fetch_cointelegraph_news():
    """Devuelve noticias del RSS oficial de CoinTelegraph, normalizadas."""
    feed = feedparser.parse(COINTELEGRAPH_RSS_URL)

    normalized = []
    for entry in feed.entries:
        image = None
        if "media_content" in entry and entry.media_content:
            image = entry.media_content[0].get("url")

        normalized.append({
            "source": "cointelegraph",
            "id": entry.get("id", entry.get("link", "")),
            "headline": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "url": entry.get("link", ""),
            "image": image,
            "datetime": entry.get("published", ""),
        })
    return normalized
