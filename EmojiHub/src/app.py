from fastapi import FastAPI

from src.routes import router

from src.config.logger import setup_logging
from src.handlers import add_handlers
from src.middleware import init_middleware


def get_app() -> FastAPI:
    setup_logging()


    app = FastAPI()

    # Exception handlers
    add_handlers(app)

    # Logging and Monitoring
    # setup_telemetry(app)

    # #CORS and SLOWAPI
    init_middleware(app)

    app.include_router(router)

    return app