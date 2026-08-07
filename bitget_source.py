import requests
from config import BITGET_ANNOUNCEMENTS_URL, BITGET_LANGUAGE

# Categorías públicas de anuncios de Bitget que nos interesan
# (nuevos listados, actividades, novedades del exchange)
BITGET_CATEGORIES = ["latest_news", "coin_listings"]


def fetch_bitget_announcements():
    """Devuelve anuncios públicos del exchange Bitget, normalizados."""
    normalized = []
    for category in BITGET_CATEGORIES:
        params = {"language": BITGET_LANGUAGE, "annType": category}
        try:
            resp = requests.get(BITGET_ANNOUNCEMENTS_URL, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except (requests.RequestException, ValueError):
            continue  # si Bitget cambia el endpoint, no debe tumbar el resto del bot

        items = data.get("data", []) if isinstance(data, dict) else []
        for item in items:
            normalized.append({
                "source": "bitget",
                "id": str(item.get("annId", item.get("cTime", ""))),
                "headline": item.get("annTitle", ""),
                "summary": "",
                "url": item.get("annUrl", ""),
                "image": None,  # los anuncios de Bitget no traen imagen propia
                "datetime": item.get("cTime"),
            })
    return normalized
