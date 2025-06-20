from typing import List, Set

from src.permission.depends.repository import IPermissionRepository
from src.permission.dto import CreatePermissionDTO, PermissionDTO
from src.permission.exceptions import PermissionDenied


class PermissionService:
    """
    **Description**: Service layer for managing permission-related business logic.

    **Attributes**:
    - `repository`: *IPermissionRepository* - Injected repository for database operations.

    **Usage**: Acts as an intermediary between the API router and the permission repository.
    """

    def __init__(self, repository: IPermissionRepository):
        self.repository = repository

    async def create_permission(self, dto: CreatePermissionDTO) -> PermissionDTO:
        """
        **Description**: Creates a new permission.

        **Parameters**:
        - `dto`: *CreatePermissionDTO* - The data for the new permission.

        **Returns**:
        - *PermissionDTO*: The newly created permission.
        """
        return await self.repository.create(dto)

    async def get_all_permissions(self) -> List[PermissionDTO]:
        """
        **Description**: Retrieves a list of all available permissions.

        **Returns**:
        - *List[PermissionDTO]*: A list of all permissions.
        """
        return await self.repository.get_all()

    async def assign_permission_to_user(self, user_id: int, permission_name: str) -> None:
        """
        **Description**: Assigns a specific permission to a user.

        **Parameters**:
        - `user_id`: *int* - The target user's ID.
        - `permission_name`: *str* - The name of the permission to assign.
        """
        await self.repository.assign_to_user(user_id, permission_name)

    async def revoke_permission_from_user(self, user_id: int, permission_name: str) -> None:
        """
        **Description**: Revokes a specific permission from a user.

        **Parameters**:
        - `user_id`: *int* - The target user's ID.
        - `permission_name`: *str* - The name of the permission to revoke.
        """
        await self.repository.revoke_from_user(user_id, permission_name)

    async def check_user_permissions(self, user_id: int, required: Set[str]) -> bool:
        """
        **Description**: Checks if a user has all of a given set of required permissions.

        **Parameters**:
        - `user_id`: *int* - The ID of the user to check.
        - `required`: *Set[str]* - A set of permission names that are required.

        **Returns**:
        - *bool*: True if the user has all required permissions, otherwise False.
        """
        if not required:  # If no permissions are required, access is granted.
            return True
        user_permissions = await self.repository.get_user_permissions(user_id)
        return required.issubset(user_permissions)