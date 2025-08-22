import pytest

from src.application.users import UserAppServices


class FakeUserDomain:
    def __init__(self):
        self.created = None
        self.updated = []

    def get_user_by_email(self, email):
        return None

    def get_user_factory(self):
        class F:
            @staticmethod
            def build_entity_with_id(data):
                class U:
                    def __init__(self):
                        self.id = "u1"
                        self.username = data.username
                        self.email = data.email
                        self.password = data.password
                        self.is_verified = False

                return U()

        return F

    def create_user(self, user):
        self.created = user
        return user

    def get_user_by_id(self, user_id):
        class U:
            def __init__(self):
                self.id = user_id
                self.username = "name"
                self.email = "e@example.com"
                self.password = "$2b$12$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                self.is_verified = False

        return U()

    def update_user_by_id(self, user_id, data):
        self.updated.append((user_id, data))
        return self.get_user_by_id(user_id)


class FakeEmail:
    async def send_signup_verification_email(self, **kwargs):
        return True

    async def send_forgot_password_email(self, **kwargs):
        return True


@pytest.mark.asyncio
async def test_create_new_user_sends_verification(monkeypatch):
    app = UserAppServices()
    fake_domain = FakeUserDomain()
    monkeypatch.setattr(app, "user_domain_services", fake_domain)
    monkeypatch.setattr(app, "email_service", FakeEmail())

    class FakeToken:
        def generate_verification_token(self, **kwargs):
            return "tok"

    monkeypatch.setattr("src.infrastructure.security.token_services", FakeToken())

    data = type("S", (), {"username": "u", "email": "e@example.com", "password": "P@ssw0rd!"})()
    out = await app.create_new_user(data)
    assert out.email == "e@example.com"
    assert fake_domain.created is not None

