import requests
from config import CRYPTOPANIC_API_KEY

CRYPTOPANIC_URL = "https://cryptopanic.com/api/v1/posts/"


def fetch_cryptopanic_news():
    """Devuelve noticias de CryptoPanic, normalizadas. Se omite si no hay API key configurada."""
    if not CRYPTOPANIC_API_KEY:
        return []

    params = {"auth_token": CRYPTOPANIC_API_KEY, "public": "true", "kind": "news"}
    resp = requests.get(CRYPTOPANIC_URL, params=params, timeout=15)
    resp.raise_for_status()
    results = resp.json().get("results", [])

    normalized = []
    for item in results:
        normalized.append({
            "source": "cryptopanic",
            "id": str(item.get("id")),
            "headline": item.get("title", ""),
            "summary": "",
            "url": item.get("url", ""),
            "image": None,
            "datetime": item.get("published_at"),
        })
    return normalized
