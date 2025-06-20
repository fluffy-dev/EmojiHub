from typing import Optional, Annotated, List, Set
from fastapi import Depends, HTTPException, Header, status

from src.auth.dto import AccessTokenDTO
from src.user.dto import UserDTO
from src.auth.depends.service import IAuthService
from src.permission.depends.service import IPermissionService
from src.permission.exceptions import PermissionDenied


async def authenticated_user(
    auth_service: IAuthService, access_token: Optional[str] = Header(default=None)
) -> UserDTO:
    """
    **Description**: A FastAPI dependency that authenticates a user via an access token.

    **Parameters**:
    - `auth_service`: *IAuthService* - Injected authentication service.
    - `access_token`: *Optional[str]* - The 'access-token' from the request header.

    **Returns**:
    - *UserDTO*: The authenticated user's data.

    **Raises**:
    - `HTTPException(401)`: If the access token is missing, invalid, or expired.
    """
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token missing")

    try:
        return await auth_service.get_current_user(AccessTokenDTO(access_token=access_token))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

AuthUser = Annotated[UserDTO, Depends(authenticated_user)]


class PermissionChecker:
    """
    **Description**: A class-based dependency for checking user permissions.

    **Functionality**:
    - It's initialized with a set of required permission names.
    - When used as a dependency, its `__call__` method is executed. It verifies that the authenticated user possesses ALL of the required permissions.

    **Usage**:
    `Depends(PermissionChecker({"user:read", "user:update"}))`
    """
    def __init__(self, required_permissions: Set[str]):
        """
        **Description**: Initializes the checker with a set of required permissions.

        **Parameters**:
        - `required_permissions`: *Set[str]* - A set of permission names required for the endpoint.
        """
        self.required_permissions = required_permissions

    async def __call__(
        self,
        user: AuthUser,
        permission_service: IPermissionService,
    ) -> UserDTO:
        """
        **Description**: The dependency logic that runs for each request.

        **Parameters**:
        - `user`: *AuthUser* - The currently authenticated user, provided by the `AuthUser` dependency.
        - `permission_service`: *IPermissionService* - Injected permission service to perform the check.

        **Returns**:
        - *UserDTO*: The user object if the permission check is successful.

        **Raises**:
        - `HTTPException(403)`: If the user lacks any of the required permissions.
        """
        if not await permission_service.check_user_permissions(user.id, self.required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Requires: {', '.join(self.required_permissions)}",
            )
        return user