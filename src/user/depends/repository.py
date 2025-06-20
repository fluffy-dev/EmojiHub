from fastapi import Depends
from typing import Annotated

from src.user.repositories.user import UserRepository

IUserRepository = Annotated[UserRepository, Depends()]
"""
**Description**: Type hint for dependency injection of the UserRepository.

**Usage**: Provides an instance of `UserRepository` to dependent components (e.g., UserService).
"""