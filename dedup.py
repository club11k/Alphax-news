import time
from difflib import SequenceMatcher

SIMILARITY_THRESHOLD = 0.55
DEDUP_WINDOW_SECONDS = 24 * 60 * 60  # no repetir el mismo tema en 24h


def _normalize(text):
    return text.lower().strip()


def _is_similar(a, b):
    return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio() >= SIMILARITY_THRESHOLD


def filter_duplicate_topics(items, recent_sent):
    """
    Descarta noticias cuyo titular sea muy parecido a algo ya enviado en las
    últimas 24h, aunque venga de una fuente distinta (ej. CoinDesk y Cointelegraph
    contando la misma subida/bajada de Bitcoin el mismo día).

    'recent_sent' es una lista de dicts {"headline": str, "timestamp": epoch} que
    se modifica in-place: se limpia de entradas caducadas y se le añaden las nuevas
    noticias que sí pasan el filtro.
    """
    now = time.time()
    recent_sent[:] = [r for r in recent_sent if now - r["timestamp"] < DEDUP_WINDOW_SECONDS]

    result = []
    for item in items:
        headline = item.get("headline", "")
        if any(_is_similar(headline, r["headline"]) for r in recent_sent):
            continue
        result.append(item)
        recent_sent.append({"headline": headline, "timestamp": now})
    return result
