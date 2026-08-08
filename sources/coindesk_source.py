import feedparser
from config import COINDESK_RSS_URL


def fetch_coindesk_news():
    """Devuelve noticias del RSS oficial de CoinDesk, normalizadas."""
    feed = feedparser.parse(COINDESK_RSS_URL)

    normalized = []
    for entry in feed.entries:
        normalized.append({
            "source": "coindesk",
            "id": entry.get("id", entry.get("link", "")),
            "headline": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "url": entry.get("link", ""),
            "image": None,  # se busca la imagen real del artículo después
            "datetime": entry.get("published", ""),
        })
    return normalized
