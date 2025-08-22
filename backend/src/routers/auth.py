from fastapi import APIRouter, Depends

from config.response_handler import ResponseHandler
from src.application.users import UserAppServices
from src.infrastructure.security import get_current_user
from src.schema.messages_enums import AuthEnums
from src.schema.users import (
    ChangePasswordResponseSchema,
    ChangePasswordSchema,
    ForgotPasswordRequestSchema,
    ForgotPasswordResponseSchema,
    LoginResponseSchema,
    LoginUserRequestSchema,
    ResetPasswordRequestSchema,
    ResetPasswordResponseSchema,
    SignUpResponseSchema,
    SignupUserRequestSchema,
    TokenPayload,
    VerifyEmailResponseSchema,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup", response_model=SignUpResponseSchema)
async def sign_up(user_data: SignupUserRequestSchema):
    """
    Endpoint to register a new user.

    `Args:`
    - user_data (SignupUserRequestSchema): User registration data.

    `Returns:`
    - SignUpResponseSchema: Success message with user data.

    `Raises:`
    - HTTPException: If the registration process fails.
    """

    try:
        user_app_services = UserAppServices()
        user = await user_app_services.create_new_user(data=user_data)
        return ResponseHandler.success(
            message=AuthEnums.SIGN_UP_SUCCESS.value,
            data=user,
        )
    except Exception as e:
        return ResponseHandler.error(exception=e)


@router.post("/verify-email", response_model=VerifyEmailResponseSchema)
async def verify_email(payload: TokenPayload):
    """
    Endpoint to verify a user's email using a verification token.

    `Args:`
    - payload (TokenPayload): Verification token.

    `Returns:`
    - dict: Success message with user data.

    `Raises:`
    - HTTPException: If the verification process fails.
    """
    try:
        user_app_services = UserAppServices()
        user = await user_app_services.verify_email(token=payload.token)
        return ResponseHandler.success(
            message=AuthEnums.EMAIL_VERIFICATION_SUCCESS.value,
            data=user,
        )
    except Exception as e:
        return ResponseHandler.error(exception=e)


@router.post("/login", response_model=LoginResponseSchema)
async def login(user_data: LoginUserRequestSchema):
    """
    Endpoint to authenticate a user and generate an access token.

    `Args:`
    - user_data (LoginUserRequestSchema): User login data.

    `Returns:`
    - LoginResponseSchema: Success message with user data and access token.

    `Raises:`
    - HTTPException: If authentication fails.
    """
    try:
        user_app_services = UserAppServices()
        token_data = await user_app_services.login(data=user_data)
        return ResponseHandler.success(
            message=AuthEnums.LOGIN_SUCCESS.value,
            data=token_data,
        )
    except Exception as e:
        return ResponseHandler.error(exception=e)


@router.post("/forgot-password", response_model=ForgotPasswordResponseSchema)
async def forgot_password(data: ForgotPasswordRequestSchema):
    """
    Endpoint to initiate the password reset process for a user.

    `Args:`
    - data (ForgotPasswordRequestSchema): User email to send the reset password email to.

    `Returns:`
    - ForgotPasswordResponseSchema: Success message if the email is sent.

    `Raises:`
    - HTTPException: If the password reset process fails.
    """
    try:
        user_app_services = UserAppServices()
        await user_app_services.forgot_password(email=data.email)
        return ResponseHandler.success(
            message=AuthEnums.FORGOT_PASSWORD_EMAIL_SENT_SUCCESS.value
        )
    except Exception as e:
        return ResponseHandler.error(exception=e)


@router.post("/reset-password", response_model=ResetPasswordResponseSchema)
async def reset_password(data: ResetPasswordRequestSchema):
    """
    Endpoint to reset a user's password using a reset token.

    `Args:`
    - data (ResetPasswordRequestSchema): Reset token and new password.

    `Returns:`
    - ResetPasswordResponseSchema: Success message if the password is reset.

    `Raises:`
    - HTTPException: If the password reset process fails.
    """

    try:
        user_app_services = UserAppServices()
        await user_app_services.reset_password(data=data)
        return ResponseHandler.success(message=AuthEnums.RESET_PASSWORD_SUCCESS.value)
    except Exception as e:
        return ResponseHandler.error(exception=e)


@router.post("/change-password", response_model=ChangePasswordResponseSchema)
async def change_password(
    payload: ChangePasswordSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Endpoint to change the password of the currently logged in user.

    `Args:`
    - payload (ChangePasswordSchema): The old and new passwords.

    `Returns:`
    - ChangePasswordResponseSchema: Success message if the password is changed.

    `Raises:`
    - HTTPException: If the password change process fails.
    """

    try:
        user_app_services = UserAppServices()
        await user_app_services.change_password(
            user_id=current_user["user_id"],
            old_password=payload.old_password,
            new_password=payload.new_password,
        )
        return ResponseHandler.success(
            message=AuthEnums.PASSWORD_CHANGED_SUCCESS.value,
        )
    except Exception as e:
        return ResponseHandler.error(exception=e)
