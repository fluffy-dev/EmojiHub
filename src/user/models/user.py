from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.libs.base_model import Base

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
    - `is_admin`: *bool* - Indicates if the user has admin privileges (default: False).

    **Usage**: Defines the database schema for storing user data.
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(20))
    surname: Mapped[str] = mapped_column(String(20), nullable=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)