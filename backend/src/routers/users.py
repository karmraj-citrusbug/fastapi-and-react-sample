from fastapi import APIRouter, Depends

from config.response_handler import ResponseHandler
from src.application.users import UserAppServices
from src.infrastructure.security import get_current_user
from src.schema.users import (
    UpdateUserRequestSchema,
    UpdateUserResponseSchema,
    UserProfileResponseSchema,
)

from ..schema.messages_enums import UserEnums

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserProfileResponseSchema)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Endpoint to retrieve the profile of the logged-in user.

    `Args:`
    - current_user (dict): The currently authenticated user.

    `Returns:`
    - UserProfileResponseSchema: The user profile data.

    `Raises:`
    - HTTPException: If an error occurs while retrieving the user profile.
    """
    user_app_services = UserAppServices()
    user = await user_app_services.get_user_profile(user_id=current_user["user_id"])
    return ResponseHandler.success(
        message=UserEnums.USER_FETCH_SUCCESS,
        data=user,
    )


@router.patch("/me", response_model=UpdateUserResponseSchema)
async def update_user_profile(
    user_data: UpdateUserRequestSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Endpoint to update the profile of the logged-in user.

    `Args:`
    - user_data (UpdateUserRequestSchema): The data to update the user profile with.
    - current_user (dict): The currently authenticated user.

    `Returns:`
    - UpdateUserResponseSchema: The updated user profile data.

    `Raises:`
    - HTTPException: If an error occurs while updating the user profile.
    """
    user_app_services = UserAppServices()
    user = await user_app_services.update_user_profile(
        user_id=current_user["user_id"],
        updated_user_data=user_data,
    )
    return ResponseHandler.success(
        message=UserEnums.USER_UPDATE_SUCESS.value,
        data=user,
    )
