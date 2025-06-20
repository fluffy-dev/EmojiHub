from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError, MultipleResultsFound

from src.libs.exceptions import AlreadyExistError
from src.user.entity import UserEntity
from src.config.database.session import ISession
from src.user.exceptions import UserNotFound, UserIsNotUnique
from src.user.models.user import UserModel
from src.user.dto import UpdateUserDTO, UserDTO, FindUserDTO

class UserRepository:
    """
    **Description**: Repository class for handling database operations related to users.

    **Attributes**:
    - `Model`: *UserModel* - SQLAlchemy model for the users table.
    - `session`: *ISession* - SQLAlchemy session for database interactions.

    **Methods**:
    - `create`: Creates a new user in the database.
    - `get_user`: Finds a single user by criteria.
    - `filter`: Filters users by criteria with pagination.
    - `get_list`: Retrieves a list of users with pagination.
    - `get`: Retrieves a user by ID.
    - `update`: Updates a user’s details.
    - `delete`: Deletes a user by ID.
    - `update_password`: Updates a user’s password.
    - `_get_dto`: Converts a database row to a UserDTO (static helper).

    **Usage**: Provides CRUD functionality for user data in the database.
    """
    Model = UserModel

    def __init__(self, session: ISession) -> None:
        """
        **Description**: Initializes the UserRepository with a database session.

        **Parameters**:
        - `session`: *ISession* - SQLAlchemy session for database operations.
        """
        self.session: ISession = session

    async def create(self, user: UserEntity) -> UserDTO:
        """
        **Description**: Creates a new user in the database.

        **Parameters**:
        - `user`: *UserEntity* - Data for the new user.

        **Returns**:
        - *UserDTO*: Details of the created user.

        **Raises**:
        - `AlreadyExistError`: If the login is already in use.

        **Usage**: Persists a new user and returns its DTO representation.
        """
        instance = self.Model(**user.__dict__)
        self.session.add(instance)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistError(f'{instance.login} is already exist')
        await self.session.refresh(instance)
        return self._get_dto(instance)

    async def get_user(self, dto: FindUserDTO) -> Optional[UserDTO]:
        """
        **Description**: Finds a single user based on specified criteria.

        **Parameters**:
        - `dto`: *FindUserDTO* - Search criteria for the user.

        **Returns**:
        - *Optional[UserDTO]*: User details if found, otherwise None.

        **Raises**:
        - `UserIsNotUnique`: If multiple users match the criteria.

        **Usage**: Locates a unique user in the database.
        """
        stmt = select(self.Model).filter_by(**dto.model_dump(exclude_none=True))
        raw = await self.session.execute(stmt)
        try:
            instance = raw.scalar_one_or_none()
        except MultipleResultsFound:
            raise UserIsNotUnique("By this criteria found several users, try filter endpoint")
        return self._get_dto(instance) if instance is not None else None

    async def filter(self, dto: FindUserDTO, limit: Optional[int] = None, offset: Optional[int] = None) -> List[UserDTO]:
        """
        **Description**: Filters users based on criteria with optional pagination.

        **Parameters**:
        - `dto`: *FindUserDTO* - Search criteria for filtering users.
        - `limit`: *Optional[int]* - Maximum number of users to return.
        - `offset`: *Optional[int]* - Starting index for pagination.

        **Returns**:
        - *List[UserDTO]*: List of matching users.

        **Usage**: Retrieves a filtered list of users from the database.
        """
        stmt = select(self.Model).filter_by(**dto.model_dump(exclude_none=True)).offset(offset).limit(limit)
        raw = await self.session.execute(stmt)
        instances = raw.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def get_list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[UserDTO]:
        """
        **Description**: Retrieves a list of all users with optional pagination.

        **Parameters**:
        - `limit`: *Optional[int]* - Maximum number of users to return.
        - `offset`: *Optional[int]* - Starting index for pagination.

        **Returns**:
        - *List[UserDTO]*: List of user details.

        **Usage**: Fetches a paginated list of users from the database.
        """
        stmt = select(self.Model).offset(offset).limit(limit)
        raw = await self.session.execute(stmt)
        instances = raw.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def get(self, pk: int) -> Optional[UserDTO]:
        """
        **Description**: Retrieves a user by their ID.

        **Parameters**:
        - `pk`: *int* - Unique identifier of the user.

        **Returns**:
        - *Optional[UserDTO]*: User details if found, otherwise None.

        **Raises**:
        - `UserNotFound`: If no user exists with the given ID.

        **Usage**: Fetches a specific user from the database.
        """
        stmt = select(self.Model).filter_by(id=pk)
        raw = await self.session.execute(stmt)
        instance = raw.scalar_one_or_none()
        if instance is None:
            raise UserNotFound(f'User with id: {pk} not found')
        return self._get_dto(instance) if instance is not None else None

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

        **Usage**: Modifies a user’s details in the database.
        """
        stmt = (
            update(self.Model)
            .values(**dto.model_dump(exclude_none=True))
            .filter_by(id=pk)
            .returning(self.Model)
        )
        raw = await self.session.execute(stmt)
        instance = raw.scalar_one_or_none()
        await self.session.commit()
        if instance is None:
            raise UserNotFound(f"User with id: {pk} not found")
        return self._get_dto(instance)

    async def delete(self, pk: int) -> None:
        """
        **Description**: Deletes a user by their ID.

        **Parameters**:
        - `pk`: *int* - Unique identifier of the user.

        **Returns**:
        - None

        **Raises**:
        - `UserNotFound`: If no user exists with the given ID (checked in service layer).

        **Usage**: Removes a user from the database.
        """
        stmt = delete(self.Model).where(self.Model.id == pk)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_password(self, new_password: str, pk: int) -> UserDTO:
        """
        **Description**: Updates a user’s password by their ID.

        **Parameters**:
        - `new_password`: *str* - New hashed password.
        - `pk`: *int* - Unique identifier of the user.

        **Returns**:
        - *UserDTO*: Updated user details.

        **Raises**:
        - `UserNotFound`: If no user exists with the given ID.

        **Usage**: Updates the password field for a user in the database.
        """
        stmt = (
            update(self.Model)
            .values(password=new_password)
            .filter_by(id=pk)
            .returning(self.Model)
        )
        raw = await self.session.execute(stmt)
        instance = raw.scalar_one_or_none()
        await self.session.commit()
        if instance is None:
            raise UserNotFound(f"User with id: {pk} not found")
        return self._get_dto(instance)

    @staticmethod
    def _get_dto(instance: UserModel) -> UserDTO:
        """
        **Description**: Converts a database row to a UserDTO.

        **Parameters**:
        - `instance`: *UserModel* - Database row representing a user.

        **Returns**:
        - *UserDTO*: Serialized user data.

        **Usage**: Helper method to transform database records into DTOs for API responses.
        """
        return UserDTO(
            id=instance.id,
            name=instance.name,
            surname=instance.surname,
            login=instance.login,
            password=instance.password,
            is_admin=instance.is_admin
        )