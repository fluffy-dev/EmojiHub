from fastapi import APIRouter, status, Header, Depends
from typing import Optional

from src.auth.dto import (
    LoginDTO, TokenDTO, RegistrationDTO,
    AccessTokenDTO, RefreshTokenDTO,
)
from src.auth.depends.service import IAuthService, AuthService
from src.user.dto import UserDTO

from src.protection import PermissionChecker

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def register(dto: RegistrationDTO, auth_service: IAuthService, user_with_permission: UserDTO = Depends(PermissionChecker({"user:create"})),):
    """
    **Description**: Registers a new user in the system.

    **Input**:
    - `dto`: *RegistrationDTO* - User details (name, surname, login, password).
    - `auth_service`: *IAuthService* - Dependency-injected authentication service.

    **Output**:
    - *UserDTO* - Details of the newly created user (id, name, surname, login, etc.).

    **Exceptions**:
    - `AlreadyExistError`: If the login is already taken.

    **How It Works**:
    - Validates the input DTO.
    - Delegates to `AuthService.registration` to create the user.
    - Returns the created user’s details.

    **Requires admin privileges**

    **HTTP Status**: 201 Created
    """
    auth_service: AuthService
    return await auth_service.registration(dto)

@router.post("/login", response_model=TokenDTO)
async def login(dto: LoginDTO, auth_service: IAuthService):
    """
    **Description**: Authenticates a user and returns access/refresh tokens.

    **Input**:
    - `dto`: *LoginDTO* - User credentials (login, password).
    - `auth_service`: *IAuthService* - Dependency-injected authentication service.

    **Output**:
    - *TokenDTO* - Contains `access_token` and `refresh_token`.

    **Exceptions**:
    - `InvalidCredentials`: If login or password is incorrect.
    - `UserNotFound`: If the user doesn’t exist.

    **How It Works**:
    - Validates credentials via `AuthService.login`.
    - Generates and returns JWT tokens upon successful authentication.

    **Requires no privileges**

    **HTTP Status**: 200 OK
    """
    auth_service: AuthService
    return await auth_service.login(dto)

@router.post("/refresh", response_model=AccessTokenDTO)
async def refresh_token(
    auth_service: IAuthService,
    user: AuthUser,
    token: Optional[str] = Header(default=None),
):
    """
    **Description**: Refreshes an access token using a valid refresh token.

    **Input**:
    - `auth_service`: *IAuthService* - Dependency-injected authentication service.
    - `token`: *str* - Refresh token provided in the HTTP header (optional).

    **Output**:
    - *AccessTokenDTO* - Contains a new `access_token`.

    **Exceptions**:
    - `InvalidToken`: If the refresh token is invalid or not a refresh token.
    - `TokenExpired`: If the refresh token has expired.
    - `InvalidSignatureError`: If the token’s signature is invalid.
    - `UserNotFound`: If the associated user doesn’t exist.

    **How It Works**:
    - Extracts the refresh token from the header.
    - Delegates to `AuthService.refresh` to validate and generate a new access token.

    **Requires user privileges**

    **HTTP Status**: 200 OK
    """
    auth_service: AuthService
    return await auth_service.refresh(RefreshTokenDTO(refresh_token=token))

@router.post("/me", response_model=UserDTO)
async def get_current_user(
    auth_service: IAuthService,
    user: AuthUser,
    access_token: Optional[str] = Header(default=None),
):
    """
    **Description**: Retrieves the current authenticated user based on an access token.

    **Input**:
    - `auth_service`: *IAuthService* - Dependency-injected authentication service.
    - `access_token`: *str* - Access token provided in the HTTP header (optional).

    **Output**:
    - *UserDTO* - Details of the authenticated user.

    **Exceptions**:
    - `InvalidToken`: If the access token is invalid.
    - `TokenExpired`: If the access token has expired.
    - `InvalidSignatureError`: If the token’s signature is invalid.
    - `UserNotFound`: If the associated user doesn’t exist.

    **How It Works**:
    - Extracts the access token from the header.
    - Uses `AuthService.get_current_user` to decode the token and fetch the user.

    **Requires user privileges**

    **HTTP Status**: 200 OK
    """
    auth_service: AuthService
    return await auth_service.get_current_user(
        AccessTokenDTO(access_token=access_token)
    )