from typing import Any, Dict

from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse

from app.channels.whatsapp_client import send_whatsapp_message
from app.channels.whatsapp_parser import extract_sender_and_text
from app.conversation.service import build_reply


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
        sender, parsed_msg = extract_sender_and_text(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    #text_body = parsed_msg.get("text", "")
    reply = build_reply(parsed_msg)
    reply_text = reply["text"]

    # 2. Send WhatsApp message (still echo for now)
    try:
        await send_whatsapp_message(to=sender, text=reply_text)
    except httpx.HTTPStatusError as e:
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
        content={
            "status": "created",
            "sender": sender,
            "message": parsed_msg,
            "reply_text": reply_text,
        },
    )
