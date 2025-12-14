from app.conversation.service import build_reply


def test_reply_engine_echoes_text():
    # Minimal input
    parsed = {"type": "text", "text": "Hello bot!", "raw": {}}

    reply = build_reply(parsed)

    assert isinstance(reply, dict)
    assert reply["text"] == "Hello bot!"


def test_reply_engine_handles_empty_text():
    parsed = {"type": "text", "text": "", "raw": {}}

    reply = build_reply(parsed)

    assert reply["text"] == "I didn't receive any text. Can you try again?"


def test_reply_engine_handles_non_text_messages():
    parsed = {"type": "image", "text": "", "raw": {}}

    reply = build_reply(parsed)

    assert reply["text"] == "I can only read text messages right now."
