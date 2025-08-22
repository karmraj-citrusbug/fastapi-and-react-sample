from dataclasses import asdict, dataclass
from uuid import UUID, uuid4

from fastapi.responses import JSONResponse

from config.db_connection import db_service
from config.response_handler import ResponseHandler
from src.domain.users.models import User
from src.schema.users import UpdateUserDomainSchema


@dataclass(frozen=True)
class UserDataClass:
    """
    Data class for User model.
    """

    username: str
    email: str
    password: str


class UserFactory:
    """
    UserFactory class for User model for creating runtime User Objects
    """

    @staticmethod
    def build_entity_with_id(data: UserDataClass) -> User:
        """
        Method to create runtime User object using dataclass.

        Args:
            data (Dict): A dictionary containing broker information.
                - username (str): Name of the broker.
                - email (str): email of the broker.
                - password (str): password of the broker.

        Returns:
            User: A runtime User object.
        """
        return User(id=uuid4(), **asdict(data))


class UserDomainServices:
    def __init__(self):
        """
        Constructor for UserDomainServices class.
        """
        self.db_session = db_service.get_session()

    @staticmethod
    def get_user_factory():
        """
        Method to get UserFactory object.

        Returns:
            UserFactory: A UserFactory object.
        """
        try:
            return UserFactory
        except Exception as e:
            return ResponseHandler.error(exception=e)

    def __get_user_repo(self):
        """
        Method to get User repository.

        Returns:
            User: A User repository.
        """
        try:
            return self.db_session.query(User)
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def get_user_by_id(self, user_id: UUID) -> User | JSONResponse:
        """
        Method to get a user by id.

        Args:
            user_id (uuid.UUID): User id.

        Returns:
            User: A User object.
        """
        try:
            user = self.__get_user_repo().get(user_id)
            return user
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def create_user(self, user: User):
        """
        Method to create a user.

        Args:
            user (User): A User object.

        Returns:
            User: A User object.
        """
        try:
            self.db_session.add(user)
            self.db_session.commit()
            self.db_session.refresh(user)
            return user
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def update_user_by_id(
        self, user_id: UUID, data: UpdateUserDomainSchema
    ) -> User | JSONResponse:
        """
        Method to update a user by id.

        Args:
            user_id (uuid.UUID): User id.
            data (dict): Dictionary containing user data to update.

        Returns:
            User: Updated User object.
        """
        try:
            self.__get_user_repo().filter(User.id == user_id).update(
                data.model_dump(exclude_unset=True)
            )
            self.db_session.commit()
            user = self.__get_user_repo().get(user_id)
            return user
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def delete_user_by_id(self, user_id: UUID):
        """
        Method to delete a user by id.

        Args:
            user_id (uuid.UUID): User id.

        Returns:
            User: Deleted User object.
        """
        try:
            user = self.__get_user_repo().filter(User.id == user_id).delete()
            self.db_session.commit()
            return user
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def get_user_by_email(self, email: str):
        """
        Method to get a user by email.

        Args:
            email (str): User email.

        Returns:
            User: A User object.
        """
        try:
            user = self.__get_user_repo().filter(User.email == email).first()
            return user
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def is_user_exist_by_id(self, user_id: str):
        """
        Method to check if a user exists.

        Args:
            email (str): User email.

        Returns:
            bool: True if user exists, False otherwise.
        """
        try:
            user = self.__get_user_repo().filter(user_id).exists()
            return user
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)
