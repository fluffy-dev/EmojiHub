from typing import List, Optional

from src.emoji.depends.repository import IEmojiRepository
from src.emoji.dto import CreateEmojiDTO, EmojiDTO, FindEmojiDTO


class EmojiService:
    """
    **Description**: Service layer for managing emoji-related business logic.

    **Usage**: Acts as an intermediary between the API router and the emoji repository.
    """
    def __init__(self, repository: IEmojiRepository):
        self.repository = repository

    async def create_emoji(self, dto: CreateEmojiDTO, creator_id: int) -> EmojiDTO:
        """
        **Description**: Orchestrates the creation of a new emoji.
        """
        return await self.repository.create(dto, creator_id)

    async def find_emojis(
        self,
        dto: FindEmojiDTO,
        current_user_id: int,
        limit: Optional[int],
        offset: Optional[int]
    ) -> List[EmojiDTO]:
        """
        **Description**: Orchestrates finding and filtering emojis.
        """
        return await self.repository.find(dto, current_user_id, limit, offset)

    async def add_user_favorite(self, user_id: int, emoji_id: int) -> None:
        """
        **Description**: Orchestrates adding an emoji to a user's favorites.
        """
        await self.repository.add_to_favorites(user_id, emoji_id)

    async def remove_user_favorite(self, user_id: int, emoji_id: int) -> None:
        """
        **Description**: Orchestrates removing an emoji from a user's favorites.
        """
        await self.repository.remove_from_favorites(user_id, emoji_id)