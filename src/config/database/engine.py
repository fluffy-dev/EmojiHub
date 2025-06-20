from asyncio import current_task
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncEngine
)
from sqlalchemy import exc

from src.config.database.settings import settings


class DatabaseHelper:
    """
    **Description**: A helper class for managing asynchronous database connections using a lazy initialization pattern.

    **Key Feature (Lazy Initialization)**:
    - The SQLAlchemy engine and session factory are **not** created when an instance of this class is created.
    - They are initialized only on the first request for a database resource (e.g., when `get_engine()` or `get_session_factory()` is first called).
    - This approach is critical for compatibility with environments that use a prefork worker model (like Celery), as it prevents database connection objects from being created in a parent process and incorrectly inherited by child processes.

    **Attributes**:
    - `url`: *str* - The database connection URL.
    - `echo`: *bool* - Flag to enable SQLAlchemy's query logging.
    - `_engine`: *Optional[AsyncEngine]* - The lazily initialized SQLAlchemy engine.
    - `_session_factory`: *Optional[async_sessionmaker]* - The lazily initialized session factory.
    - `_scoped_session_factory`: *Optional[async_scoped_session]* - The lazily initialized scoped session factory.

    **Usage**: A single global instance is typically created and used throughout the application to obtain database sessions for ORM operations.
    """
    def __init__(self, url: str, echo: bool = False):
        """
        **Description**: Initializes the DatabaseHelper with connection parameters.

        **Note**: This constructor does **not** create the database engine or session factory. It only stores the configuration for subsequent lazy initialization.

        **Parameters**:
        - `url`: *str* - The database connection string.
        - `echo`: *bool* - If True, SQLAlchemy will log all generated SQL statements.
        """
        self.url = url
        self.echo = echo
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker[AsyncSession]] = None
        self._scoped_session_factory: Optional[async_scoped_session] = None

    def get_engine(self) -> AsyncEngine:
        """
        **Description**: Retrieves the shared SQLAlchemy async engine, creating it on the first call.

        **Logic**:
        - Implements the lazy initialization pattern. If the internal `_engine` attribute is `None`, it creates a new `AsyncEngine`.
        - Subsequent calls will return the existing engine instance, ensuring a single engine per application instance.

        **Returns**:
        - *AsyncEngine*: The singleton-like async engine instance for the application.
        """
        if self._engine is None:
            self._engine = create_async_engine(url=self.url, echo=self.echo)
        return self._engine

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        """
        **Description**: Retrieves the shared SQLAlchemy async session factory, creating it on the first call.

        **Logic**:
        - Lazily initializes the `async_sessionmaker` if it doesn't exist.
        - It depends on `self.get_engine()` to ensure the engine is available before creating the factory.

        **Returns**:
        - *async_sessionmaker[AsyncSession]*: The singleton-like session factory instance.
        """
        if self._session_factory is None:
            self._session_factory = async_sessionmaker(
                bind=self.get_engine(),
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        return self._session_factory

    def get_scope_session(self) -> async_scoped_session:
        """
        **Description**: Retrieves a scoped session factory, creating it on the first call.

        **Logic**:
        - Lazily initializes an `async_scoped_session` factory.
        - Sessions provided by this factory are scoped to the current asynchronous task (`asyncio.current_task`). This ensures session isolation in concurrent operations within the same process.

        **Returns**:
        - *async_scoped_session*: The scoped session factory instance.
        """
        if self._scoped_session_factory is None:
            session_factory = self.get_session_factory()
            self._scoped_session_factory = async_scoped_session(
                session_factory=session_factory,
                scopefunc=current_task
            )
        return self._scoped_session_factory

    async def dispose(self) -> None:
        """
        **Description**: Gracefully disposes of the database engine and resets the helper's internal state.

        **Actions**:
        - Calls `await self._engine.dispose()` to close all open connections in the connection pool.
        - Resets the internal `_engine`, `_session_factory`, and `_scoped_session_factory` attributes to `None`.

        **Usage**: Intended for use in specific lifecycle events, such as application shutdown or during testing, to ensure clean resource cleanup.
        """
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
            self._scoped_session_factory = None

    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        **Description**: Provides an `AsyncSession` within a managed asynchronous context.

        **Functionality**:
        - Creates a new session from the session factory.
        - Yields the session for use within an `async with` block.
        - Automatically rolls back the transaction if a `SQLAlchemyError` occurs.
        - Always closes the session in the `finally` block to prevent connection leaks.

        **Yields**:
        - *AsyncSession*: A new database session instance.

        **Raises**:
        - *SQLAlchemyError*: Re-raises any database-related errors after performing a rollback.

        **Usage**: The recommended way to handle sessions for single units of work (`async with db_helper.get_db_session() as session:`).
        """
        session_factory = self.get_session_factory()
        session: AsyncSession = session_factory()
        try:
            yield session
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        **Description**: Provides an `AsyncSession` via an async generator, suitable for dependency injection.

        **Functionality**:
        - This method mirrors the behavior of `get_db_session` but is structured as a standard async generator.
        - It safely handles the session lifecycle: creation, rollback on error, and guaranteed closure.

        **Yields**:
        - *AsyncSession*: A new database session instance.

        **Raises**:
        - *SQLAlchemyError*: Re-raises any database-related errors after performing a rollback.

        **Usage**: Primarily intended for use as a dependency in web frameworks like FastAPI (`Depends(db_helper.get_session)`).
        """
        session_factory = self.get_session_factory()
        session: AsyncSession = session_factory()
        try:
            yield session
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


db_helper = DatabaseHelper(settings.database_url, settings.db_echo_log)
"""
**Description**: A global, module-level instance of the `DatabaseHelper`.

**Configuration**:
- It is initialized with the database URL and echo settings loaded from the application's configuration (`settings`).

**Key Point**:
- Creating this instance at import time is lightweight and safe due to the lazy initialization pattern of the `DatabaseHelper` class. The actual database engine and connection pool are not created until they are first needed by the application.

**Usage**:
- This instance should be imported and used throughout the application to obtain database sessions (`from .db_helper import db_helper`).
"""