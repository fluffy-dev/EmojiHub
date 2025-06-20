from src.libs.exceptions import NotFoundException, SeveralAnswersFoundException

class UserNotFound(NotFoundException):
    """
    **Description**: Exception raised when a user is not found in the system.

    **Cause**: Triggered if no user matches the provided ID or search criteria.

    **Usage**: Used in `get`, `update`, `delete`, and `update_password` operations.
    """
    pass

class UserIsNotUnique(SeveralAnswersFoundException):
    """
    **Description**: Exception raised when multiple users match the search criteria.

    **Cause**: Occurs if the `get_user` operation returns more than one result.

    **Usage**: Thrown in the `get_user` operation to enforce uniqueness of results.
    """
    pass