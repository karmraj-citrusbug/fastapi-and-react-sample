from uuid import UUID

from fastapi import status

from config.response_handler import ResponseHandler
from src.domain.users.services import UserDataClass, UserDomainServices
from src.exceptions.users import (
    AuthenticationException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.infrastructure.email_service import EmailService
from src.infrastructure.security import hash_password, token_services, verify_password
from src.schema.users import (
    LoginUserRequestSchema,
    ResetPasswordRequestSchema,
    SignupUserRequestSchema,
    UpdateUserDomainSchema,
    UpdateUserRequestSchema,
    UserLoginResponseSchema,
    UserResponseSchema,
)


class UserAppServices:
    """
    Class to handle user related operations.
    """

    def __init__(self):
        """
        Constructor for UserAppServices class.
        """
        self.user_domain_services = UserDomainServices()
        self.email_service = EmailService()

    async def create_new_user(self, data: SignupUserRequestSchema):
        """
        Method to create a new user.

        Args:
            data (SignupUserRequestSchema): User registration data.

        Returns:
            User: A User object.

        Raises:
            UserAlreadyExistsException: If the user with the given email already exists.
        """
        try:
            existing_user_by_email = self.user_domain_services.get_user_by_email(
                email=data.email
            )
            if existing_user_by_email:
                raise UserAlreadyExistsException(message="Email already exists")

            # Create user with hashed password
            hashed_password = hash_password(data.password)
            user_dataclass = UserDataClass(
                username=data.username,
                email=data.email,
                password=hashed_password,
            )

            # Create user
            user = self.user_domain_services.get_user_factory().build_entity_with_id(
                data=user_dataclass
            )
            user = self.user_domain_services.create_user(user=user)

            # Generate verification token
            verification_token = token_services.generate_verification_token(
                user_id=str(user.id),
                token_type="verification",
            )

            # Send verification email
            await self.email_service.send_signup_verification_email(
                username=user.username,
                email=user.email,
                token=verification_token,
            )
            return UserResponseSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                is_verified=user.is_verified,
            )
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def verify_email(self, token: str):
        """
        Verify a user's email using a verification token.

        Args:
            token (str): Verification token.

        Returns:
            User: Verified user object.

        Raises:
            AuthenticationException: If verification fails.
            UserNotFoundException: If user with given ID does not exist.
        """
        try:
            # Verify token and get user_id
            token_payload = token_services.verify_token(
                token, expected_type="verification"
            )

            if not token_payload or not token_payload.get("sub"):
                raise AuthenticationException(message="Invalid verification token")

            user_id = token_payload["sub"]
            user = self.user_domain_services.get_user_by_id(user_id=user_id)

            if not user:
                raise UserNotFoundException()

            if user.is_verified:
                raise AuthenticationException(
                    message="Email already verified",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Update user verification status
            self.user_domain_services.update_user_by_id(
                user_id=user.id,
                data=UpdateUserDomainSchema(is_verified=True),
            )

            return UserResponseSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                is_verified=user.is_verified,
            )
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def login(self, data: LoginUserRequestSchema):
        """
        Authenticate a user and generate an access token.

        Args:
            data (LoginUserRequestSchema): User login data containing email and password.

        Returns:
            dict: A dictionary containing the access token and token type.

        Raises:
            AuthenticationException: If authentication fails due to invalid credentials
                                    or unverified email.
        """
        try:
            user = self.user_domain_services.get_user_by_email(email=data.email)

            if not user or not verify_password(data.password, user.password):
                raise AuthenticationException()

            if not user.is_verified:
                raise AuthenticationException(
                    message="Email not verified. Please verify your email first."
                )

            # Generate access token with additional claims
            additional_claims = {"email": user.email, "user_id": str(user.id)}

            access_token = token_services.generate_access_token(
                user_id=str(user.id),
                additional_claims=additional_claims,
            )

            return UserLoginResponseSchema(
                access_token=access_token,
                token_type="bearer",
            )

        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def forgot_password(self, email: str):
        """
        Initiate the password reset process for a user.

        Args:
            email (str): User email to send the reset password email to.

        Returns:
            None

        Raises:
            AuthenticationException: If password reset process fails.
        """
        try:
            user = self.user_domain_services.get_user_by_email(email=email)

            if not user:
                # Return success to prevent user enumeration
                return None

            # Generate reset token
            reset_token = token_services.generate_verification_token(
                user_id=str(user.id),
                token_type="reset",
            )

            # Send reset password email
            await self.email_service.send_forgot_password_email(
                username=user.username,
                email=email,
                token=reset_token,
            )
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def reset_password(self, data: ResetPasswordRequestSchema):
        """
        Reset user's password using a reset token.

        Args:
            data (ResetPasswordRequestSchema): Reset token and new password.

        Returns:
            None

        Raises:
            AuthenticationException: If reset token is invalid or expired.
            UserNotFoundException: If user with given ID does not exist.
        """
        try:
            # Verify reset token and get user_id
            user_id = token_services.verify_reset_token(data.token)

            if not user_id:
                raise AuthenticationException(message="Invalid or expired reset token")

            # Verify user exists
            user = self.user_domain_services.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundException()

            # Hash new password and update
            hashed_password = hash_password(data.new_password)

            self.user_domain_services.update_user_by_id(
                user_id=user_id,
                data=UpdateUserDomainSchema(password=hashed_password),
            )
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def change_password(
        self,
        user_id: str,
        old_password: str,
        new_password: str,
    ):
        """
        Change user's password.

        Args:
            user_id (str): User ID.
            old_password (str): Current password.
            new_password (str): New password.

        Returns:
            None

        Raises:
            AuthenticationException: If current password is incorrect.
            UserNotFoundException: If user with given ID does not exist.
        """
        try:
            user = self.user_domain_services.get_user_by_id(user_id)

            if not user:
                raise UserNotFoundException()

            if not verify_password(old_password, user.password):
                raise AuthenticationException(
                    message="Current password is incorrect",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # Hash new password and update
            hashed_password = hash_password(new_password)
            self.user_domain_services.update_user_by_id(
                user_id=user_id,
                data=UpdateUserDomainSchema(password=hashed_password),
            )

            return None
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def get_user_profile(self, user_id: UUID):
        """
        Method to get a user by id.

        Args:
            user_id (UUID): User's ID.

        Returns:
            User: A User object.

        Raises:
            Exception: If an error occurs while retrieving the user.
        """

        try:
            user = self.user_domain_services.get_user_by_id(user_id)
            return UserResponseSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                is_verified=user.is_verified,
            )

        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def update_user_profile(
        self,
        user_id: UUID,
        updated_user_data: UpdateUserRequestSchema,
    ):
        """
        Method to update a user's profile.

        Args:
            user_id (uuid.UUID): The ID of the user to update.
            updated_user_data (UpdateUserRequestSchema): The data to update the user with.

        Returns:
            User: The updated user object.

        Raises:
            UserNotFoundException: If the user with the given ID does not exist.
        """
        try:
            # check user exist
            if not self.user_domain_services.get_user_by_id(user_id=user_id):
                raise UserNotFoundException()

            # update user
            user = self.user_domain_services.update_user_by_id(
                user_id=user_id,
                data=UpdateUserDomainSchema(username=updated_user_data.username),
            )

            return UserResponseSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                is_verified=user.is_verified,
            )
        except Exception as e:
            return ResponseHandler.error(exception=e)
