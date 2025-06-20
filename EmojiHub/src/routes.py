from fastapi import APIRouter

# from src.user.router import router as user_router
from src.auth.router import router as auth_router
from src.permission.router import router as permission_router
from src.emoji.router import router as emoji_router

router = APIRouter(prefix="/v1", tags=["API"])

# router.include_router(user_router)
router.include_router(auth_router)
router.include_router(emoji_router)
router.include_router(permission_router)

router.include_router(export_router)