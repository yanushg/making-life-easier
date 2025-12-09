import json
import pytest

from app.channels.whatsapp_parser import extract_sender_and_text


def load_fixture(name: str):
    path = f"tests/fixtures/{name}"
    with open(path, "r") as f:
        return json.load(f)


def test_extract_sender_and_text_from_valid_payload():
    payload = load_fixture("whatsapp_text_message.json")

    sender, message = extract_sender_and_text(payload)

    assert sender == "972549406690"
    assert message["type"] == "text"
    assert message["text"] == "Hello from fixture"

    # Ensure raw message exists
    assert "raw" in message
    assert message["raw"]["id"] == "wamid.TEST"


def test_extract_sender_and_text_raises_on_invalid_payload():
    # completely wrong shape
    bad_payload = {"foo": "bar"}

    with pytest.raises(ValueError):
        extract_sender_and_text(bad_payload)
