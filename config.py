import os

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]  # username o ID del canal, ej: @club11k_crypto_news

# --- APIs de datos ---
FINNHUB_API_KEY = os.environ["FINNHUB_API_KEY"]

# Clave opcional para el filtro de relevancia con IA (Anthropic).
# Si no se define, el bot cae automáticamente al filtro por palabras clave.
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# --- Top 10-20 criptomonedas a cubrir ---
TOP_COINS = [
    "Bitcoin", "BTC",
    "Ethereum", "ETH",
    "BNB", "Binance Coin",
    "Solana", "SOL",
    "XRP", "Ripple",
    "Cardano", "ADA",
    "Dogecoin", "DOGE",
    "TRON", "TRX",
    "Toncoin", "TON",
    "Avalanche", "AVAX",
    "Shiba Inu", "SHIB",
    "Polkadot", "DOT",
    "Chainlink", "LINK",
    "Polygon", "MATIC",
    "Litecoin", "LTC",
    "Bitcoin Cash", "BCH",
    "NEAR Protocol", "NEAR",
    "Uniswap", "UNI",
]

# Motivos indirectos que también mueven el mercado cripto (igual criterio que en el bot de oro)
MACRO_KEYWORDS = [
    "Fed", "Reserva Federal", "tipos de interés", "SEC", "regulación cripto",
    "ETF Bitcoin", "ETF Ethereum", "inflación", "halving", "hackeo", "exploit",
    "stablecoin", "USDT", "USDC", "quiebra exchange", "lavado de dinero",
]

# Países/bloques cuyas noticias macro sí nos interesan (mismo criterio que el bot de oro)
RELEVANT_REGIONS = ["Estados Unidos", "China", "Japón", "Europa", "Unión Europea"]

# --- Bitget ---
BITGET_ANNOUNCEMENTS_URL = "https://api.bitget.com/api/v2/public/annoucements"
BITGET_LANGUAGE = "es_ES"

# --- Programación ---
TIMEZONE = "Europe/Andorra"
DAILY_SUMMARY_HOUR = 9
DAILY_SUMMARY_MINUTE = 0
CHECK_INTERVAL_MINUTES = 2  # mismo intervalo que se dejó fijado en el bot de oro
SEND_SPACING_SECONDS = 60   # 1 noticia por minuto, igual que en el bot de oro
