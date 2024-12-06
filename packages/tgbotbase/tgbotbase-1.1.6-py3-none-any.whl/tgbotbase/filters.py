import os
from typing import Any

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

try:
    from src.models import User, UserRole  # type: ignore
except ImportError:
    class UserRole(Any): ...
    class User(Any): ...


class Role(Filter):
    def __init__(self, role: UserRole):
        self.role = role

    async def __call__(self, message: Message | CallbackQuery) -> bool:
        user: User | None = (
            User.select().where(User.user_id == message.from_user.id).first()
        )
        if user and user.role >= self.role:
            return True
        return False


class ChatType(Filter):
    def __init__(self, *type: str, exclude: list[str] = []):
        self.types = type
        self.exclude = exclude

    async def __call__(self, message: Message | CallbackQuery) -> bool:
        return (
            message.chat.type in self.types and message.chat.type not in self.exclude
            if isinstance(message, Message)
            else message.message.chat.type in self.types
            and message.message.chat.type not in self.exclude
        )


class PauseFilter(Filter):
    def __init__(self):
        pass

    async def __call__(self, message) -> bool:
        if os.environ["GLOBAL_PAUSE"] == "true":
            return True

        return False
