from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.libs.base_model import Base
from src.emoji.models.user_favorite_emoji import user_favorite_emoji_association_table


class Emoji(Base):
    """
    **Description**: SQLAlchemy model representing the `emojis` database table.

    **Table**: `emojis`

    **Columns**:
    - `id`: *int* - Primary key, auto-incremented identifier.
    - `name`: *str* - The common name or description of the emoji.
    - `character`: *str* - The single Unicode character for the emoji.
    - `created_by_user_id`: *int* - Foreign key linking to the user who created this emoji.

    **Relationships**:
    - `creator`: A many-to-one relationship to the `UserModel` who added the emoji.
    - `favorited_by`: A many-to-many relationship to `UserModel`, tracking which users have favorited this emoji.

    **Usage**: Defines the schema for storing emoji data.
    """
    __tablename__ = "emojis"

    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    character: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)
    created_by_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    creator: Mapped["UserModel"] = relationship(back_populates="created_emojis")
    favorited_by: Mapped[List["UserModel"]] = relationship(
        secondary=user_favorite_emoji_association_table,
        back_populates="favorite_emojis"
    )