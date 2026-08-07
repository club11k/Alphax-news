# Alphax News – Bot de noticias cripto para Telegram

Réplica del bot de noticias de oro (XAUUSD), adaptada a criptomonedas.

## Fuentes
- Finnhub (categoría `crypto`)
- Anuncios públicos del exchange Bitget
- CryptoPanic (requiere `CRYPTOPANIC_API_KEY`, gratis en cryptopanic.com/developers/api)
- CoinDesk (RSS oficial, sin API key)
- CoinTelegraph (RSS oficial, sin API key)

## Cobertura
- Top 10-20 criptomonedas por capitalización (ver `config.py` → `TOP_COINS`)
- Motivos macro que también mueven el mercado cripto (Fed, SEC, regulación, ETFs, etc.)
- Todos los anuncios relevantes de Bitget (listados, hackeos, cambios grandes)

## Despliegue en Render
1. Sube este proyecto a un repo nuevo, ej. `club11k/alphax-news`.
2. En Render: **New → Web Service**, conecta el repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn main:app`
5. Configura las variables de entorno (ver `.env.example`):
   - `TELEGRAM_BOT_TOKEN` → el token de **Alphaxnews_bot**
   - `TELEGRAM_CHAT_ID` → el username del canal (ej. `@club11k_crypto_news`)
   - `FINNHUB_API_KEY`
   - `CRYPTOPANIC_API_KEY` (opcional pero recomendada — gratis en cryptopanic.com/developers/api)
   - `ANTHROPIC_API_KEY` (opcional, para el filtro de relevancia con IA)
6. Plan Standard recomendado (el free se duerme por inactividad, como pasó con el bot de oro).

## Notas
- Revisión de fuentes cada 2 minutos (mismo intervalo que se dejó fijado en el bot de oro).
- Resumen diario a las 9:00 (hora `Europe/Andorra`) con las noticias de alto impacto del día.
- Envío espaciado (1 noticia/minuto) para no saturar el canal.
- Si CryptoPanic, CoinDesk o CoinTelegraph cambian su API/RSS, hay que revisar el archivo correspondiente en `sources/`.
