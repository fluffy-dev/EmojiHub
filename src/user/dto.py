from pydantic import BaseModel, constr, model_validator

class FindUserDTO(BaseModel):
    """
    **Description**: Data Transfer Object (DTO) for finding or filtering users based on specified criteria.

    **Fields**:
    - `id`: *int* - Optional user ID for filtering.
    - `name`: *constr(max_length=20)* - Optional user name for filtering (max 20 characters).
    - `surname`: *constr(max_length=20)* - Optional user surname for filtering (max 20 characters).
    - `login`: *str* - Optional user login for filtering.

    **Validation**:
    - At least one field must be provided for the search operation.

    **Usage**: Used in `get_user` and `filter` operations to define search criteria.
    """
    id: int = None
    name: constr(max_length=20) = None
    surname: constr(max_length=20) = None
    login: str = None

    @model_validator(mode='after')
    def check_at_least_one_value(self):
        """Ensure at least one field is not None."""
        if not any(v is not None for v in self.__dict__.values()):
            raise ValueError('At least one field must be provided.')
        return self

class UserDTO(BaseModel):
    """
    **Description**: Represents a user’s data for transfer and display purposes.

    **Fields**:
    - `id`: *int* - Unique identifier of the user (optional during creation).
    - `name`: *constr(max_length=20)* - User’s first name (max 20 characters).
    - `surname`: *constr(max_length=20)* - User’s last name (max 20 characters).
    - `login`: *str* - User’s login identifier (e.g., username or email).
    - `password`: *str* - Hashed password (optional, not included in responses).
    - `is_admin`: *bool* - Indicates if the user has admin privileges (default: False).

    **Usage**: Used to serialize user data for API responses or input validation.
    """
    id: int = None
    name: constr(max_length=20)
    surname: constr(max_length=20)
    login: str
    password: str = None
    is_admin: bool = False

class UpdateUserDTO(BaseModel):
    """
    **Description**: Data Transfer Object (DTO) for updating user details.

    **Fields**:
    - `name`: *constr(max_length=20)* - Optional new first name (max 20 characters).
    - `surname`: *constr(max_length=20)* - Optional new last name (max 20 characters).

    **Validation**:
    - At least one field must be provided for the update operation.

    **Usage**: Passed to the update endpoint to modify user name or surname.
    """
    name: constr(max_length=20) = None
    surname: constr(max_length=20) = None

    @model_validator(mode='after')
    def check_at_least_one_value(self):
        """Ensure at least one field is not None."""
        if not any(v is not None for v in self.__dict__.values()):
            raise ValueError('At least one field must be provided.')
        return self

class UpdatePasswordDTO(BaseModel):
    """
    **Description**: Data Transfer Object (DTO) for updating a user’s password.

    **Fields**:
    - `password`: *str* - New plaintext password to be hashed and stored.

    **Usage**: Used in password update operations via the PATCH endpoint.
    """
    password: str