import pytest

from src.infrastructure.websockets.connection_manager import ConnectionManager


class FakeWebSocket:
    def __init__(self):
        self.accepted = False
        self.sent = []
        self.client = ("127.0.0.1", 0)

    async def accept(self):
        self.accepted = True

    async def send_json(self, data):
        self.sent.append(data)


@pytest.mark.asyncio
async def test_broadcast_and_personal_message():
    mgr = ConnectionManager()
    ws1, ws2 = FakeWebSocket(), FakeWebSocket()

    await mgr.connect(ws1, user_id="u1")
    await mgr.connect(ws2, user_id="u2")

    await mgr.broadcast({"x": 1})
    assert ws1.sent and ws2.sent

    await mgr.send_personal_message("u1", {"y": 2})
    assert ws1.sent[-1] == {"y": 2}

