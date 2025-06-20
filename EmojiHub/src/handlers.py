import logging

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.auth.exceptions import AuthError
from src.libs.exceptions import AlreadyExistError, NotFoundException, PaginationError, SeveralAnswersFoundException
from src.parser.exceptions import ParsingError, LoginFailedError, FabricsNotFound

from pydantic import ValidationError

logger = logging.getLogger(__name__)

def add_handlers(app: FastAPI):
    @app.exception_handler(AlreadyExistError)
    async def already_exists_handler(_, exc: AlreadyExistError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AuthError)
    async def auth_failure_handler(_, exc):
        # 401 for auth failures
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(_, exc: NotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PaginationError)
    async def pagination_error_handler(_, exc: PaginationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(SeveralAnswersFoundException)
    async def several_answers_found_exception(_, exc: SeveralAnswersFoundException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(_, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Provided data isn't valid, error {str(exc)}"},
        )

    @app.exception_handler(ParsingError)
    async def parsing_error_handler(_, exc: ParsingError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Error raised while parsing the data, error {str(exc)}"}
        )

    @app.exception_handler(LoginFailedError)
    async def login_error_handler(_, exc: LoginFailedError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Failed login to Afterbuy or some troubles with internet connection, error {str(exc)}"}
        )

    @app.exception_handler(FabricsNotFound)
    async def fabrics_not_found_error(_, exc: FabricsNotFound):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Fabric not found on afterbuy, do you sure it exists?"}
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )