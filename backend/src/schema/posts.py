from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from fastapi import status
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.domain.enums import ContentTone, PostStatus, MarketEventSource


class PostDataModelSchema(BaseModel):
    """
    Schema for a post.
    """

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    market_event_id: UUID
    is_customized: bool
    status: PostStatus
    created_at: datetime
    updated_at: datetime


class GetPostDataModelSchema(BaseModel):
    """
    Schema for a post.
    """

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    market_event_id: UUID
    is_customized: bool
    status: PostStatus
    created_at: datetime
    updated_at: datetime
    source: MarketEventSource


class GetPostsListingsQueryParams(BaseModel):
    search_term: str = Field(
        "", alias="search", description="Term to search for in the posts"
    )
    page: int = Field(
        1, ge=1, description="Page number for pagination (default: 1, must be >= 1)"
    )
    limit: int = Field(
        10, le=100, description="Number of entries per page (default: 10, max: 100)"
    )
    status: Optional[PostStatus] = Field(None, description="Filter posts by status")
    source: Optional[MarketEventSource] = Field(
        None, description="Filter by market event source"
    )
    start_date: Optional[date] = Field(
        None, description="Filter by start date (YYYY-MM-DD)"
    )
    end_date: Optional[date] = Field(
        None, description="Filter by end date (YYYY-MM-DD)"
    )

    @model_validator(mode="after")
    def validate_dates(self) -> "GetPostsListingsQueryParams":
        start_date = self.start_date
        end_date = self.end_date

        if start_date and end_date and end_date < start_date:
            raise ValueError("end_date must not be earlier than start_date")

        return self

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, v: Optional[date]) -> Optional[date]:
        if v is None:
            return v

        if not isinstance(v, date):
            raise ValueError("Date must be in YYYY-MM-DD format")

        return v

    class Config:
        validate_by_name = True
        json_encoders = {date: lambda v: v.strftime("%Y-%m-%d")}


class UpdatePostSchema(BaseModel):
    """
    Schema for updating a post.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    market_event_id: Optional[UUID] = None
    is_customized: Optional[bool] = None
    status: Optional[PostStatus] = None


class CreatePostRequestSchema(BaseModel):
    """
    Schema for creating a post.
    """

    market_event_id: str


class UpdatePostRequestSchema(BaseModel):
    """
    Schema for updating a post.
    """

    description: Optional[str] = None


class ApprovePostRequestSchema(BaseModel):
    """
    Schema for updating a post.
    """

    post_id: UUID


class PublishPostsRequestSchema(BaseModel):
    """
    Schema for updating a post.
    """

    post_ids: List[UUID]


class CreateCustomizedPostRequestSchema(BaseModel):
    """
    Schema for creating a customized post.
    """

    event_title: str


class CustomizePostRequestSchema(BaseModel):
    """
    Schema for updating a post.
    """

    prompt: str
    content_tone: ContentTone


class GetPostDataResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Post fetched successfully"
    page: int = 1
    limit: int = 10
    total_pages: int = 1
    total_records: int = 1
    has_next: bool = False
    has_previous: bool = False
    data: list[GetPostDataModelSchema]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Post fetched successfully",
                "page": 1,
                "limit": 10,
                "total_pages": 1,
                "total_records": 1,
                "has_next": False,
                "has_previous": False,
                "data": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Post 1",
                        "description": "Post 1 description",
                        "market_event_id": "123e4567-e89b-12d3-a456-426614174000",
                        "is_customized": False,
                        "status": "DRAFT",
                        "created_at": "2021-01-01 00:00:00",
                        "updated_at": "2021-01-01 00:00:00",
                        "source": "Alpha Vantage",
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "title": "Post 2",
                        "description": "Post 2 description",
                        "market_event_id": "123e4567-e89b-12d3-a456-426614174001",
                        "is_customized": False,
                        "status": "DRAFT",
                        "created_at": "2021-01-01 00:00:00",
                        "updated_at": "2021-01-01 00:00:00",
                        "source": "Alpha Vantage",
                    },
                ],
            }
        }
    )


class GetPostDetailsResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Post fetched successfully"
    data: GetPostDataModelSchema


class GetPostStatisticsResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Post fetched successfully"
    data: dict = {
        "total_posts": 1,
        "draft_posts": 1,
        "published_posts": 1,
        "customized_posts": 1,
    }


class CreatePostResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_201_CREATED
    message: str = "Post created successfully"
    data: PostDataModelSchema


class UpdatePostResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Post updated successfully"
    data: PostDataModelSchema


class ApprovePostResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Post approved successfully"
    data: PostDataModelSchema

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Posts approved successfully",
                "data": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Post 1",
                        "description": "Post 1 description",
                        "market_event_id": "123e4567-e89b-12d3-a456-426614174000",
                        "is_customized": False,
                        "status": "APPROVED",
                        "created_at": "2021-01-01 00:00:00",
                        "updated_at": "2021-01-01 00:00:00",
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "title": "Post 2",
                        "description": "Post 2 description",
                        "market_event_id": "123e4567-e89b-12d3-a456-426614174001",
                        "is_customized": False,
                        "status": "APPROVED",
                        "created_at": "2021-01-01 00:00:00",
                        "updated_at": "2021-01-01 00:00:00",
                    },
                ],
            }
        }
    )


class PublishPostsResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Posts published successfully"
    data: list[PostDataModelSchema]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Posts published successfully",
                "data": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Post 1",
                        "description": "Post 1 description",
                        "market_event_id": "123e4567-e89b-12d3-a456-426614174000",
                        "is_customized": False,
                        "status": "PUBLISHED",
                        "created_at": "2021-01-01 00:00:00",
                        "updated_at": "2021-01-01 00:00:00",
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "title": "Post 2",
                        "description": "Post 2 description",
                        "market_event_id": "123e4567-e89b-12d3-a456-426614174001",
                        "is_customized": False,
                        "status": "PUBLISHED",
                        "created_at": "2021-01-01 00:00:00",
                        "updated_at": "2021-01-01 00:00:00",
                    },
                ],
            }
        }
    )


class CreateCustomizedPostResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_201_CREATED
    message: str = "Customized post created successfully"
    data: PostDataModelSchema


class UpdateCustomizedPostResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Post customized successfully"
    data: PostDataModelSchema


class PostDataResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    page: int = 1
    limit: int = 10
    total_pages: int = 1
    total_records: int = 1
    has_next: bool = False
    has_previous: bool = False
    data: List[GetPostDataModelSchema]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "page": 1,
                "limit": 10,
                "total_pages": 1,
                "total_records": 1,
                "has_next": False,
                "has_previous": False,
                "data": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Post 1",
                        "description": "Post 1 description",
                        "market_event_id": "123e4567-e89b-12d3-a456-426614174000",
                        "is_customized": False,
                        "status": "DRAFT",
                        "created_at": "2021-01-01 00:00:00",
                        "updated_at": "2021-01-01 00:00:00",
                        "source": "Alpha Vantage",
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "title": "Post 2",
                        "description": "Post 2 description",
                        "market_event_id": "123e4567-e89b-12d3-a456-426614174001",
                        "is_customized": False,
                        "status": "DRAFT",
                        "created_at": "2021-01-01 00:00:00",
                        "updated_at": "2021-01-01 00:00:00",
                        "source": "Alpha Vantage",
                    },
                ],
            }
        }
    )


class PostCountsResponseSchema(BaseModel):
    """
    Schema for a post.
    """

    total_posts: int = 1
    draft_posts: int = 1
    published_posts: int = 1
    customized_posts: int = 1


class GetPublishedPostsListingsQueryParams(BaseModel):
    search_term: str = Field(
        "", alias="search", description="Term to search for in the posts"
    )
    page: int = Field(
        1, ge=1, description="Page number for pagination (default: 1, must be >= 1)"
    )
    limit: int = Field(
        10, le=100, description="Number of entries per page (default: 10, max: 100)"
    )
    source: Optional[MarketEventSource] = Field(
        None, description="Filter by market event source"
    )
    start_date: Optional[date] = Field(
        None, description="Filter by start date (YYYY-MM-DD)"
    )
    end_date: Optional[date] = Field(
        None, description="Filter by end date (YYYY-MM-DD)"
    )

    @model_validator(mode="after")
    def validate_dates(self) -> "GetPostsListingsQueryParams":
        start_date = self.start_date
        end_date = self.end_date

        if start_date and end_date and end_date < start_date:
            raise ValueError("end_date must not be earlier than start_date")

        return self

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, v: Optional[date]) -> Optional[date]:
        if v is None:
            return v

        if not isinstance(v, date):
            raise ValueError("Date must be in YYYY-MM-DD format")

        return v

    class Config:
        validate_by_name = True
        json_encoders = {date: lambda v: v.strftime("%Y-%m-%d")}
        