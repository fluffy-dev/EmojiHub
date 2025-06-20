from sqlalchemy import Table, Column, Integer, ForeignKey
from src.libs.base_model import Base

user_favorite_emoji_association_table = Table(
    "user_favorite_emoji_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("emoji_id", Integer, ForeignKey("emojis.id", ondelete="CASCADE"), primary_key=True),
)
"""
**Description**: An association table for the many-to-many relationship between users and their favorite emojis.

**Table**: `user_favorite_emoji_association`

**Columns**:
- `user_id`: *int* - Foreign key to `users.id`. Part of the composite primary key.
- `emoji_id`: *int* - Foreign key to `emojis.id`. Part of the composite primary key.

**Usage**: Links users to the emojis they have marked as favorites.
"""