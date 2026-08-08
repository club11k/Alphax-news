import logging
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

# IDs ya enviados en esta ejecución, para no duplicar noticias entre ciclos
seen_ids = set()


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

    if relevant_items:
        logger.info(f"Enviando {len(relevant_items)} noticias relevantes")
        send_news_batch(relevant_items)
    else:
        logger.info("Sin noticias relevantes en este ciclo")


def run_daily_summary():
    logger.info("Enviando resumen diario 9:00")
    send_daily_summary_header()
    run_cycle()


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
