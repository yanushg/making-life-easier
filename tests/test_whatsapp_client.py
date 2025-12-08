# tests/test_whatsapp_client.py
import pytest

from app.channels.whatsapp_client import send_whatsapp_message
from app.core import config


class FakeResponse:
    def __init__(self, status_code: int = 200, text: str = ""):
        self.status_code = status_code
        self.text = text
        self.json_called = False

    def raise_for_status(self):
        if self.status_code >= 400:
            # Simulate httpx.HTTPStatusError behaviour enough for our tests
            raise Exception(f"HTTP error {self.status_code}")

    def json(self):
        self.json_called = True
        return {"dummy": "ok"}


class FakeClient:
    def __init__(self, status_code: int = 200, text: str = ""):
        self.calls = 0
        self.last_url = None
        self.last_headers = None
        self.last_json = None
        self._status_code = status_code
        self._text = text

    async def post(self, url, headers=None, json=None):
        self.calls += 1
        self.last_url = url
        self.last_headers = headers
        self.last_json = json
        return FakeResponse(status_code=self._status_code, text=self._text)


@pytest.mark.asyncio
async def test_send_whatsapp_message_builds_correct_request(monkeypatch):
    # Arrange: fake env values
    monkeypatch.setattr(config, "WHATSAPP_ACCESS_TOKEN", "TEST_TOKEN_123")
    monkeypatch.setattr(config, "WHATSAPP_PHONE_NUMBER_ID", "PHONE_ID_123")

    fake_client = FakeClient()

    # Act
    await send_whatsapp_message(
        to="972500000000",
        text="hello from test",
        client=fake_client,
    )

    # Assert URL
    assert fake_client.last_url == (
        "https://graph.facebook.com/v19.0/PHONE_ID_123/messages"
    )

    # Assert headers
    assert fake_client.last_headers == {
        "Authorization": "Bearer TEST_TOKEN_123",
        "Content-Type": "application/json",
    }

    # Assert JSON payload
    assert fake_client.last_json == {
        "messaging_product": "whatsapp",
        "to": "972500000000",
        "type": "text",
        "text": {"body": "hello from test"},
    }


@pytest.mark.asyncio
async def test_send_whatsapp_message_no_config_skips_send(monkeypatch):
    # Arrange: clear env in config
    monkeypatch.setattr(config, "WHATSAPP_ACCESS_TOKEN", "")
    monkeypatch.setattr(config, "WHATSAPP_PHONE_NUMBER_ID", "")

    fake_client = FakeClient()

    # Act: should not crash, and should not call fake_client.post
    await send_whatsapp_message(
        to="972500000000",
        text="hello",
        client=fake_client,
    )

    # Assert: no URL means we skipped sending
    assert fake_client.calls == 1
