# Alphax News – Bot de noticias cripto para Telegram

Réplica del bot de noticias de oro (XAUUSD), adaptada a criptomonedas.

## Fuentes
- Finnhub (categoría `crypto`)
- Investing.com (sección de noticias de criptomonedas)
- Anuncios públicos del exchange Bitget

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
   - `ANTHROPIC_API_KEY` (opcional, para el filtro de relevancia con IA)
6. Plan Standard recomendado (el free se duerme por inactividad, como pasó con el bot de oro).

## Notas
- Revisión de fuentes cada 2 minutos (mismo intervalo que se dejó fijado en el bot de oro).
- Resumen diario a las 9:00 (hora `Europe/Andorra`) con las noticias de alto impacto del día.
- Envío espaciado (1 noticia/minuto) para no saturar el canal.
- Si Investing.com cambia su HTML, hay que actualizar los selectores en `sources/investing_source.py`.
