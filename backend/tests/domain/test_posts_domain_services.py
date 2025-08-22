from types import SimpleNamespace
from src.domain.enums import PostStatus
from src.domain.posts.models import Post
from src.domain.posts.services import PostDataClass, PostDomainServices, PostFactory
from src.schema.posts import UpdatePostSchema


def test_post_factory_builds_entity_with_id():
    data = PostDataClass(
        title="t",
        description="d",
        user_id="u1",
        market_event_id="00000000-0000-0000-0000-000000000000",
    )
    post = PostFactory.build_entity_with_id(data)
    assert isinstance(post, Post)
    assert post.title == "t"
    assert post.id is not None


def test_update_post_sets_customized_and_resets_status(monkeypatch):
    svc = PostDomainServices()

    # Fake session behaviors used in update_post
    class FakeSession:
        def commit(self):
            return None

        def refresh(self, _):
            return None

    monkeypatch.setattr(svc, "db_session", FakeSession())

    post = SimpleNamespace(title="old", description="old", status=PostStatus.APPROVED, is_customized=False)
    data = UpdatePostSchema(description="new desc")

    updated = svc.update_post(post=post, post_data=data)

    assert updated.is_customized is True
    assert updated.status == PostStatus.DRAFT
    assert updated.description == "new desc"


def test_approve_then_publish_posts(monkeypatch):
    svc = PostDomainServices()

    class FakeSession:
        def commit(self):
            return None

    monkeypatch.setattr(svc, "db_session", FakeSession())

    # Approve
    draft = SimpleNamespace(id="p1", status=PostStatus.DRAFT)
    monkeypatch.setattr(svc, "get_post_by_id", lambda _id: draft)
    out = svc.approve_post_by_id(post_id="p1")
    assert out.status == PostStatus.APPROVED

    # Publish
    approved = SimpleNamespace(id="p2", status=PostStatus.APPROVED)
    monkeypatch.setattr(svc, "get_post_by_id", lambda _id: approved)
    posts = svc.publish_posts_by_ids(post_ids=["p2"])
    assert posts[0].status == PostStatus.PUBLISHED
