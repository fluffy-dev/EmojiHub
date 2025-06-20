from fastapi import Depends
from typing import Annotated
from src.emoji.repositories.emoji import EmojiRepository

IEmojiRepository = Annotated[EmojiRepository, Depends()]