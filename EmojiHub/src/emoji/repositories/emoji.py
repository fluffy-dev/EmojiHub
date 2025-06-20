from typing import List, Optional
from sqlalchemy import select, exists, and_
from sqlalchemy.orm import selectinload

from src.config.database.session import ISession
from src.user.models.user import UserModel
from src.user.exceptions import UserNotFound
from src.emoji.models.emoji import Emoji
from src.emoji.models.user_favorite_emoji import user_favorite_emoji_association_table
from src.emoji.dto import CreateEmojiDTO, EmojiDTO, FindEmojiDTO


class EmojiRepository:
    """
    **Description**: Repository for all database operations related to emojis.

    **Usage**: Handles creation, complex filtering, and favorite management for emojis.
    """
    Model = Emoji

    def __init__(self, session: ISession):
        self.session = session

    async def create(self, dto: CreateEmojiDTO, creator_id: int) -> EmojiDTO:
        """
        **Description**: Creates a new emoji record in the database.

        **Parameters**:
        - `dto`: *CreateEmojiDTO* - Data for the new emoji.
        - `creator_id`: *int* - The ID of the user creating the emoji.

        **Returns**:
        - *EmojiDTO*: The DTO representation of the newly created emoji.
        """
        instance = self.Model(**dto.model_dump(), created_by_user_id=creator_id)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        # For a newly created emoji, it's not a favorite by default.
        return EmojiDTO.model_validate(instance)

    async def find(
            self,
            dto: FindEmojiDTO,
            current_user_id: int,
            limit: Optional[int] = None,
            offset: Optional[int] = None
    ) -> List[EmojiDTO]:
        """
        **Description**: Finds and filters emojis with a dynamic `is_favorite` flag for the current user.

        **Parameters**:
        - `dto`: *FindEmojiDTO* - The filtering criteria.
        - `current_user_id`: *int* - The ID of the user making the request, used to determine favorites.
        - `limit`: *Optional[int]* - Pagination limit.
        - `offset`: *Optional[int]* - Pagination offset.

        **Returns**:
        - *List[EmojiDTO]*: A list of emojis matching the criteria.
        """
        # Subquery to check if an emoji is in the current user's favorites
        is_favorite_subquery = exists().where(
            and_(
                user_favorite_emoji_association_table.c.user_id == current_user_id,
                user_favorite_emoji_association_table.c.emoji_id == self.Model.id
            )
        ).label("is_favorite")

        stmt = select(self.Model, is_favorite_subquery).order_by(self.Model.id)

        if dto.name:
            stmt = stmt.where(self.Model.name.ilike(f"%{dto.name}%"))

        if dto.favorites_only:
            stmt = stmt.where(is_favorite_subquery)

        stmt = stmt.offset(offset).limit(limit)

        result = await self.session.execute(stmt)

        # The result is a list of tuples: (Emoji, is_favorite_bool)
        return [
            EmojiDTO(
                id=emoji.id,
                name=emoji.name,
                character=emoji.character,
                created_by_user_id=emoji.created_by_user_id,
                is_favorite=is_favorite
            )
            for emoji, is_favorite in result.all()
        ]

    async def add_to_favorites(self, user_id: int, emoji_id: int) -> None:
        """
        **Description**: Adds an emoji to a user's favorites list.

        **Parameters**:
        - `user_id`: *int* - The user's ID.
        - `emoji_id`: *int* - The emoji's ID.
        """
        user = await self.session.get(UserModel, user_id, options=[selectinload(UserModel.favorite_emojis)])
        if not user:
            raise UserNotFound("User not found")

        emoji = await self.session.get(self.Model, emoji_id)
        if not emoji:
            raise ValueError("Emoji not found")

        if emoji not in user.favorite_emojis:
            user.favorite_emojis.append(emoji)
            await self.session.commit()

    async def remove_from_favorites(self, user_id: int, emoji_id: int) -> None:
        """
        **Description**: Removes an emoji from a user's favorites list.

        **Parameters**:
        - `user_id`: *int* - The user's ID.
        - `emoji_id`: *int* - The emoji's ID.
        """
        user = await self.session.get(UserModel, user_id, options=[selectinload(UserModel.favorite_emojis)])
        if not user:
            raise UserNotFound("User not found")

        emoji = await self.session.get(self.Model, emoji_id)
        if not emoji:
            raise ValueError("Emoji not found")

        if emoji in user.favorite_emojis:
            user.favorite_emojis.remove(emoji)
            await self.session.commit()