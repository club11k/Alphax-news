import requests
from bs4 import BeautifulSoup

INVESTING_CRYPTO_NEWS_URL = "https://www.investing.com/news/cryptocurrency-news"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def fetch_investing_crypto_news():
    """
    Scraper de la sección de noticias cripto de Investing.com.
    Misma lógica que el scraper usado en el bot de oro, adaptada a la URL cripto.
    NOTA: si Investing.com cambia su HTML, hay que actualizar los selectores.
    """
    resp = requests.get(INVESTING_CRYPTO_NEWS_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    normalized = []
    articles = soup.select("article[data-test='article-item']")
    for art in articles:
        title_el = art.select_one("a[data-test='article-title-link']")
        if not title_el:
            continue

        headline = title_el.get_text(strip=True)
        url = title_el.get("href", "")

        img_el = art.select_one("img")
        image = img_el.get("src") if img_el else None

        normalized.append({
            "source": "investing",
            "id": url,
            "headline": headline,
            "summary": "",  # se completa en el paso de resumen/traducción con IA
            "url": url,
            "image": image,
            "datetime": None,
        })
    return normalized
