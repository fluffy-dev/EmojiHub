from src.libs.base_model import Base

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

class Emoji(Base):
    """
    Represents an emoji in the database.

    Attributes:
        id: The unique identifier for the emoji.
        name: The name or description of the emoji.
        character: The actual emoji character.
        is_favorite: A flag indicating if the emoji is a favorite.
    """
    __tablename__ = "emojis"

    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    character: Mapped[str] = mapped_column(String(1), unique=True, index=True)
    is_favorite: Mapped[bool] = mapped_column(default=False)