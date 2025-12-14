def build_reply(parsed_message: dict) -> dict:
    """
    Build a reply based on parsed message.
    Returns a dict:
    {
        "text": "...",
        ...
    }
    """
    msg_type = parsed_message.get("type")
    text = parsed_message.get("text", "")

    # 1. Unsupported message type
    if msg_type != "text":
        return {"text": "I can only read text messages right now."}

    # 2. Empty text
    if not text.strip():
        return {"text": "I didn't receive any text. Can you try again?"}

    # 3. Default = echo
    return {"text": text}
