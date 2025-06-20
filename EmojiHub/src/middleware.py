from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from src.config.cors import settings as cors_settings

def init_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_settings.allow_origins,
        allow_credentials=cors_settings.allow_credentials,
        allow_methods=cors_settings.allow_methods,
        allow_headers=cors_settings.allow_headers,
        allow_origin_regex=cors_settings.allow_origin_regex,
        max_age=cors_settings.max_age,
    )

def init_rate_limit(app: FastAPI):
    limiter = Limiter(key_func=get_remote_address, default_limits=["5/second"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(SlowAPIMiddleware)


def init_middleware(app: FastAPI):
    init_cors(app)
    init_rate_limit(app)
