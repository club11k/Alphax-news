import feedparser
from config import COINTELEGRAPH_RSS_URL


def fetch_cointelegraph_news():
    """
    Devuelve noticias del RSS oficial de CoinTelegraph, normalizadas.
    NOTA: Cointelegraph no expone una imagen específica por artículo en su og:image
    (siempre devuelve el mismo logo genérico), así que aquí nunca se rellena 'image':
    main.py generará una imagen de plantilla para estas noticias.
    """
    feed = feedparser.parse(COINTELEGRAPH_RSS_URL)

    normalized = []
    for entry in feed.entries:
        normalized.append({
            "source": "cointelegraph",
            "id": entry.get("id", entry.get("link", "")),
            "headline": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "url": entry.get("link", ""),
            "image": None,
            "skip_image_lookup": True,  # no buscar og:image, siempre irá con plantilla
            "datetime": entry.get("published", ""),
        })
    return normalized
