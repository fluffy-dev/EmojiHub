from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.libs.base_model import Base
from src.permission.models.user_permission import user_permission_association_table


class PermissionModel(Base):
    """
    **Description**: SQLAlchemy model representing the `permissions` database table.

    **Table**: `permissions`

    **Columns**:
    - `id`: *int* - Primary key, auto-incremented identifier.
    - `name`: *str* - The unique name of the permission (e.g., 'user:create', 'permission:assign').
    - `description`: *str* - A human-readable description of what the permission allows.

    **Relationships**:
    - `users`: A many-to-many relationship to `UserModel`, indicating which users have this permission.

    **Usage**: Defines the schema for storing available permissions in the system.
    """
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    users: Mapped[List["UserModel"]] = relationship(
        secondary=user_permission_association_table,
        back_populates="permissions",
    )