from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.libs.base_model import Base
from src.permission.models.user_permission import user_permission_association_table

from src.emoji.models.emoji import Emoji
from src.emoji.models.user_favorite_emoji import user_favorite_emoji_association_table



class UserModel(Base):
    """
    **Description**: SQLAlchemy model representing the `users` database table.

    **Table**: `users`

    **Columns**:
    - `id`: *int* - Primary key, auto-incremented identifier.
    - `name`: *str* - User’s first name (max length: 20).
    - `surname`: *str* - User’s last name (max length: 20, nullable).
    - `login`: *str* - User’s login (max length: 50, unique, indexed).
    - `password`: *str* - Hashed password.

    **Relationships**:
    - `permissions`: A many-to-many relationship to `PermissionModel`, indicating the permissions this user has.

    **Usage**: Defines the database schema for storing user data.
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(20), nullable=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str]

    permissions: Mapped[List["PermissionModel"]] = relationship(
        secondary=user_permission_association_table,
        back_populates="users",
        lazy="selectin",
    )

    created_emojis: Mapped[List["Emoji"]] = relationship(back_populates="creator")
    favorite_emojis: Mapped[List["Emoji"]] = relationship(
        secondary=user_favorite_emoji_association_table,
        back_populates="favorited_by"
    )