import time
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SEND_SPACING_SECONDS

API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_news_item(item):
    """Envía una noticia: con foto real si hay, con imagen generada si no, o como texto si falla todo."""
    caption = item["summary"] or item["headline"]

    if item.get("image_bytes"):
        url = f"{API_BASE}/sendPhoto"
        files = {"photo": ("news.png", item["image_bytes"], "image/png")}
        payload = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "HTML"}
        resp = requests.post(url, data=payload, files=files, timeout=20)
    elif item.get("image"):
        url = f"{API_BASE}/sendPhoto"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "photo": item["image"],
            "caption": caption,
            "parse_mode": "HTML",
        }
        resp = requests.post(url, data=payload, timeout=15)
    else:
        url = f"{API_BASE}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": caption,
            "parse_mode": "HTML",
        }
        resp = requests.post(url, data=payload, timeout=15)

    if not resp.ok:
        # Si falla el envío con foto (real o generada), reintenta como texto plano
        if item.get("image") or item.get("image_bytes"):
            fallback = requests.post(f"{API_BASE}/sendMessage", data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": caption,
                "parse_mode": "HTML",
            }, timeout=15)
            return fallback.ok
        return False
    return True


def send_news_batch(items):
    """Envía una lista de noticias espaciadas para no saturar el canal."""
    for item in items:
        send_news_item(item)
        time.sleep(SEND_SPACING_SECONDS)


def send_daily_summary_header():
    requests.post(f"{API_BASE}/sendMessage", data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "Buenos días, estas son las noticias cripto de hoy de ALTO IMPACTO",
        "parse_mode": "HTML",
    }, timeout=15)


def send_daily_digest(headlines):
    """
    Envía el recopilatorio de titulares enviados durante el día (cada uno ya se
    mandó individualmente cuando salió, esto es solo el resumen de las 9:00).
    """
    if not headlines:
        requests.post(f"{API_BASE}/sendMessage", data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": "Hoy no hubo más noticias de alto impacto además de las ya enviadas.",
            "parse_mode": "HTML",
        }, timeout=15)
        return

    lines = [f"• {h}" for h in headlines]

    # Trocear en varios mensajes si se pasa del límite de Telegram (~4096 caracteres)
    chunks, current = [], ""
    for line in lines:
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) > 3500:
            chunks.append(current)
            current = line
        else:
            current = candidate
    if current:
        chunks.append(current)

    for chunk in chunks:
        requests.post(f"{API_BASE}/sendMessage", data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "HTML",
        }, timeout=15)
