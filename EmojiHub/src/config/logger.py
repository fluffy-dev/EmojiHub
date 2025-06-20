from logging.handlers import RotatingFileHandler

import logging
import sys


def setup_logging(
    log_file: str = "app.log",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    sqlalchemy_level: int = logging.DEBUG,
    uvicorn_level: int = logging.INFO,
    file_bytes_size: int = 10*1024*1024,
    backup_count: int = 10,
) -> None:
    """Configure logging for the application."""
    # Base formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # File handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=file_bytes_size,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    # Console handler with UTF-8
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    # Root logger setup
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

    # Specific loggers
    logging.getLogger("sqlalchemy.engine").setLevel(sqlalchemy_level)
    logging.getLogger("uvicorn.error").setLevel(uvicorn_level)
    logging.getLogger("uvicorn.access").setLevel(uvicorn_level)

    # Application logger
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")

