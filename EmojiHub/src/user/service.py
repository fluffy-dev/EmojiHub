from typing import List, Optional
from src.user.depends.repository import IUserRepository
from src.user.dto import FindUserDTO, UserDTO, UpdateUserDTO, UpdatePasswordDTO
from src.user.entity import UserEntity
from src.user.hash import hash_password

class UserService:
    """
    **Description**: Service layer for managing user-related business logic.

    **Attributes**:
    - `repository`: *IUserRepository* - Injected repository for database operations.

    **Methods**:
    - `create`: Creates a new user.
    - `get_user`: Finds a user by criteria.
    - `filter`: Filters users by criteria with pagination.
    - `get_list`: Retrieves a list of users with pagination.
    - `get`: Retrieves a user by ID.
    - `update`: Updates a user’s details.
    - `delete`: Deletes a user by ID.
    - `update_password`: Updates a user’s password.

    **Usage**: Acts as an intermediary between the API router and repository layers.
    """
    def __init__(self, repository: IUserRepository):
        """
        **Description**: Initializes the UserService with a repository instance.

        **Parameters**:
        - `repository`: *IUserRepository* - Repository for database access.
        """
        self.repository = repository

    async def create(self, entity: UserEntity) -> UserDTO:
        """
        **Description**: Creates a new user in the system.

        **Parameters**:
        - `entity`: *UserEntity* - Data for the new user.

        **Returns**:
        - *UserDTO*: Details of the created user.

        **Raises**:
        - `AlreadyExistError`: If the login is already in use.

        **Usage**: Hashes the password and persists the user via the repository.
        """
        entity.password = hash_password(entity.password)
        return await self.repository.create(entity)

    async def get_user(self, dto: FindUserDTO) -> Optional[UserDTO]:
        """
        **Description**: Finds a single user based on search criteria.

        **Parameters**:
        - `dto`: *FindUserDTO* - Criteria for finding the user.

        **Returns**:
        - *Optional[UserDTO]*: User details if found, otherwise None.

        **Raises**:
        - `UserIsNotUnique`: If multiple users match the criteria.

        **Usage**: Searches for a unique user via the repository.
        """
        return await self.repository.get_user(dto)

    async def filter(self, dto: FindUserDTO, limit: Optional[int] = None, offset: Optional[int] = None):
        """
        **Description**: Filters users based on criteria with optional pagination.

        **Parameters**:
        - `dto`: *FindUserDTO* - Search criteria for filtering users.
        - `limit`: *Optional[int]* - Maximum number of users to return.
        - `offset`: *Optional[int]* - Starting index for pagination.

        **Returns**:
        - *List[UserDTO]*: List of matching users.

        **Usage**: Retrieves a filtered list of users from the repository.
        """
        return await self.repository.filter(dto, limit, offset)

    async def get_list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[UserDTO]:
        """
        **Description**: Retrieves a list of all users with optional pagination.

        **Parameters**:
        - `limit`: *Optional[int]* - Maximum number of users to return.
        - `offset`: *Optional[int]* - Starting index for pagination.

        **Returns**:
        - *List[UserDTO]*: List of user details.

        **Usage**: Fetches a paginated list of users from the repository.
        """
        return await self.repository.get_list(limit, offset)

    async def get(self, pk: int):
        """
        **Description**: Retrieves a user by their ID.

        **Parameters**:
        - `pk`: *int* - Unique identifier of the user.

        **Returns**:
        - *UserDTO*: Details of the user.

        **Raises**:
        - `UserNotFound`: If no user exists with the given ID.

        **Usage**: Fetches a specific user from the repository.
        """
        return await self.repository.get(pk)

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
        """
        **Description**: Updates a user’s details by their ID.

        **Parameters**:
        - `dto`: *UpdateUserDTO* - New details for the user (name and/or surname).
        - `pk`: *int* - Unique identifier of the user.

        **Returns**:
        - *UserDTO*: Updated user details.

        **Raises**:
        - `UserNotFound`: If no user exists with the given ID.

        **Usage**: Modifies a user’s details via the repository.
        """
        return await self.repository.update(dto, pk)

    async def delete(self, pk: int) -> UserDTO:
        """
        **Description**: Deletes a user by their ID.

        **Parameters**:
        - `pk`: *int* - Unique identifier of the user.

        **Returns**:
        - *UserDTO*: Details of the deleted user.

        **Raises**:
        - `UserNotFound`: If no user exists with the given ID.

        **Usage**: Removes a user from the system via the repository.
        """
        return await self.repository.delete(pk)

    async def update_password(self, dto: UpdatePasswordDTO, pk: int) -> UserDTO:
        """
        **Description**: Updates a user’s password.

        **Parameters**:
        - `dto`: *UpdatePasswordDTO* - New password data.
        - `pk`: *int* - Unique identifier of the user.

        **Returns**:
        - *UserDTO*: Updated user details (excluding password).

        **Raises**:
        - `UserNotFound`: If no user exists with the given ID.

        **Usage**: Hashes the new password and updates it via the repository.
        """
        new_password = hash_password(dto.password)
        return await self.repository.update_password(new_password, pk)