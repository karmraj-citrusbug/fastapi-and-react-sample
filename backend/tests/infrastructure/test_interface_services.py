from src.infrastructure.llm.openai_service import OpenAIServices
from src.infrastructure.email_service import EmailService


def test_openai_service_returns_stub_when_no_key(monkeypatch):
    from config import settings as cfg

    # Force empty key
    monkeypatch.setattr(cfg, "app_settings", type("S", (), {"OPENAI_API_KEY": ""})())

    svc = OpenAIServices()
    out = svc.get_chat_completion(user_prompt="hello")
    assert isinstance(out, dict)
    assert out.get("summary")


def test_email_service_noop_without_api_key(monkeypatch):
    from config.settings import app_settings

    monkeypatch.setattr(app_settings, "SENDGRID_API_KEY", "")

    svc = EmailService()
    ok = None

    async def run():
        nonlocal ok
        ok = await svc.send_signup_verification_email("u", "e@example.com", "t")

    import asyncio

    asyncio.run(run())
    assert ok is True
