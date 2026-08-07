import feedparser
from config import COINDESK_RSS_URL


def fetch_coindesk_news():
    """Devuelve noticias del RSS oficial de CoinDesk, normalizadas."""
    feed = feedparser.parse(COINDESK_RSS_URL)

    normalized = []
    for entry in feed.entries:
        image = None
        if "media_content" in entry and entry.media_content:
            image = entry.media_content[0].get("url")

        normalized.append({
            "source": "coindesk",
            "id": entry.get("id", entry.get("link", "")),
            "headline": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "url": entry.get("link", ""),
            "image": image,
            "datetime": entry.get("published", ""),
        })
    return normalized
