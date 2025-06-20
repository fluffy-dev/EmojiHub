class AuthError(Exception):
    """
    **Description**: Base exception class for all authentication-related errors.

    **Usage**: Inherited by specific authentication exceptions to provide a common base.
    """

class InvalidCredentials(AuthError):
    """
    **Description**: Raised when login credentials (login/password) are invalid.

    **Cause**: Triggered if the login doesn’t exist or the password doesn’t match.

    **Usage**: Used in login operations to signal authentication failure.
    """

class InvalidToken(AuthError):
    """
    **Description**: Raised when a JWT token is malformed or invalid.

    **Cause**: Occurs if the token structure is incorrect or lacks required data.

    **Usage**: Thrown during token decoding or validation processes.
    """

class TokenExpired(AuthError):
    """
    **Description**: Raised when a JWT token has exceeded its expiration time.

    **Cause**: Triggered when the `exp` field indicates the token is no longer valid.

    **Usage**: Used in token validation to enforce token lifetime.
    """

class InvalidSignatureError(AuthError):
    """
    **Description**: Raised when a JWT token’s signature is invalid or doesn’t match the expected algorithm.

    **Cause**: Occurs if the token was tampered with or signed with a different key/algorithm.

    **Usage**: Thrown during token validation to ensure security.
    """