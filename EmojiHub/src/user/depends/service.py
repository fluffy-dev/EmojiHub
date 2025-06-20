from fastapi import Depends
from typing import Annotated

from src.user.service import UserService

IUserService = Annotated[UserService, Depends()]
"""
**Description**: Type hint for dependency injection of the UserService.

**Usage**: Provides an instance of `UserService` to dependent components (e.g., API routes).
"""