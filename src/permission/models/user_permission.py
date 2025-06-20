from sqlalchemy import Table, Column, Integer, ForeignKey

from src.libs.base_model import Base


user_permission_association_table = Table(
    "user_permission_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)
"""
**Description**: An association table for the many-to-many relationship between users and permissions.

**Table**: `user_permission_association`

**Columns**:
- `user_id`: *int* - Foreign key to `users.id`. Part of the composite primary key.
- `permission_id`: *int* - Foreign key to `permissions.id`. Part of the composite primary key.

**Usage**: Links users to the permissions they have been granted.
"""