from fastapi import Depends
from typing import Annotated

from src.auth.service import AuthService

IAuthService = Annotated[AuthService, Depends()]
"""
**Description**: Dependency injection type hint for `AuthService`.

**Usage**: Used in FastAPI routes to inject an instance of `AuthService` automatically.
"""