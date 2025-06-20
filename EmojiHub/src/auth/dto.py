from pydantic import BaseModel, Field, constr

class TokenUser(BaseModel):
    """
    **Description**: Represents the user data embedded within a JWT token.

    **Fields**:
    - `user_id`: *int* - The unique identifier of the user.
    - `user_name`: *str* - The name of the user.

    **Usage**: Used as part of the `TokenPayload` to embed user information in tokens.
    """
    user_id: int
    user_name: str

class TokenPayload(BaseModel):
    """
    **Description**: Defines the structure of a JWT token's payload.

    **Fields**:
    - `token_type`: *str* - Type of token, either "access" or "refresh" (defaults to "access").
    - `user`: *TokenUser* - Embedded user data.
    - `exp`: *int* - Expiration timestamp (Unix timestamp).
    - `iat`: *int* - Issued-at timestamp (Unix timestamp).

    **Usage**: Encoded into JWT tokens to carry authentication data.
    """
    token_type: str = "access"
    user: TokenUser
    exp: int = Field()
    iat: int = Field()

class LoginDTO(BaseModel):
    """
    **Description**: Data Transfer Object (DTO) for user login credentials.

    **Fields**:
    - `login`: *str* - The user's login identifier (e.g., username or email).
    - `password`: *str* - The user's plaintext password.

    **Usage**: Passed to the login endpoint to authenticate a user.
    """
    login: str
    password: str

class RegistrationDTO(BaseModel):
    """
    **Description**: Data Transfer Object (DTO) for user registration details.

    **Fields**:
    - `name`: *str* - User's first name (max length: 20 characters).
    - `surname`: *str* - User's last name (max length: 20 characters).
    - `login`: *str* - User's login identifier (e.g., username or email).
    - `password`: *str* - User's password (min length: 8 characters).

    **Usage**: Used in the registration endpoint to create a new user.
    """
    name: constr(max_length=20)
    surname: constr(max_length=20)
    login: str
    password: constr(min_length=8)

class TokenDTO(BaseModel):
    """
    **Description**: Data Transfer Object (DTO) for returning access and refresh tokens.

    **Fields**:
    - `access_token`: *str* - JWT token for accessing protected resources.
    - `refresh_token`: *str* - JWT token for refreshing the access token.

    **Usage**: Returned after successful login or token creation.
    """
    access_token: str
    refresh_token: str

class RefreshTokenDTO(BaseModel):
    """
    **Description**: Data Transfer Object (DTO) for refresh token input.

    **Fields**:
    - `refresh_token`: *str* - The JWT refresh token to be validated and used.

    **Usage**: Provided to the refresh endpoint to obtain a new access token.
    """
    refresh_token: str

class AccessTokenDTO(BaseModel):
    """
    **Description**: Data Transfer Object (DTO) for access token input or output.

    **Fields**:
    - `access_token`: *str* - The JWT access token.

    **Usage**: Used as input to retrieve user data or as output when refreshing tokens.
    """
    access_token: str