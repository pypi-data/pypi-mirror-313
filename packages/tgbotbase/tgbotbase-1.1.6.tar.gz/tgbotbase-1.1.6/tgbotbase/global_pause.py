import os
from typing import Any

from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from tgbotbase.filters import PauseFilter, Role

try:
    from src.models import User, UserRole  # type: ignore
except ImportError:
    class UserRole(Any): ...
    class User(Any): ...


from tgbotbase.utils import SHARED_OBJECTS

dp = SHARED_OBJECTS["dp"]

os.environ["GLOBAL_PAUSE"] = "false"


@dp.message(Role(UserRole.ADMIN.value), Command("pause"))
async def pause(message: Message):
    os.environ["GLOBAL_PAUSE"] = "true"
    await message.answer("Paused")


@dp.message(Role(UserRole.ADMIN.value), PauseFilter(), Command("unpause"))
async def unpause(message: Message):
    os.environ["GLOBAL_PAUSE"] = "false"
    await message.answer("Unpaused")


@dp.callback_query(PauseFilter())
@dp.message(PauseFilter())
async def paused(message: Message | CallbackQuery, user: User):
    pass
