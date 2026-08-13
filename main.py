import logging
import json
import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from config import (
    TIMEZONE, DAILY_SUMMARY_HOUR, DAILY_SUMMARY_MINUTE, CHECK_INTERVAL_MINUTES,
)
from sources.finnhub_source import fetch_finnhub_crypto_news
from sources.bitget_source import fetch_bitget_announcements
from sources.coindesk_source import fetch_coindesk_news
from sources.cointelegraph_source import fetch_cointelegraph_news
from image_utils import ensure_images
from image_generator import generate_news_image
from filters import filter_and_enrich
from telegram_sender import send_news_batch, send_daily_summary_header

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crypto-news-bot")

app = Flask(__name__)

SEEN_IDS_FILE = "/tmp/seen_ids.json"
MAX_STORED_IDS = 1000

# IDs ya enviados, para no duplicar noticias entre ciclos.
# Se guardan también en disco (/tmp) para sobrevivir a un reinicio del proceso
# sin redeploy (aunque un redeploy sí borra /tmp; para eso está prime_seen_ids).
seen_ids = set()


def load_seen_ids_from_disk():
    if os.path.exists(SEEN_IDS_FILE):
        try:
            with open(SEEN_IDS_FILE, "r") as f:
                seen_ids.update(json.load(f))
            logger.info(f"{len(seen_ids)} IDs cargados desde disco")
        except (json.JSONDecodeError, OSError):
            logger.exception("No se pudo leer seen_ids.json, se ignora")


def save_seen_ids_to_disk():
    try:
        # Nos quedamos con los últimos MAX_STORED_IDS para que el archivo no crezca sin límite
        trimmed = list(seen_ids)[-MAX_STORED_IDS:]
        with open(SEEN_IDS_FILE, "w") as f:
            json.dump(trimmed, f)
    except OSError:
        logger.exception("No se pudo guardar seen_ids.json")


def collect_all_news():
    items = []
    for fetch_fn in (
        fetch_finnhub_crypto_news,
        fetch_bitget_announcements,
        fetch_coindesk_news,
        fetch_cointelegraph_news,
    ):
        try:
            items.extend(fetch_fn())
        except Exception:
            logger.exception(f"Fallo al obtener noticias de {fetch_fn.__name__}")
    return items


def prime_seen_ids():
    """
    Al arrancar (o tras un redeploy), marca todas las noticias que ya existen en las
    fuentes como 'vistas' sin enviarlas. Así solo se envía lo que sea realmente nuevo
    a partir de ahora, y un redeploy no provoca un reenvío masivo de noticias antiguas.
    """
    load_seen_ids_from_disk()
    logger.info("Arranque: cargando noticias existentes sin enviarlas...")
    raw_items = collect_all_news()
    for i in raw_items:
        seen_ids.add(i["id"])
    save_seen_ids_to_disk()
    logger.info(f"{len(seen_ids)} noticias marcadas como ya vistas")


def run_cycle():
    logger.info("Revisando fuentes de noticias cripto...")
    raw_items = collect_all_news()
    new_items = [i for i in raw_items if i["id"] not in seen_ids]

    relevant_items = filter_and_enrich(new_items)
    relevant_items = ensure_images(relevant_items)
    for i in relevant_items:
        if not i.get("image"):
            i["image_bytes"] = generate_news_image(i["headline"], tag=i.get("source", "cripto"))
    for i in new_items:
        seen_ids.add(i["id"])
    save_seen_ids_to_disk()

    if relevant_items:
        logger.info(f"Enviando {len(relevant_items)} noticias relevantes")
        send_news_batch(relevant_items)
    else:
        logger.info("Sin noticias relevantes en este ciclo")


def run_daily_summary():
    logger.info("Enviando resumen diario 9:00")
    send_daily_summary_header()
    run_cycle()


prime_seen_ids()

scheduler = BackgroundScheduler(timezone=TIMEZONE)
scheduler.add_job(run_cycle, "interval", minutes=CHECK_INTERVAL_MINUTES)
scheduler.add_job(
    run_daily_summary,
    CronTrigger(hour=DAILY_SUMMARY_HOUR, minute=DAILY_SUMMARY_MINUTE, timezone=TIMEZONE),
)
scheduler.start()


@app.route("/")
def health_check():
    return "crypto-news-bot activo", 200


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
