import re
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

OG_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def find_article_image(url):
    """
    Entra en la página del artículo y busca su imagen og:image real.
    Devuelve None si no la encuentra o si falla (no debe tumbar el resto del bot).
    """
    if not url:
        return None
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        match = OG_IMAGE_RE.search(resp.text)
        return match.group(1) if match else None
    except requests.RequestException:
        return None


def ensure_images(items):
    """Rellena la imagen de cada noticia que no la traiga, buscándola en su propia página."""
    for item in items:
        if not item.get("image") and item.get("url"):
            item["image"] = find_article_image(item["url"])
    return items
