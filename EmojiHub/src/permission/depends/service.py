from fastapi import Depends
from typing import Annotated
from src.permission.service import PermissionService

IPermissionService = Annotated[PermissionService, Depends()]