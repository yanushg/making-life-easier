import json
from fastapi.testclient import TestClient
from app.main import app
from app.api import whatsapp_webhook as whatsapp_module

client = TestClient(app)


def load_fixture(name: str):
    path = f"tests/fixtures/{name}"
    with open(path, "r") as f:
        return json.load(f)


def test_whatsapp_ping_get_200():
    response = client.get("/webhook/whatsapp/")
    assert response.status_code == 200
    assert response.text == "whatsapp webhook is up"


def test_whatsapp_webhook_post_calls_send(monkeypatch):
    called = {}

    async def fake_send(to: str, text: str, client=None):
        called["to"] = to
        called["text"] = text

    monkeypatch.setattr(whatsapp_module, "send_whatsapp_message", fake_send)

    payload = load_fixture("whatsapp_text_message.json")

    response = client.post("/webhook/whatsapp/", json=payload)

    assert response.status_code == 201
    assert response.json() == {"status": "created"}

    assert called["to"] == "972500000000"
    assert called["text"] == "Hello from fixture"
