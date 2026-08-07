import requests
from config import FINNHUB_API_KEY

FINNHUB_NEWS_URL = "https://finnhub.io/api/v1/news"


def fetch_finnhub_crypto_news():
    """Devuelve noticias de la categoría 'crypto' de Finnhub, normalizadas."""
    params = {"category": "crypto", "token": FINNHUB_API_KEY}
    resp = requests.get(FINNHUB_NEWS_URL, params=params, timeout=15)
    resp.raise_for_status()
    items = resp.json()

    normalized = []
    for item in items:
        normalized.append({
            "source": "finnhub",
            "id": str(item.get("id")),
            "headline": item.get("headline", ""),
            "summary": item.get("summary", ""),
            "url": item.get("url", ""),
            "image": item.get("image") or None,
            "datetime": item.get("datetime"),  # unix timestamp
        })
    return normalized
