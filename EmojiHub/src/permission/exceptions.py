from src.libs.exceptions import AlreadyExistError, NotFoundException

class PermissionNotFound(NotFoundException):
    """
    **Description**: Raised when a requested permission is not found in the database.
    """
    pass

class PermissionAlreadyExists(AlreadyExistError):
    """
    **Description**: Raised when attempting to create a permission that already exists.
    """
    pass

class PermissionDenied(Exception):
    """
    **Description**: Raised when a user lacks the required permissions for an action.
    """
    pass