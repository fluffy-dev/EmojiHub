from fastapi import HTTPException

from src.user.dto import FindUserDTO, UserDTO
from src.user.entity import UserEntity
from src.user.depends.service import IUserService
from src.user.exceptions import UserNotFound
from src.user.hash import verify

from src.auth.depends.token_service import ITokenService
from src.auth.exceptions import InvalidCredentials, InvalidToken
from src.auth.dto import LoginDTO, TokenDTO, RegistrationDTO, AccessTokenDTO, RefreshTokenDTO


class AuthService:
    """
    **Description**: Core service class for handling user authentication operations.

    **Dependencies**:
    - `user_service`: *IUserService* - Manages user creation, retrieval, etc.
    - `token_service`: *ITokenService* - Handles token generation and validation.

    **Methods**:
    - `login`: Authenticates a user and returns tokens.
    - `refresh`: Generates a new access token from a refresh token.
    - `get_current_user`: Retrieves the user from an access token.
    - `registration`: Creates a new user.

    **Usage**: Injected into API routes to perform authentication tasks.
    """
    def __init__(self, user_service: IUserService, token_service: ITokenService):
        self.user_service = user_service
        self.token_service = token_service

    async def login(self, dto: LoginDTO) -> TokenDTO:
        """
        **Description**: Authenticates a user and generates access/refresh tokens.

        **Input**:
        - `dto`: *LoginDTO* - Contains `login` and `password`.

        **Output**:
        - *TokenDTO* - Contains `access_token` and `refresh_token`.

        **Exceptions**:
        - `UserNotFound`: If no user matches the provided login.
        - `InvalidCredentials`: If the password is incorrect.

        **How It Works**:
        - Fetches the user by login using `user_service.get_user`.
        - Verifies the password using a hash comparison.
        - Generates tokens via `token_service.create_tokens` if credentials are valid.
        """
        user: UserDTO = await self.user_service.get_user(dto=FindUserDTO(login=dto.login))
        if user is None:
            raise UserNotFound(f"User with login: '{dto.login}' not found")
        if not verify(user.password, dto.password):
            raise InvalidCredentials("Login or Password is incorrect")
        return await self.token_service.create_tokens(user)

    async def refresh(self, dto: RefreshTokenDTO) -> AccessTokenDTO:
        """
        **Description**: Refreshes an access token using a valid refresh token.

        **Input**:
        - `dto`: *RefreshTokenDTO* - Contains `refresh_token`.

        **Output**:
        - *AccessTokenDTO* - Contains a new `access_token`.

        **Exceptions**:
        - `InvalidToken`: If the token isn’t a refresh token or is invalid.
        - `UserNotFound`: If the user tied to the token doesn’t exist.

        **How It Works**:
        - Decodes the refresh token to verify its type and user info.
        - Fetches the user by ID from `user_service`.
        - Generates a new access token if valid.
        """
        payload = await self.token_service.decode_token(dto.refresh_token)
        if payload.get("token_type") != "refresh":
            raise InvalidToken("Provided token is not a refresh token")

        user_info = payload.get("user")
        user: UserDTO = await self.user_service.get(int(user_info["user_id"]))

        if user is None:
            raise UserNotFound(f"User with id: {user_info['user_id']} not found")

        tokens = await self.token_service.create_tokens(user)
        return AccessTokenDTO(access_token=tokens.access_token)

    async def get_current_user(self, dto: AccessTokenDTO) -> UserDTO:
        """
        **Description**: Retrieves the authenticated user from an access token.

        **Input**:
        - `dto`: *AccessTokenDTO* - Contains `access_token`.

        **Output**:
        - *UserDTO* - Details of the authenticated user.

        **Exceptions**:
        - `InvalidToken`: If the token lacks user info or is invalid.
        - `UserNotFound`: If the user doesn’t exist.

        **How It Works**:
        - Decodes the access token to extract user info.
        - Retrieves the user by ID using `user_service.get`.
        """
        payload = await self.token_service.decode_token(dto.access_token)
        user_info = payload.get("user")
        if user_info is None:
            raise InvalidToken("Token does not contain user information")
        return await self.user_service.get(int(user_info["user_id"]))

    async def registration(self, dto: RegistrationDTO) -> UserDTO:
        """
        **Description**: Registers a new user in the system.

        **Input**:
        - `dto`: *RegistrationDTO* - Contains `name`, `surname`, `login`, and `password`.

        **Output**:
        - *UserDTO* - Details of the newly created user.

        **Exceptions**:
        - `AlreadyExistError`: If the login is already in use.

        **How It Works**:
        - Converts DTO to a `UserEntity`.
        - Uses `user_service.create` to persist the user.
        """
        registration_data = dto.model_dump()
        user_entity = UserEntity(**registration_data)
        return await self.user_service.create(user_entity)