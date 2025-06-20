from typing import List, Optional, Set
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.config.database.session import ISession
from src.permission.models.permission import PermissionModel
from src.user.models.user import UserModel
from src.permission.dto import CreatePermissionDTO, PermissionDTO
from src.permission.exceptions import PermissionAlreadyExists, PermissionNotFound
from src.user.exceptions import UserNotFound


class PermissionRepository:
    """
    **Description**: Repository for handling all database operations related to permissions.

    **Attributes**:
    - `session`: *ISession* - The database session for executing queries.

    **Usage**: Provides an abstraction layer for CRUD and assignment operations on permissions.
    """
    Model = PermissionModel

    def __init__(self, session: ISession) -> None:
        self.session = session

    async def create(self, dto: CreatePermissionDTO) -> PermissionDTO:
        """
        **Description**: Creates a new permission in the database.

        **Parameters**:
        - `dto`: *CreatePermissionDTO* - Data for the new permission.

        **Returns**:
        - *PermissionDTO*: The created permission's data.

        **Raises**:
        - `PermissionAlreadyExists`: If a permission with the same name already exists.
        """
        instance = self.Model(**dto.model_dump())
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
        except IntegrityError:
            await self.session.rollback()
            raise PermissionAlreadyExists(f"Permission '{dto.name}' already exists.")
        return PermissionDTO.model_validate(instance)

    async def get_by_name(self, name: str) -> Optional[PermissionModel]:
        """
        **Description**: Retrieves a single permission model instance by its unique name.

        **Parameters**:
        - `name`: *str* - The name of the permission to find.

        **Returns**:
        - *Optional[PermissionModel]*: The ORM model if found, otherwise None.
        """
        stmt = select(self.Model).where(self.Model.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[PermissionDTO]:
        """
        **Description**: Retrieves a list of all permissions in the system.

        **Returns**:
        - *List[PermissionDTO]*: A list of all permissions.
        """
        stmt = select(self.Model).order_by(self.Model.name)
        result = await self.session.execute(stmt)
        return [PermissionDTO.model_validate(row) for row in result.scalars().all()]

    async def get_user_permissions(self, user_id: int) -> Set[str]:
        """
        **Description**: Retrieves all permission names for a specific user.

        **Parameters**:
        - `user_id`: *int* - The ID of the user.

        **Returns**:
        - *Set[str]*: A set of permission names the user has.
        """
        stmt = select(self.Model.name).join(self.Model.users).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        return set(result.scalars().all())

    async def assign_to_user(self, user_id: int, permission_name: str) -> None:
        """
        **Description**: Assigns a permission to a user.

        **Parameters**:
        - `user_id`: *int* - The ID of the user to assign the permission to.
        - `permission_name`: *str* - The name of the permission to assign.

        **Raises**:
        - `UserNotFound`: If the user does not exist.
        - `PermissionNotFound`: If the permission does not exist.
        """
        user = await self.session.get(UserModel, user_id, options=[selectinload(UserModel.permissions)])
        if not user:
            raise UserNotFound(f"User with ID {user_id} not found.")

        permission = await self.get_by_name(permission_name)
        if not permission:
            raise PermissionNotFound(f"Permission '{permission_name}' not found.")

        if permission not in user.permissions:
            user.permissions.append(permission)
            await self.session.commit()

    async def revoke_from_user(self, user_id: int, permission_name: str) -> None:
        """
        **Description**: Revokes a permission from a user.

        **Parameters**:
        - `user_id`: *int* - The ID of the user to revoke the permission from.
        - `permission_name`: *str* - The name of the permission to revoke.

        **Raises**:
        - `UserNotFound`: If the user does not exist.
        - `PermissionNotFound`: If the permission does not exist.
        """
        user = await self.session.get(UserModel, user_id, options=[selectinload(UserModel.permissions)])
        if not user:
            raise UserNotFound(f"User with ID {user_id} not found.")

        permission = await self.get_by_name(permission_name)
        if not permission:
            raise PermissionNotFound(f"Permission '{permission_name}' not found.")

        if permission in user.permissions:
            user.permissions.remove(permission)
            await self.session.commit()