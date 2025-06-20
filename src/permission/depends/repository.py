from fastapi import Depends
from typing import Annotated
from src.permission.repositories.permission import PermissionRepository

IPermissionRepository = Annotated[PermissionRepository, Depends()]