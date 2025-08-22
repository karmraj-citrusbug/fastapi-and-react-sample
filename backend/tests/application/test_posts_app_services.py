from types import SimpleNamespace
import pytest

from src.application.posts import PostAppServices
from src.domain.enums import PostStatus
from src.schema.posts import GetPostsListingsQueryParams


class FakePostDomainServices:
    def __init__(self):
        self.calls = []

    def get_posts_by_user_id(self, *, offset, limit, search_term, status, source, start_date, end_date, user_id):
        self.calls.append(
            {
                "offset": offset,
                "limit": limit,
                "search_term": search_term,
                "status": status,
                "source": source,
                "start_date": start_date,
                "end_date": end_date,
                "user_id": user_id,
            }
        )
        # Return minimal data structures matching app expectations
        fake_post = SimpleNamespace(
            id="p1", title="t", description="d", market_event_id="m1", is_customized=False,
            status=PostStatus.DRAFT, created_at=None, updated_at=None
        )
        results = [(fake_post, "SRC")]
        return results, 1


@pytest.mark.asyncio
async def test_get_posts_listings_paginates_and_maps(monkeypatch):
    app = PostAppServices()

    fake_domain = FakePostDomainServices()
    monkeypatch.setattr(app, "post_domain_services", fake_domain)

    qp = GetPostsListingsQueryParams(page=1, limit=10)
    current_user = {"user_id": "u1"}

    out = await app.get_posts_listings(current_user=current_user, query_params=qp)

    assert out.page == 1
    assert out.limit == 10
    assert out.total_records == 1
    assert len(out.data) == 1
    assert fake_domain.calls[0]["offset"] == 0
    assert fake_domain.calls[0]["user_id"] == "u1"


@pytest.mark.asyncio
async def test_create_customized_post_triggers_background_task(monkeypatch):
    app = PostAppServices()

    called = {"value": False}

    class FakeTask:
        @staticmethod
        def delay(*, event_title, user_id):
            called["value"] = (event_title, user_id)

    monkeypatch.setattr("src.infrastructure.tasks.process_customized_news_events_data", FakeTask)

    await app.create_customized_post(event_title="hello", current_user={"user_id": "u2"})

    assert called["value"] == ("hello", "u2")
