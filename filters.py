import json
import requests
from config import TOP_COINS, MACRO_KEYWORDS, ANTHROPIC_API_KEY

KEYWORDS = [k.lower() for k in TOP_COINS + MACRO_KEYWORDS]


def keyword_relevant(item):
    text = f"{item.get('headline', '')} {item.get('summary', '')}".lower()
    return any(k.lower() in text for k in KEYWORDS)


def ai_relevance_and_summary(item):
    """
    Pide a Claude (Anthropic API) que:
    1) confirme si la noticia es de alto impacto para el top 10-20 de cripto o Bitget
    2) devuelva un resumen corto en español, en lenguaje sencillo, sin mencionar la fuente
    Si no hay ANTHROPIC_API_KEY configurada, se omite este paso y se usa solo el filtro de keywords.
    """
    if not ANTHROPIC_API_KEY:
        return {"relevant": True, "summary": item.get("headline", "")}

    prompt = (
        "Eres un editor de un canal de noticias cripto en español. "
        "Te paso una noticia y debes responder SOLO con JSON, sin texto extra:\n"
        '{"relevant": true/false, "summary": "resumen corto en español, tono sencillo, '
        'sin nombrar la fuente, máximo 3 frases"}\n\n'
        "Marca 'relevant' como true solo si afecta de forma clara al top 10-20 de "
        "criptomonedas por capitalización o son novedades importantes del exchange Bitget "
        "(nuevos listados, hackeos, cambios regulatorios grandes). Ignora ruido menor.\n\n"
        "Para el 'summary', hazlo dinámico y fácil de leer en Telegram:\n"
        "- Añade 1-3 emojis relevantes al contenido (ej. 🚀 subida, 📉 bajada, ⚠️ alerta, "
        "🏦 bancos/regulación, 🔐 seguridad/hackeo).\n"
        "- Resalta en negrita los datos clave (cifras, nombres de criptos, porcentajes) "
        "usando etiquetas HTML <b>así</b> (Telegram lo soporta, no uses markdown con asteriscos).\n"
        "- No abuses: negrita solo en lo realmente importante, no en frases enteras.\n\n"
        f"Titular: {item.get('headline', '')}\n"
        f"Contenido: {item.get('summary', '')}"
    )

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=20,
    )
    resp.raise_for_status()
    text = resp.json()["content"][0]["text"].strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(text)
        return {
            "relevant": bool(parsed.get("relevant")),
            "summary": parsed.get("summary", item.get("headline", "")),
        }
    except (ValueError, KeyError, IndexError):
        # Si la IA falla al responder en JSON, no descartamos la noticia:
        # dejamos que decida el filtro de keywords y usamos el titular como resumen.
        return {"relevant": True, "summary": item.get("headline", "")}


def filter_and_enrich(items):
    """Aplica primero el filtro de keywords (barato) y luego la IA (caro) solo a lo que pasa."""
    result = []
    for item in items:
        if not keyword_relevant(item):
            continue
        enriched = ai_relevance_and_summary(item)
        if enriched["relevant"]:
            item["summary"] = enriched["summary"]
            result.append(item)
    return result
