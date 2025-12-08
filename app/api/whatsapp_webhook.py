from typing import Any, Dict

from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse

from app.channels.whatsapp_client import send_whatsapp_message
import logging
import httpx

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_class=PlainTextResponse, status_code=status.HTTP_200_OK)
async def whatsapp_ping():
    return "whatsapp webhook is up"


@router.post("/",status_code=status.HTTP_201_CREATED)
async def whatsapp_webhook(payload: Dict[str, Any] = Body(...)):
    # 1. Extract sender + text
    try:
        msg = payload["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = msg["from"]
        text_body = msg.get("text", {}).get("body", "")
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid WhatsApp payload structure")

    # 2. Try to send WhatsApp message
    try:
        await send_whatsapp_message(to=from_number, text=text_body)
    except httpx.HTTPStatusError as e:
        # This is the REAL error from WhatsApp
        status_code = e.response.status_code
        try:
            error_body = e.response.json()
        except ValueError:
            error_body = e.response.text

        return JSONResponse(
            status_code=status_code,
            content={"error": error_body},
        )

    # 3. Success
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"status": "created"},
    )
