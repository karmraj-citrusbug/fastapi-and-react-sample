from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import status
from pydantic import BaseModel, ConfigDict

from src.domain.enums import (
    MarketEvenProcessingtStatus,
    MarketEventSource,
    PriorityFlag,
    SentimentalAnalysis,
)


class MarketEventDataModelSchema(BaseModel):
    """
    Schema for market event.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    banner: Optional[str] = None
    sentimental_analysis: Optional[SentimentalAnalysis] = None
    priority_flag: Optional[PriorityFlag] = None
    compliance_check: Optional[str] = None
    description: str
    deep_research_content: Optional[str] = None
    ai_generated_summarized_content: Optional[str] = None
    processing_status: MarketEvenProcessingtStatus
    source: MarketEventSource
    is_customized: bool = False
    updated_at: datetime
    post_generated: bool


class UpdateMarketEventSchema(BaseModel):
    """
    Schema for update market event.
    """

    title: Optional[str] = None
    banner: Optional[str] = None
    sentimental_analysis: Optional[SentimentalAnalysis] = None
    priority_flag: Optional[PriorityFlag] = None
    compliance_check: Optional[str] = None
    description: Optional[str] = None
    deep_research_content: Optional[str] = None
    ai_generated_summarized_content: Optional[str] = None
    processing_status: Optional[MarketEvenProcessingtStatus] = None
    source: Optional[MarketEventSource] = None


class RunTimeMarketEventSchema(UpdateMarketEventSchema):
    """
    Schema for runtime market event.
    """

    id: str  # This is added for referencing the broadcasting only
    title: Optional[str] = None
    banner: Optional[str] = None
    sentimental_analysis: Optional[SentimentalAnalysis] = None
    priority_flag: Optional[PriorityFlag] = None
    compliance_check: Optional[str] = None
    description: Optional[str] = None
    deep_research_content: Optional[str] = None
    ai_generated_summarized_content: Optional[str] = None
    processing_status: Optional[MarketEvenProcessingtStatus] = None
    source: Optional[MarketEventSource] = None
    editable: bool = False
    updated_at: str


class GetMarketEventsResponseSchema(BaseModel):
    """
    Schema for get market events.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Market events fetched successfully"
    page: int = 1
    limit: int = 10
    total_pages: int = 1
    total_records: int = 1
    has_next: bool = False
    has_previous: bool = False
    data: list[MarketEventDataModelSchema]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Market events fetched successfully",
                "page": 1,
                "limit": 10,
                "total_pages": 4,
                "total_records": 46,
                "has_next": False,
                "has_previous": False,
                "data": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Market Event 1",
                        "banner": "https://example.com/banner.jpg",
                        "sentimental_analysis": "POSITIVE",
                        "priority_flag": "HIGH",
                        "compliance_check": "COMPLIANT",
                        "description": "Market Event 1 description",
                        "deep_research_content": "Market Event 1 deep research content",
                        "ai_generated_summarized_content": "Market Event 1 ai generated summarized content",
                        "processing_status": "COMPLETED",
                        "source": "MANUAL",
                        "is_customized": False,
                        "updated_at": "2021-01-01 00:00:00",
                        "post_generated": False,
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "title": "Market Event 2",
                        "banner": "https://example.com/banner2.jpg",
                        "sentimental_analysis": "NEGATIVE",
                        "priority_flag": "MEDIUM",
                        "compliance_check": "NON-COMPLIANT",
                        "description": "Market Event 2 description",
                        "deep_research_content": "Market Event 2 deep research content",
                        "ai_generated_summarized_content": "Market Event 2 ai generated summarized content",
                        "processing_status": "COMPLETED",
                        "source": "MANUAL",
                        "is_customized": False,
                        "updated_at": "2021-01-01 00:00:00",
                        "post_generated": True,
                    },
                ],
            }
        }
    )


class MarketEventResponseSchema(BaseModel):
    """
    Schema for market events response with pagination.
    """

    model_config = ConfigDict(from_attributes=True)

    page: int
    limit: int
    total_pages: int
    total_records: int
    has_next: bool
    has_previous: bool
    data: List[MarketEventDataModelSchema]


class ListMarketEventDataModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: List[MarketEventDataModelSchema]
