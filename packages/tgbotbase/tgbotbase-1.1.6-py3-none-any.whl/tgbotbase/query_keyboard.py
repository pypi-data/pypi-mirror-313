from __future__ import annotations

import math
from typing import Any

from aiogram import Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbotbase.answer import AnswerContext
from tgbotbase.factories import MultiKeyboardFactory
from tgbotbase.keyboards import keyboard
from tgbotbase.utils import SHARED_OBJECTS, KeyboardStorage, get_sender, logger

# for local debugging
try:
    from src.models import BookType, User  # type: ignore
except ImportError:
    class User(Any): ...
    class BookType(Any): ...


# get classes, variables and functions from shared objects
dp: Dispatcher = SHARED_OBJECTS.get("dp")

if dp is None:
    logger.warning(
        "i18n is not initialized to SHARED_OBJECTS, import i18n and add as value to key 'i18n' to SHARED_OBJECTS"
    )


@dp.callback_query(MultiKeyboardFactory.filter(F.action == "page"))
async def page(
    callback: CallbackQuery,
    callback_data: MultiKeyboardFactory,
    user: User,
    cxt: AnswerContext,
):
    data: dict = KeyboardStorage.get(user.user_id, {})
    if data.get("kb_session") != callback_data.kb_session:
        await cxt.answer(user.localize("keyboard_session_error"))
        return

    max_page = math.ceil(data["query"].count() / (data["height"] * data["width"]))

    if int(callback_data.page) < 1 or int(callback_data.page) > max_page:
        await callback.answer("Такой страницы не существует")
        return

    await cxt.answer(
        text=data["default_text"],
        reply_markup=keyboard.book(
            localize=user.localize, page=int(callback_data.page), **data
        ),
    )


@dp.callback_query(MultiKeyboardFactory.filter(F.action == "select"))
async def select(
    callback: CallbackQuery,
    callback_data: MultiKeyboardFactory,
    state: FSMContext,
    user: User,
    cxt: AnswerContext,
):
    data: dict = KeyboardStorage.get(user.user_id, {})
    if data.get("kb_session") != callback_data.kb_session:
        await cxt.answer(user.localize("keyboard_session_error"))
        return
    item = int(callback_data.item_selected)

    if data["book_type"] == BookType.MANY.value:
        selected = data.get("selected", [])
        if item in selected:
            selected.remove(item)
        else:
            selected.append(item)

        KeyboardStorage[user.user_id].update(selected=selected)

        await cxt.answer(
            text=data["default_text"],
            reply_markup=keyboard.book(
                localize=user.localize, page=int(callback_data.page), **data
            ),
        )

    elif data["book_type"] == BookType.ONE.value:
        db_item = data["db"].select().where(data["db"].id == item).first()
        await cxt.redirect(data["select_handler"], item=db_item)


@dp.callback_query(MultiKeyboardFactory.filter(F.action == "send"))
async def send_selected(
    callback: CallbackQuery,
    user: User,
    callback_data: MultiKeyboardFactory,
    cxt: AnswerContext,
):
    sender = get_sender(callback)
    data: dict = KeyboardStorage.get(user.user_id, {})
    if data.get("kb_session") != callback_data.kb_session:
        await sender(user.localize("keyboard_session_error"))
        return

    selected = data.get("selected", [])
    selected = list(data["db"].select().where(data["db"].id.in_(selected)))

    await cxt.redirect(data["select_handler"], selected=selected)


@dp.callback_query(MultiKeyboardFactory.filter(F.action == "secret"))
async def secret(
    message: CallbackQuery,
    user: User,
    callback_data: MultiKeyboardFactory,
    state: FSMContext,
):
    await message.answer("🫣👽💦💦🔞")
