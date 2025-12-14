import httpx
from app.core import config


from typing import Optional


async def send_whatsapp_message(
    to: str, text: str, client: Optional[httpx.AsyncClient] = None
) -> None:
    url = f"https://graph.facebook.com/v19.0/{config.WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    if client is None:
        async with httpx.AsyncClient() as real_client:
            response = await real_client.post(url, headers=headers, json=payload)
    else:
        response = await client.post(url, headers=headers, json=payload)

    response.raise_for_status()
