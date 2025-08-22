from config.response_handler import ResponseHandler
from src.application.market_events import MarketEventAppServices
from src.domain.enums import PostStatus
from src.domain.posts.services import PostDataClass, PostDomainServices, PostFactory
from src.exceptions.market_events import MarketEventNotFoundException
from src.exceptions.posts import (
    PostNotAuthorizedException,
    PostNotFoundException,
    PostNotPublishedException,
)
from src.infrastructure.llm.openai_service import OpenAIServices
from src.infrastructure.tasks import process_customized_news_events_data
from src.schema.posts import (
    ApprovePostRequestSchema,
    CustomizePostRequestSchema,
    GetPostDataModelSchema,
    GetPublishedPostsListingsQueryParams,
    PostDataResponseSchema,
    PublishPostsRequestSchema,
    UpdatePostRequestSchema,
    UpdatePostSchema,
    GetPostsListingsQueryParams,
)
from src.schema.utils import PromptEnum


class PostAppServices:
    """
    PostAppServices class for handling post-related operations.
    """

    def __init__(self):
        """
        Constructor for PostAppServices class.
        """
        self.post_domain_services = PostDomainServices()
        self.market_event_app_services = MarketEventAppServices()
        self.openai_services = OpenAIServices()

    async def get_posts_listings(
        self,
        current_user: dict,
        query_params: GetPostsListingsQueryParams,
    ):
        try:
            offset = (query_params.page - 1) * query_params.limit

            results, count = self.post_domain_services.get_posts_by_user_id(
                offset=offset,
                limit=query_params.limit,
                search_term=query_params.search_term,
                status=query_params.status,
                source=query_params.source,
                start_date=query_params.start_date,
                end_date=query_params.end_date,
                user_id=current_user["user_id"],
            )

            post_data = [
                GetPostDataModelSchema(**post.__dict__, source=source)
                for post, source in results
            ]

            has_next = offset + query_params.limit < count
            has_previous = query_params.page > 1
            pages = (count + query_params.limit - 1) // query_params.limit

            return PostDataResponseSchema(
                page=query_params.page,
                limit=query_params.limit,
                total_pages=pages,
                total_records=count,
                has_next=has_next,
                has_previous=has_previous,
                data=post_data,
            )

        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def get_post_details_by_id(self, current_user: dict, post_id: str):
        """
        Method to get a single post by ID, including MarketEvent source.
        """
        try:
            result = self.post_domain_services.get_post_by_id_with_market_event_source(
                post_id=post_id
            )

            if not result:
                raise PostNotFoundException()

            post, source = result

            if str(post.user_id) != str(current_user["user_id"]):
                raise PostNotAuthorizedException()

            return GetPostDataModelSchema(**post.__dict__, source=source)

        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def get_published_post_by_id(self, post_id: str):
        """
        Method to get a single post by ID, including MarketEvent source.
        """
        try:
            result = self.post_domain_services.get_post_by_id_with_market_event_source(
                post_id=post_id
            )

            if not result:
                raise PostNotFoundException()

            post, source = result

            if post.status != PostStatus.PUBLISHED:
                raise PostNotPublishedException()

            return GetPostDataModelSchema(**post.__dict__, source=source)

        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def get_post_statistics_data(self, current_user: dict):
        """
        Method to get post statistics for the current user.

        Args:
            current_user (dict): The currently authenticated user.

        Returns:
            dict: A dictionary containing the counts of total posts, draft posts, published posts, and customized posts.
        """
        try:
            statistics_data = self.post_domain_services.get_post_counts_by_user_id(
                user_id=current_user["user_id"]
            )
            return statistics_data
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def create_post_from_dataclass(self, post_data: PostDataClass):
        """
        Method to create a post from a PostDataClass.

        Args:
            post_data (PostDataClass): The dataclass object containing the post data.

        Returns:
            Post: The created post object.
        """
        try:
            post_data = PostFactory.build_entity_with_id(data=post_data)

            post_data = self.post_domain_services.create_post(post=post_data)
            return post_data
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def create_post_from_market_event_id(
        self,
        market_event_id: str,
        current_user: dict,
    ):
        """
        Method to create a new post from a market event ID.

        Args:
            market_event_id (str): ID of the market event.
            current_user (dict): Current user information.

        Returns:
            dict: Created post data.
        """
        try:
            existing_post_from_market_event_id = (
                self.post_domain_services.get_post_by_user_id_and_market_event_id(
                    user_id=current_user["user_id"],
                    market_event_id=market_event_id,
                )
            )

            if not existing_post_from_market_event_id:
                market_event = (
                    await self.market_event_app_services.get_market_event_details_by_id(
                        id=market_event_id
                    )
                )

                if not market_event:
                    raise MarketEventNotFoundException()

                post_dataclass = PostDataClass(
                    title=market_event.title,
                    description=market_event.deep_research_content,
                    user_id=current_user["user_id"],
                    market_event_id=market_event.id,
                    status=PostStatus.DRAFT,
                    is_customized=market_event.is_customized,
                )

                post_data = await self.create_post_from_dataclass(
                    post_data=post_dataclass
                )
                return post_data
            return existing_post_from_market_event_id

        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def create_customized_post(self, event_title: str, current_user: dict):
        """
        Method to create a customized post based on an event title.

        Args:
            event_title (str): Title of the event to search for.
            current_user (dict): The currently authenticated user.

        Returns:
            None
        """
        try:
            process_customized_news_events_data.delay(
                event_title=event_title,
                user_id=current_user["user_id"],
            )
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def approve_post_by_id(
        self,
        payload: ApprovePostRequestSchema,
        current_user: dict,
    ):
        try:
            return self.post_domain_services.approve_post_by_id(post_id=payload.post_id)
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def publish_posts_by_ids(
        self,
        payload: PublishPostsRequestSchema,
        current_user: dict,
    ):
        try:
            return self.post_domain_services.publish_posts_by_ids(
                post_ids=payload.post_ids
            )
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def update_post(
        self,
        post_id: str,
        post_data: UpdatePostRequestSchema,
        current_user: dict,
    ):
        """
        Updates a post by its ID.

        Args:
            post_id (str): ID of the post to update.
            post_data (dict): The data to update the post with.
            current_user (dict): The currently authenticated user.

        Returns:
            Post: The updated post object.

        Raises:
            PostNotFoundException: If the post with the given ID does not exist.
            PostNotAuthorizedException: If the currently authenticated user does not own the post.
        """

        try:
            post = self.post_domain_services.get_post_by_id(post_id)
            if not post:
                raise PostNotFoundException()

            if str(post.user_id) != str(current_user["user_id"]):
                raise PostNotAuthorizedException()

            post = self.post_domain_services.update_post(post=post, post_data=post_data)
            return post
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def customize_post_content_using_prompt_and_tone(
        self,
        post_id: str,
        payload: CustomizePostRequestSchema,
        current_user: dict,
    ):
        """
        Method to customize a post content using a prompt and tone.

        Args:
            post_id (str): ID of the post to customize.
            payload (CustomizePostRequestSchema): The request payload containing the prompt and tone to use for customization.
            current_user (dict): The currently authenticated user.

        Returns:
            dict: Updated post data.
        """
        try:
            post = self.post_domain_services.get_post_by_id(post_id=post_id)
            if not post:
                raise PostNotFoundException()

            if str(post.user_id) != str(current_user["user_id"]):
                raise PostNotAuthorizedException()

            updated_content = self.openai_services.get_chat_completion(
                user_prompt=PromptEnum.REVISING_FINANCIAL_CONTENT_WITH_TONE_CONTROL_USER_PROMPT.value.format(
                    financial_content=post.description,
                    custom_instructions=payload.prompt,
                    tone_style=payload.content_tone.value,
                )
            )
            post_updated_data = UpdatePostSchema(description=updated_content)
            updated_post = self.post_domain_services.update_post(
                post=post, post_data=post_updated_data
            )
            return updated_post
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def get_published_posts_listings(
        self,
        query_params: GetPublishedPostsListingsQueryParams,
    ):
        """
        Method to get the published posts with search, pagination, and optional filters on source and date range.

        Args:
            query_params (GetPublishedPostsListingsQueryParams): The query parameters for filtering and pagination.
                - search_term (str): The search term to filter posts by title or description.
                - page (int): The page number for pagination.
                - limit (int): The number of items per page for pagination.
                - source (Optional[MarketEventSource]): The market event source to filter by.
                - start_date (Optional[date]): The start date to filter by.
                - end_date (Optional[date]): The end date to filter by.

        Returns:
            PostDataResponseSchema: The response schema containing the list of published posts.
        """
        try:
            offset = (query_params.page - 1) * query_params.limit

            results, count = self.post_domain_services.get_published_posts(
                offset=offset,
                limit=query_params.limit,
                search_term=query_params.search_term,
                source=query_params.source,
                start_date=query_params.start_date,
                end_date=query_params.end_date,
            )

            post_data = [
                GetPostDataModelSchema(**post.__dict__, source=source)
                for post, source in results
            ]

            has_next = offset + query_params.limit < count
            has_previous = query_params.page > 1
            pages = (count + query_params.limit - 1) // query_params.limit

            return PostDataResponseSchema(
                page=query_params.page,
                limit=query_params.limit,
                total_pages=pages,
                total_records=count,
                has_next=has_next,
                has_previous=has_previous,
                data=post_data,
            )

        except Exception as e:
            return ResponseHandler.error(exception=e)
