from pydantic import BaseModel, Field, constr
from typing import Optional

class EmojiDTO(BaseModel):
    """
    **Description**: DTO for representing an emoji in API responses.

    **Attributes**:
    - `id`: *int* - The unique identifier of the emoji.
    - `name`: *str* - The common name of the emoji.
    - `character`: *str* - The Unicode character of the emoji.
    - `created_by_user_id`: *Optional[int]* - The ID of the user who created it.
    - `is_favorite`: *bool* - A dynamic flag indicating if the emoji is a favorite for the *current* user.

    **Configuration**:
    - `from_attributes = True`: Allows creating this DTO from an ORM model instance.
    """
    id: int
    name: str
    character: str
    created_by_user_id: Optional[int]
    is_favorite: bool = False

    class Config:
        from_attributes = True


class CreateEmojiDTO(BaseModel):
    """
    **Description**: DTO for creating a new emoji.

    **Attributes**:
    - `name`: *str* - The name for the new emoji (e.g., 'grinning face').
    - `character`: *str* - The single Unicode character for the emoji (e.g., '😀').
    """
    name: constr(min_length=3, max_length=100)
    character: constr(min_length=1, max_length=10)


class FindEmojiDTO(BaseModel):
    """
    **Description**: DTO for specifying search criteria to find emojis. All fields are optional.

    **Attributes**:
    - `name`: *Optional[str]* - Criterion to search for emojis by name (case-insensitive substring match).
    - `favorites_only`: *Optional[bool]* - If True, returns only emojis favorited by the current user.
    """
    name: Optional[str] = Field(None, description="Filter by a case-insensitive part of the emoji name")
    favorites_only: Optional[bool] = Field(False, description="Set to true to only see your favorite emojis")