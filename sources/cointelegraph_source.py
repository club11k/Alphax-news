import feedparser
from config import COINTELEGRAPH_RSS_URL


def fetch_cointelegraph_news():
    """Devuelve noticias del RSS oficial de CoinTelegraph, normalizadas."""
    feed = feedparser.parse(COINTELEGRAPH_RSS_URL)

    normalized = []
    for entry in feed.entries:
        normalized.append({
            "source": "cointelegraph",
            "id": entry.get("id", entry.get("link", "")),
            "headline": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "url": entry.get("link", ""),
            "image": None,  # el RSS trae un logo genérico de plantilla; se busca la imagen real después
            "datetime": entry.get("published", ""),
        })
    return normalized
