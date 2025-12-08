from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

class WebchatMessage(BaseModel):
    user_id: str
    message: str

@router.post("/message", status_code=status.HTTP_201_CREATED)
async def webchat_message(msg: WebchatMessage):
    """
    Simple endpoint for web chat messages.
    For now, just echo back.
    """
    # TODO: call conversation service later
    return {
        "reply": f"Echo: {msg.message}",
        "user_id": msg.user_id,
    }
