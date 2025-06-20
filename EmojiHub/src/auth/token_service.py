from typing import Dict, Any
from jwt import ExpiredSignatureError, PyJWTError, decode, encode, get_unverified_header
from datetime import datetime, timedelta

from src.auth.dto import TokenPayload, TokenUser, TokenDTO
from src.auth.exceptions import InvalidToken, TokenExpired, InvalidSignatureError
from src.config.jwt_config import config_token
from src.config.security import settings
from src.user.dto import UserDTO

class TokenService:
    """
    **Description**: Manages creation, encoding, decoding, and validation of JWT tokens.

    **Configuration**:
    - `access_token_lifetime`: *int* - Lifetime of access tokens (seconds).
    - `refresh_token_lifetime`: *int* - Lifetime of refresh tokens (seconds).
    - `secret_key`: *str* - Key for signing tokens.
    - `algorithm`: *str* - Algorithm for token signatures (e.g., HS256).

    **Methods**:
    - `create_tokens`: Generates access/refresh token pair.
    - `generate_access_token`: Creates an access token.
    - `generate_refresh_token`: Creates a refresh token.
    - `encode_token`: Encodes a payload into a JWT.
    - `decode_token`: Decodes a JWT into its payload.
    - `_validate_token`: Validates token algorithm.
    """
    def __init__(self) -> None:
        self.access_token_lifetime = config_token.ACCESS_TOKEN_LIFETIME
        self.refresh_token_lifetime = config_token.REFRESH_TOKEN_LIFETIME
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm

    async def create_tokens(self, dto: UserDTO) -> TokenDTO:
        """
        **Description**: Generates a pair of access and refresh tokens.

        **Input**:
        - `dto`: *UserDTO* - User data (id, name, etc.).

        **Output**:
        - *TokenDTO* - Contains `access_token` and `refresh_token`.

        **How It Works**:
        - Calls `generate_access_token` and `generate_refresh_token`.
        - Packages results into a `TokenDTO`.
        """
        access_token = await self.generate_access_token(dto)
        refresh_token = await self.generate_refresh_token(dto)
        return TokenDTO(access_token=access_token, refresh_token=refresh_token)

    def _validate_token(self, token: str) -> str:
        """
        **Description**: Validates a token’s signing algorithm.

        **Input**:
        - `token`: *str* - JWT token to validate.

        **Output**:
        - *str* - The validated token.

        **Exceptions**:
        - `InvalidSignatureError`: If the algorithm doesn’t match.

        **How It Works**:
        - Checks the token header for the algorithm.
        - Raises an error if it doesn’t match the configured algorithm.
        """
        token_info = get_unverified_header(token)

        if token_info.get("alg") != self.algorithm:
            raise InvalidSignatureError("Token signature mismatch")

        return token

    async def encode_token(self, payload: TokenPayload) -> str:
        """
        **Description**: Encodes a payload into a JWT token.

        **Input**:
        - `payload`: *TokenPayload* - Data to encode (token type, user, timestamps).

        **Output**:
        - *str* - Encoded JWT token.

        **How It Works**:
        - Uses PyJWT’s `encode` with the secret key and algorithm.
        """
        return encode(payload.model_dump(), self.secret_key, algorithm=self.algorithm)

    async def decode_token(self, token: str) -> Dict[str, Any]:
        """
        **Description**: Decodes a JWT token into its payload.

        **Input**:
        - `token`: *str* - JWT token to decode.

        **Output**:
        - *Dict[str, Any]* - Decoded payload (e.g., {"token_type": "access", "user": {...}}).

        **Exceptions**:
        - `TokenExpired`: If the token has expired.
        - `InvalidToken`: If the token is malformed or invalid.

        **How It Works**:
        - Validates the token’s algorithm.
        - Decodes using PyJWT, handling expiration and errors.
        """
        try:
            self._validate_token(token)
            return decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise TokenExpired("Token is expired")
        except PyJWTError:
            raise InvalidToken("Token is invalid")

    async def generate_access_token(self, dto: UserDTO) -> str:
        """
        **Description**: Generates an access token for a user.

        **Input**:
        - `dto`: *UserDTO* - User data (id, name, etc.).

        **Output**:
        - *str* - JWT access token.

        **How It Works**:
        - Creates a `TokenPayload` with type "access" and user data.
        - Sets expiration based on `access_token_lifetime`.
        - Encodes the payload into a token.
        """
        payload = TokenPayload(
            token_type="access",
            user=TokenUser(user_id=int(dto.id), user_name=str(dto.name)),
            exp=int((datetime.now() + timedelta(seconds=self.access_token_lifetime)).timestamp()),
            iat=int(datetime.now().timestamp()),
        )
        return await self.encode_token(payload)

    async def generate_refresh_token(self, dto: UserDTO) -> str:
        """
        **Description**: Generates a refresh token for a user.

        **Input**:
        - `dto`: *UserDTO* - User data (id, name, etc.).

        **Output**:
        - *str* - JWT refresh token.

        **How It Works**:
        - Creates a `TokenPayload` with type "refresh" and user data.
        - Sets expiration based on `refresh_token_lifetime`.
        - Encodes the payload into a token.
        """
        payload = TokenPayload(
            token_type="refresh",
            user=TokenUser(user_id=int(dto.id), user_name=str(dto.name)),
            exp=int((datetime.now() + timedelta(seconds=self.refresh_token_lifetime)).timestamp()),
            iat=int(datetime.now().timestamp()),
        )
        return await self.encode_token(payload)