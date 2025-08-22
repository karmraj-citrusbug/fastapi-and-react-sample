from dataclasses import asdict, dataclass
from typing import List
from uuid import UUID, uuid4
from datetime import date, datetime, time

from config.db_connection import db_service
from config.response_handler import ResponseHandler
from src.domain.enums import PostStatus, MarketEventSource, ContentTone
from src.domain.market_events.models import MarketEvent
from src.domain.posts.models import Post
from src.exceptions.posts import PostNotDraftedException
from src.schema.posts import PostCountsResponseSchema, UpdatePostSchema


@dataclass(frozen=True)
class PostDataClass:
    """
    Data class for Post model.
    """

    title: str
    description: str
    user_id: str
    market_event_id: UUID
    status: PostStatus = PostStatus.DRAFT
    is_customized: bool = False


class PostFactory:
    """
    PostFactory class for Post model for creating runtime Post Objects
    """

    @staticmethod
    def build_entity_with_id(data: PostDataClass) -> Post:
        """
        Method to create runtime Post object using dataclass.

        Args:
            data (Dict): A dictionary containing broker information.
                - username (str): Name of the broker.
                - email (str): email of the broker.
                - password (str): password of the broker.

        Returns:
            Post: A runtime Post object.
        """
        return Post(id=uuid4(), **asdict(data))


class PostDomainServices:
    def __init__(self):
        """
        Constructor for PostDomainServices class.
        """
        self.db_session = db_service.get_session()

    @staticmethod
    def get_post_factory():
        """
        Method to get PostFactory object.

        Returns:
            PostFactory: A PostFactory object.
        """
        try:
            return PostFactory
        except Exception as e:
            raise ResponseHandler.error(exception=e)

    def __get_post_repository(self):
        """
        Method to get Post repository object.

        Returns:
            Post: A Post repository object.
        """

        try:
            return self.db_session.query(Post)
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def get_posts_by_user_id(
        self,
        user_id: str,
        offset: int = 0,
        limit: int = 10,
        search_term: str = "",
        status: PostStatus | None = None,
        source: MarketEventSource | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        """
        Method to get posts by user ID with search, pagination, and optional filters on status, source, and date range.

        Args:
            user_id (str): The ID of the user.
            offset (int): The offset for pagination.
            limit (int): The limit for pagination.
            search_term (str): The search term to find in the title or description.
            status (PostStatus | None): The status to filter by (optional).
            source (MarketEventSource | None): The market event source to filter by (optional).
            start_date (date | None): The start date of the date range to filter by (optional).
            end_date (date | None): The end date of the date range to filter by (optional).

        Returns:
            tuple[list[Post], int]: A tuple containing the posts and the total count of posts.
        """
        try:
            query = self.__get_post_repository().with_entities(
                Post, MarketEvent.source
            ).join(
                MarketEvent, Post.market_event_id == MarketEvent.id
            ).filter(
                Post.user_id == user_id
            ).order_by(
                Post.updated_at.desc()
            )

            if search_term:
                query = query.filter(
                    Post.title.ilike(f"%{search_term}%")
                    | Post.description.ilike(f"%{search_term}%")
                )

            if status:
                query = query.filter(Post.status == status)

            if source:
                query = query.filter(MarketEvent.source == source)

            if start_date and end_date:
                start_dt = datetime.combine(start_date, time.min)
                end_dt = datetime.combine(end_date, time.max)
                query = query.filter(Post.created_at.between(start_dt, end_dt))

            count = query.count()
            posts = query.offset(offset).limit(limit).all()
            return posts, count
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def get_post_by_id(self, post_id: str) -> Post | None:
        """
        Method to get a post by its ID.

        Args:
            post_id (UUID): The ID of the post.

        Returns:
            Post | None: The Post object if found, else None.
        """
        try:
            post = self.__get_post_repository().get(post_id)
            return post
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)
        
    def get_post_by_id_with_market_event_source(self, post_id: str) -> tuple[Post, MarketEventSource] | None:
        """
        Method to get a post by its ID along with its market event source.

        Args:
            post_id (UUID): The ID of the post.

        Returns:
            tuple[Post, MarketEventSource] | None: The Post object and MarketEvent source if found.
        """
        try:
            query = self.__get_post_repository().with_entities(
                Post, MarketEvent.source
            ).join(
                MarketEvent, Post.market_event_id == MarketEvent.id
            ).filter(Post.id == post_id)

            return query.first()
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def get_post_by_market_event_id(self, market_event_id: str) -> Post | None:
        """
        Method to get a post by its ID.

        Args:
            market_event_id (UUID): The ID of the market event.

        Returns:
            Post | None: The Post object if found, else None.
        """
        try:
            post = (
                self.__get_post_repository()
                .filter(Post.market_event_id == market_event_id)
                .first()
            )
            return post
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def get_post_by_user_id_and_market_event_id(
        self,
        user_id: str,
        market_event_id: str,
    ) -> Post | None:
        """
        Method to get a post by its user ID and market event ID.

        Args:
            user_id (str): The ID of the user.
            market_event_id (str): The ID of the market event.

        Returns:
            Post | None: The Post object if found, else None.
        """
        try:
            post = (
                self.__get_post_repository()
                .filter(
                    Post.user_id == user_id,
                    Post.market_event_id == market_event_id,
                )
                .first()
            )
            return post
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def get_post_counts_by_user_id(self, user_id: str):
        """
        Method to get the counts of posts for a specific user.

        Args:
            user_id (str): The ID of the user whose post counts are being retrieved.

        Returns:
            dict: A dictionary containing the counts of total posts, draft posts,
                published posts, and customized posts for the specified user.
        """
        try:
            query = self.__get_post_repository().filter(Post.user_id == user_id)

            total_posts = query.count()
            draft_posts = query.filter(Post.status == PostStatus.DRAFT).count()
            published_posts = query.filter(Post.status == PostStatus.PUBLISHED).count()

            customized_posts = query.filter(Post.is_customized.is_(True)).count()

            return PostCountsResponseSchema(
                total_posts=total_posts,
                draft_posts=draft_posts,
                published_posts=published_posts,
                customized_posts=customized_posts,
            )
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def create_post(self, post: Post) -> Post:
        """
        Method to create a new post in the database.

        Args:
            post (Post): The Post object to be added to the database.

        Returns:
            Post: The Post object after being added and committed to the database.
        """
        try:
            self.db_session.add(post)
            self.db_session.commit()
            self.db_session.refresh(post)
            return post
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def update_post(
        self,
        post: Post,
        post_data: UpdatePostSchema,
    ) -> Post:
        """
        Updates an existing post with the provided data.

        Args:
            post (Post): The existing post object to be updated.
            post_data (UpdatePostSchema): The data containing updates for the post.

        Returns:
            Post | None: The updated post object if successful, otherwise None.

        Raises:
            Exception: If an error occurs during the update process, a rollback is performed
                    and the exception is handled by the ResponseHandler.
        """
        try:
            update_data = post_data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(post, key, value)

            if "description" in update_data:
                setattr(post, "is_customized", True)
            
            post.status = PostStatus.DRAFT

            self.db_session.commit()
            self.db_session.refresh(post)
            return post
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def approve_post_by_id(self, post_id: str):
        """
        Publishes multiple posts by their IDs.

        Args:
            post_ids (List[str]): IDs of the posts to be published.

        Returns:
            List[Post]: The list of published Post objects.

        Raises:
            Exception: If an error occurs during the publishing process, a rollback is performed
                    and the exception is handled by the ResponseHandler.
        """
        try:
            post = self.get_post_by_id(post_id)

            if post:
                if post.status == PostStatus.DRAFT:
                    post.status = PostStatus.APPROVED
                else:
                    raise PostNotDraftedException()

            self.db_session.commit()
            return post
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def publish_posts_by_ids(self, post_ids: List[str]):
        """
        Publishes multiple posts by their IDs.

        Args:
            post_ids (List[str]): IDs of the posts to be published.

        Returns:
            List[Post]: The list of published Post objects.

        Raises:
            Exception: If an error occurs during the publishing process, a rollback is performed
                    and the exception is handled by the ResponseHandler.
        """
        try:
            posts = [self.get_post_by_id(post_id) for post_id in post_ids]

            for post in posts:
                if post and post.status == PostStatus.APPROVED:
                    post.status = PostStatus.PUBLISHED

            self.db_session.commit()
            return posts
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)

    def get_published_posts(
        self,
        offset: int = 0,
        limit: int = 10,
        search_term: str = "",
        source: MarketEventSource | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        """
        Retrieves a list of published posts with optional filtering and pagination.

        Args:
            offset (int): The offset for pagination.
            limit (int): The limit for pagination.
            search_term (str): The search term to find in the title or description.
            source (MarketEventSource | None): The market event source to filter by (optional).
            start_date (date | None): The start date of the date range to filter by (optional).
            end_date (date | None): The end date of the date range to filter by (optional).

        Returns:
            tuple[list[Post], int]: A tuple containing the posts and the total count of posts.
        """
        try:
            query = self.__get_post_repository().with_entities(
                Post, MarketEvent.source
            ).join(
                MarketEvent, Post.market_event_id == MarketEvent.id
            ).filter(
                Post.status == PostStatus.PUBLISHED
            ).order_by(
                Post.updated_at.desc()
            )

            if search_term:
                query = query.filter(
                    Post.title.ilike(f"%{search_term}%")
                    | Post.description.ilike(f"%{search_term}%")
                )

            if source:
                query = query.filter(MarketEvent.source == source)

            if start_date and end_date:
                start_dt = datetime.combine(start_date, time.min)
                end_dt = datetime.combine(end_date, time.max)
                query = query.filter(Post.created_at.between(start_dt, end_dt))

            count = query.count()
            posts = query.offset(offset).limit(limit).all()
            return posts, count
        except Exception as e:
            self.db_session.rollback()
            raise ResponseHandler.error(exception=e)
        