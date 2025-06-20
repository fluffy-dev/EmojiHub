from pydantic import BaseModel, Field
from typing import Optional

class PermissionDTO(BaseModel):
    """
    **Description**: Pydantic model for representing a permission in API responses.

    **Attributes**:
    - `id`: *int* - The unique identifier of the permission.
    - `name`: *str* - The unique name of the permission (e.g., 'user:create').
    - `description`: *Optional[str]* - A human-readable description.

    **Configuration**:
    - `from_attributes = True`: Allows creating this DTO from an ORM model instance.
    """
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CreatePermissionDTO(BaseModel):
    """
    **Description**: DTO for creating a new permission.

    **Attributes**:
    - `name`: *str* - The unique name for the new permission. Must not already exist.
    - `description`: *Optional[str]* - An optional description for the permission.
    """
    name: str = Field(..., description="Unique name for the permission, e.g., 'user:read'")
    description: Optional[str] = Field(None, description="A description of what this permission allows")


class AssignPermissionDTO(BaseModel):
    """
    **Description**: DTO for assigning a permission to a user.

    **Attributes**:
    - `permission_name`: *str* - The name of the permission to assign.
    """
    permission_name: str