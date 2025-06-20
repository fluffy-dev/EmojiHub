from src.config.security import settings
from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher

password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    """
    **Description**: Hashes a plaintext password using the Argon2 algorithm.

    **Parameters**:
    - `password`: *str* - Plaintext password to be hashed.

    **Returns**:
    - *str*: Hashed password string.

    **Usage**: Called before storing passwords in the database to ensure security.
    """
    salt = settings.secret_key
    hashed = password_hasher.hash(password.encode(), salt=salt.encode("utf-8"))
    return hashed

def verify(password_hash: str, password: str) -> bool:
    """
    **Description**: Verifies a plaintext password against a stored hash.

    **Parameters**:
    - `password_hash`: *str* - Stored hashed password.
    - `password`: *str* - Plaintext password to verify.

    **Returns**:
    - *bool*: True if the password matches the hash, False otherwise.

    **Raises**:
    - `RuntimeError`: If an unexpected error occurs during verification.

    **Usage**: Used during authentication to validate user login credentials.
    """
    try:
        return password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False
    except Exception as e:
        raise RuntimeError(f"Something broken in verify {str(e)}")