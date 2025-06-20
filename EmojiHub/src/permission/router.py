from typing import List
from fastapi import APIRouter, Depends, status, HTTPException

from src.permission.depends.service import IPermissionService
from src.permission.dto import CreatePermissionDTO, PermissionDTO, AssignPermissionDTO
from src.protection import PermissionChecker
from src.user.exceptions import UserNotFound
from src.permission.exceptions import PermissionNotFound, PermissionAlreadyExists


router = APIRouter(prefix="/permissions", tags=["Permissions"])

# Dependency for managing permissions
CanManagePermissions = Depends(PermissionChecker({"permission:create", "permission:assign", "permission:revoke"}))
CanReadPermissions = Depends(PermissionChecker({"permission:read"}))


@router.post("/", response_model=PermissionDTO, status_code=status.HTTP_201_CREATED, dependencies=[CanManagePermissions])
async def create_permission(
    dto: CreatePermissionDTO,
    permission_service: IPermissionService,
):
    """
    **Description**: Creates a new permission in the system.

    **Requires Permissions**: `permission:create`
    """
    try:
        return await permission_service.create_permission(dto)
    except PermissionAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=List[PermissionDTO], dependencies=[CanReadPermissions])
async def get_all_permissions(
    permission_service: IPermissionService,
):
    """
    **Description**: Retrieves a list of all available permissions.

    **Requires Permissions**: `permission:read`
    """
    return await permission_service.get_all_permissions()


@router.post(
    "/user/{user_id}/assign",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[CanManagePermissions],
)
async def assign_permission_to_user(
    user_id: int,
    dto: AssignPermissionDTO,
    permission_service: IPermissionService,
):
    """
    **Description**: Assigns a permission to a specific user.

    **Requires Permissions**: `permission:assign`
    """
    try:
        await permission_service.assign_permission_to_user(user_id, dto.permission_name)
    except (UserNotFound, PermissionNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/user/{user_id}/revoke",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[CanManagePermissions],
)
async def revoke_permission_from_user(
    user_id: int,
    dto: AssignPermissionDTO,
    permission_service: IPermissionService,
):
    """
    **Description**: Revokes a permission from a specific user.

    **Requires Permissions**: `permission:revoke`
    """
    try:
        await permission_service.revoke_permission_from_user(user_id, dto.permission_name)
    except (UserNotFound, PermissionNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))