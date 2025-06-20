from fastapi import Depends
from typing import Annotated
from src.emoji.service import EmojiService

IEmojiService = Annotated[EmojiService, Depends()]