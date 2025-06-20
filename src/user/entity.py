from dataclasses import dataclass

@dataclass
class UserEntity:
    """
    **Description**: Represents a user entity for creation or internal processing.

    **Fields**:
    - `name`: *str* - User’s first name.
    - `surname`: *str* - User’s last name.
    - `login`: *str* - User’s login identifier.
    - `password`: *str | None* - Plaintext password (hashed before storage, optional).
    - `is_admin`: *bool* - Indicates if the user has admin privileges (default: False).

    **Usage**: Used as input for creating or updating a user in the service layer.
    """
    name: str
    surname: str
    login: str
    password: str | None = None
    is_admin: bool = False