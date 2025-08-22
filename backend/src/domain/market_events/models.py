from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.enums import (
    MarketEvenProcessingtStatus,
    MarketEventSource,
    PriorityFlag,
    SentimentalAnalysis,
)
from src.domain.utils import ActivityTrackingBaseModel


class MarketEvent(ActivityTrackingBaseModel):
    __tablename__ = "market_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    banner = Column(String, nullable=True)
    sentimental_analysis: Mapped[SentimentalAnalysis] = mapped_column(
        SqlEnum(SentimentalAnalysis),
        nullable=True,
    )
    priority_flag: Mapped[PriorityFlag] = mapped_column(
        SqlEnum(PriorityFlag),
        nullable=True,
    )
    compliance_check = Column(String, nullable=True)
    description = Column(String, nullable=False)
    deep_research_content = Column(String, nullable=True)
    ai_generated_summarized_content = Column(String, nullable=True)
    processing_status: Mapped[MarketEvenProcessingtStatus] = mapped_column(
        SqlEnum(MarketEvenProcessingtStatus),
        default=MarketEvenProcessingtStatus.RESEARCHING,
        nullable=False,
    )
    source: Mapped[MarketEventSource] = mapped_column(
        SqlEnum(MarketEventSource),
        nullable=False,
    )
    is_customized = Column(Boolean, default=False)
