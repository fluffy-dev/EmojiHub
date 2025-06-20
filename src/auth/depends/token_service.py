from fastapi import Depends
from typing import Annotated

from src.auth.token_service import TokenService

ITokenService = Annotated[TokenService, Depends()]
"""
**Description**: Dependency injection type hint for `TokenService`.

**Usage**: Used in `AuthService` to inject an instance of `TokenService` automatically.
"""