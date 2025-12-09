from typing import Any, Dict, Tuple


def extract_sender_and_text(payload: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Extract sender phone + parsed message dict from WhatsApp webhook payload.

    Returns:
        (sender: str, parsed_message: dict)

    parsed_message example:
    {
        "type": "text",
        "text": "Hello there",
        "raw": { full message object }
    }

    Raises:
        ValueError: if structure is invalid.
    """
    try:
        msg = payload["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = msg["from"]

        msg_type = msg.get("type", "text")

        if msg_type == "text":
            text_body = msg.get("text", {}).get("body", "")
            parsed = {
                "type": "text",
                "text": text_body,
                "raw": msg,
            }

        else:
            # For now, support only text
            parsed = {
                "type": msg_type,
                "text": "",
                "raw": msg,
            }

    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("Invalid WhatsApp payload structure") from exc

    if not sender:
        raise ValueError("Missing sender in WhatsApp payload")

    return sender, parsed
