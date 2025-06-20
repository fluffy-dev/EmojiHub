from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query

from src.protection import PermissionChecker, AuthUser
from src.user.dto import UserDTO
from src.emoji.depends.service import IEmojiService
from src.emoji.dto import CreateEmojiDTO, EmojiDTO, FindEmojiDTO

router = APIRouter(prefix="/emojis", tags=["Emojis"])

@router.post(
    "/",
    response_model=EmojiDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(PermissionChecker({"emoji:create"}))]
)
async def create_emoji(
    dto: CreateEmojiDTO,
    service: IEmojiService,
    user: AuthUser,
):
    """
    **Description**: Creates a new emoji in the system.

    **Requires Permissions**: `emoji:create`
    """
    return await service.create_emoji(dto, user.id)


@router.get(
    "/",
    response_model=List[EmojiDTO],
    dependencies=[Depends(PermissionChecker({"emoji:read"}))]
)
async def find_emojis(
    service: IEmojiService,
    user: AuthUser,
    filters: FindEmojiDTO = Depends(),
    limit: Optional[int] = Query(100, ge=1, le=200),
    offset: Optional[int] = Query(0, ge=0),
):
    """
    **Description**: Retrieves a list of emojis based on filter criteria.

    The `is_favorite` flag in the response is specific to the authenticated user.

    **Requires Permissions**: `emoji:read`
    """
    return await service.find_emojis(filters, user.id, limit, offset)


@router.post(
    "/{emoji_id}/favorite",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(PermissionChecker({"emoji:favorite"}))]
)
async def add_to_favorites(
    emoji_id: int,
    service: IEmojiService,
    user: AuthUser,
):
    """
    **Description**: Adds an emoji to the authenticated user's favorites list.

    **Requires Permissions**: `emoji:favorite`
    """
    await service.add_user_favorite(user.id, emoji_id)


@router.delete(
    "/{emoji_id}/favorite",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(PermissionChecker({"emoji:favorite"}))]
)
async def remove_from_favorites(
    emoji_id: int,
    service: IEmojiService,
    user: AuthUser,
):
    """
    **Description**: Removes an emoji from the authenticated user's favorites list.

    **Requires Permissions**: `emoji:favorite`
    """
    await service.remove_user_favorite(user.id, emoji_id)