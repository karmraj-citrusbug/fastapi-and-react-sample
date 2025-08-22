from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, String

from src.domain.utils import ActivityTrackingBaseModel


class User(ActivityTrackingBaseModel):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
