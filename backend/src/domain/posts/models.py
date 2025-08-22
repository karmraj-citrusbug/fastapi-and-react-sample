from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums import PostStatus
from src.domain.users.models import User  # Import User model to ensure it's registered
from src.domain.utils import ActivityTrackingBaseModel


class Post(ActivityTrackingBaseModel):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    market_event_id = Column(UUID, ForeignKey("market_events.id"))
    status: Mapped[PostStatus] = mapped_column(SqlEnum(PostStatus), nullable=False)
    is_customized = Column(Boolean, default=False)
