from fastapi import APIRouter, Depends, status

from config.response_handler import ResponseHandler
from src.application.posts import PostAppServices
from src.infrastructure.security import get_current_user
from src.schema.messages_enums import PostEnums
from src.schema.posts import (
    CreatePostRequestSchema,
    CreatePostResponseSchema,
    GetPostDataResponseSchema,
    GetPostDetailsResponseSchema,
    PublishPostsRequestSchema,
    PublishPostsResponseSchema,
    UpdatePostRequestSchema,
    UpdatePostResponseSchema,
    GetPostsListingsQueryParams,
)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/", response_model=GetPostDataResponseSchema)
async def get_posts_listings(
    query_params: GetPostsListingsQueryParams = Depends(),
    current_user: dict = Depends(get_current_user),
):
    """
    Endpoint to get Post list with search and pagination.

    `Args:`
    - query_params (GetPostsListingsQueryParams): Query parameters for filtering and pagination.
    - current_user (dict): The currently authenticated user.

    `Returns:`
    - GetPostDataResponseSchema: List of Posts.
    """
    post_app_services = PostAppServices()
    data = await post_app_services.get_posts_listings(
        query_params=query_params,
        current_user=current_user,
    )
    return ResponseHandler.success_listings(
        message=PostEnums.POST_FETCH_SUCCESS,
        data=data,
    )


@router.get("/details/{post_id}", response_model=GetPostDetailsResponseSchema)
async def get_post_details_by_id(
    post_id: str, current_user: dict = Depends(get_current_user)
):
    """
    Endpoint to get a single Post by ID.

    `Args:`
    - post_id (str): ID of the Post.

    `Returns:`
    - GetPostDetailsResponseSchema: Post details.
    """
    post_app_services = PostAppServices()
    post = await post_app_services.get_post_details_by_id(
        current_user=current_user,
        post_id=post_id,
    )
    return ResponseHandler.success(
        message=PostEnums.POST_FETCH_SUCCESS,
        data=post,
    )


@router.post("/", response_model=CreatePostResponseSchema)
async def create_post_from_market_event_id(
    payload: CreatePostRequestSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Endpoint to create a post from a market event ID.

    `Args:`
    - payload (CreatePostRequestSchema): The request payload containing the market event ID.
    - current_user (dict): The currently authenticated user.

    `Returns:`
    - CreatePostResponseSchema: The response schema containing the created post data.
    """

    post_app_services = PostAppServices()
    post = await post_app_services.create_post_from_market_event_id(
        market_event_id=payload.market_event_id,
        current_user=current_user,
    )
    return ResponseHandler.success(
        status_code=status.HTTP_201_CREATED,
        message=PostEnums.POST_CREATE_SUCCESS,
        data=post,
    )


@router.patch("/{post_id}", response_model=UpdatePostResponseSchema)
async def update_post_description_or_status_by_id(
    payload: UpdatePostRequestSchema,
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    """
    Endpoint to update a post description or status.

    `Args:`
    - payload (UpdatePostRequestSchema): The request payload containing the updated
            post description and/or status.
    - post_id (str): ID of the post to update.
    - current_user (dict): The currently authenticated user.

    `Returns:`
    - UpdatePostResponseSchema: The response schema containing the updated post data.
    """
    post_app_services = PostAppServices()
    post = await post_app_services.update_post(
        post_id=post_id,
        post_data=payload,
        current_user=current_user,
    )
    return ResponseHandler.success(
        message=PostEnums.POST_UPDATE_SUCCESS,
        data=post,
    )


@router.post("/publish", response_model=PublishPostsResponseSchema)
async def publish_posts_by_ids(
    payload: PublishPostsRequestSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Endpoint to publish multiple posts by their IDs.

    `Args:`
    - payload (PublishPostsRequestSchema): The request payload containing the list of post IDs to publish.
    - current_user (dict): The currently authenticated user.

    `Returns:`
    - PublishPostsResponseSchema: The response schema containing the result of the publish operation.
    """

    post_app_services = PostAppServices()
    post = await post_app_services.publish_posts_by_ids(
        payload=payload,
        current_user=current_user,
    )
    return ResponseHandler.success(
        message=PostEnums.POST_PUBLISH_SUCCESS,
        data=post,
    )
