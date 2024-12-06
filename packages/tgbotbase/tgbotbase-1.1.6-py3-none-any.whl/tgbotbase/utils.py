"""
# Universal telegram bot base for bots maded by @abuztrade on aiogram 3.x
### Default settings:
```python
os.environ["LOG_FILENAME"]       = "./logs/bot_{time:DD-MM-YYYY}.log"
os.environ["LOG_FORMAT"]         = "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <level>{message}</level>"
os.environ["LOG_ROTATION"]       = "2days"
os.environ["LOG_COMPRESSION"]    = "zip"
os.environ["LOG_BACKTRACE_BOOL"] = "True"
os.environ["LOG_DIAGNOSE_BOOL"]  = "True"
os.environ["LOCALES_FOLDER"]     = "locales"
os.environ["LOCALES_STARTSWITH"] = "bot"
os.environ["KEYBOARDS_PATH"]     = "./src/keyboards.yml"
```

## Also should fill SHARED_OBJECTS["dp"] with your root aiogram 3.x dispatcher for keyboord.book works
```python
SHARED_OBJECTS["dp"] = dp
```
"""

import os
import random
import string
import time
from dataclasses import dataclass
from sys import stderr
from typing import Callable, Dict, Union

import i18n
import requests
import ruamel.yaml
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.methods.send_message import SendMessage
from aiogram.types import (
    CallbackQuery,
    ContentType,
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardMarkup
from dotenv import dotenv_values
from loguru import logger
from loguru._file_sink import FileSink

DOTENV = dotenv_values(".env")
for key, value in DOTENV.items():
    os.environ[key] = value

ENV = os.environ.copy()
# global objects from initial app for share to this library
SHARED_OBJECTS = {
    # should be filled after init utils module and before init others
}
# ENV VARIABLES
utils_settings = {
    "filename": "./logs/bot_{time:DD-MM-YYYY}.log",
    "log_format": "<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <level>{message}</level>",
    "rotation": "2days",
    "compression": "zip",
    "backtrace": True,
    "diagnose": True,
    "locales_folder": "./locales",
    "locales_startswith": "bot",
    "keyboards_path": "./src/keyboards.yml",
}


def smart_bool(value: str) -> bool:
    return value.lower() in ["true", "t", "1", "y", "yes"]


for key, env_key in [
    ("filename", "LOG_FILENAME"),  # os.environ["LOG_FILENAME"]       = ...
    ("log_format", "LOG_FORMAT"),  # os.environ["LOG_FORMAT"]         = ...
    ("rotation", "LOG_ROTATION"),  # os.environ["LOG_ROTATION"]       = ...
    ("compression", "LOG_COMPRESSION"),  # os.environ["LOG_COMPRESSION"]    = ...
    ("backtrace", "LOG_BACKTRACE_BOOL"),  # os.environ["LOG_BACKTRACE_BOOL"] = ...
    ("diagnose", "LOG_DIAGNOSE_BOOL"),  # os.environ["LOG_DIAGNOSE_BOOL"]  = ...
    ("locales_folder", "LOCALES_FOLDER"),  # os.environ["LOCALES_FOLDER"]     = ...
    (
        "locales_startswith",
        "LOCALES_STARTSWITH",
    ),  # os.environ["LOCALES_STARTSWITH"]         = ...
    ("keyboards_path", "KEYBOARDS_PATH"),
]:  # os.environ["KEYBOARDS_PATH"]     = ...
    if ENV.get(env_key) is not None:
        utils_settings[key] = (
            ENV[env_key] if not env_key.endswith("_BOOL") else smart_bool(ENV[env_key])
        )

yaml = ruamel.yaml.YAML()
Localize = Callable[[str], str]

logger.remove()
logger.add(stderr, format=utils_settings["log_format"])

logger.add(
    utils_settings["filename"],
    format=utils_settings["log_format"],
    rotation=utils_settings["rotation"],
    compression=utils_settings["compression"],
    backtrace=utils_settings["backtrace"],
    diagnose=utils_settings["diagnose"],
)

logger.level("DEBUG", color="<magenta>")

KeyboardStorage: Dict[int, dict] = {}


# load locales
i18n.load_path.append(utils_settings["locales_folder"])
i18n.set("encoding", "utf-8")


def localizator(key: str, locale: str = "en", **kwargs) -> str:
    return i18n.t(
        f"{utils_settings['locales_startswith']}.{key}", locale=locale, **kwargs
    )


def reload_i18n() -> None:
    i18n.translations.container.clear()

    for dir in i18n.load_path:
        i18n.resource_loader.load_directory(dir)


def set_value_i18n(locale: str, path: str, value: str):
    data = load_yaml(
        f"{utils_settings['locales_folder']}/{utils_settings['locales_startswith']}.{locale}.yml"
    )
    temp = data[locale]
    path = path.split(".")
    for key in path[:-1]:
        temp = temp[key]
    temp[path[-1]] = value

    with open(
        f"{utils_settings['locales_folder']}/{utils_settings['locales_startswith']}.{locale}.yml",
        "w",
        encoding="utf-8",
    ) as f:
        yaml.dump(data, f)


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.load(f)


def get_logger_filename() -> str:
    for _, handler in logger._core.handlers.items():
        if isinstance(handler._sink, FileSink):
            return handler._sink._file.name


async def get_msg_args(
    message: Message,
    target: int,
    error_msg: str = None,
    validator: Callable[[str], bool] = lambda len_args, args: len_args != args,
) -> tuple[bool, list[str] | None]:
    args = message.text.split()[1:]
    if validator(len(args), target):
        if error_msg:
            await message.answer(error_msg)
        return False, None
    return True, args


def get_sender(
    message: Union[Message, CallbackQuery],
) -> Union[EditMessageText, SendMessage]:
    if isinstance(message, CallbackQuery):
        return message.message.edit_text
    else:
        return message.answer


def get_message_obj(message: Union[Message, CallbackQuery]) -> Message:
    if isinstance(message, CallbackQuery):
        return message.message
    else:
        return message


def keyboard_session():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def add_session_to_keyboard(kb: dict, session: str) -> dict:
    for i in range(len(kb["buttons"])):
        if isinstance(kb["buttons"][i]["data"], str) and kb["buttons"][i][
            "data"
        ].startswith("part:"):
            kb["buttons"][i]["data"] += f":{session}"

    return kb


def get_p2p_price(cache_price=[0, 0]) -> float:
    # cache_price - cached variable
    # store cache value for a 60 seconds
    if cache_price[1] + int(os.getenv("CACHE_RUBUSD_PRICE_TIME", 60)) > time.time():
        return cache_price[0]

    try:
        resp = requests.post(
            "https://api2.bybit.com/fiat/otc/item/online",
            json={
                "userId": "",
                "tokenId": "USDT",
                "currencyId": "RUB",
                "payment": [],
                "side": "1",
                "size": "1",
                "page": "1",
                "amount": "",
                "authMaker": False,
                "canTrade": False,
            },
            headers={
                "Origin": "https://www.bybit.com",
                "Referer": "https://www.bybit.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
            timeout=5,
        ).json()
    except Exception as e:
        logger.warning(f"Failed to get p2p price: {e}")
        return 0

    price = float(resp["result"]["items"][0]["price"])
    # add to cache
    cache_price = [price, time.time()]
    return price


async def answer_message(
    text: str,
    reply_markup: InlineKeyboardMarkup = None,
    to_chat_id: int = None,
    parse_mode: str = "HTML",
    reply_to_message_id: int = None,
    edit_channel_id: int = None,
    edit_message_id: int = None,
    disable_notification: bool = None,
    media: "Media" = None,
    _message: Union[Message, CallbackQuery] = None,  # IMPORTANT
    skip_error: bool = False,
    **formats: dict,
) -> Message:
    if not _message:
        raise Exception("No message to answer")

    try:
        message = get_message_obj(_message)

        text = text.format(**formats) if formats else text
        if not to_chat_id:
            # edit text for any message
            if edit_channel_id and edit_message_id:
                if media and media.content_type != ContentType.TEXT.value:
                    return await message.bot.edit_message_caption(
                        caption=text,
                        chat_id=edit_channel_id,
                        message_id=edit_message_id,
                        parse_mode=parse_mode,
                        reply_markup=reply_markup,
                    )

                return await message.bot.edit_message_text(
                    text=text,
                    chat_id=edit_channel_id,
                    message_id=edit_message_id,
                    parse_mode=parse_mode,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup,
                )

            elif isinstance(_message, Message):
                if media and media.content_type != ContentType.TEXT.value:
                    if media.is_media_group:
                        return await message.answer_media_group(
                            media=media.to_inputmedia(text),
                            disable_notification=disable_notification,
                            reply_to_message_id=reply_to_message_id,
                        )

                    return await message.__getattribute__(
                        f"answer_{media.content_type.lower()}"
                    )(
                        **{media.content_type.lower(): media.media_list[0]},
                        caption=text,
                        parse_mode="HTML",
                        disable_notification=disable_notification,
                        reply_to_message_id=reply_to_message_id,
                        reply_markup=reply_markup,
                    )

                return await message.answer(
                    text=text,
                    parse_mode=parse_mode,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup,
                    disable_notification=disable_notification,
                )

            elif isinstance(_message, CallbackQuery):
                if media and media.content_type != ContentType.TEXT.value:
                    return await message.bot.edit_message_caption(
                        caption=text,
                        chat_id=edit_channel_id,
                        message_id=edit_message_id,
                        parse_mode=parse_mode,
                        reply_markup=reply_markup,
                    )
                return await message.edit_text(
                    text=text,
                    parse_mode=parse_mode,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup,
                )
        else:
            if media and media.content_type != ContentType.TEXT.value:
                if media.is_media_group:
                    if reply_markup is not None:
                        logger.warning(
                            "Function utils.py:answer_message() got reply_markup, but reply markup is not supported for media groups. It will be skipped."
                        )

                    return await message.bot.send_media_group(
                        to_chat_id,
                        media=media.to_inputmedia(text),
                        disable_notification=disable_notification,
                        reply_to_message_id=reply_to_message_id,
                    )

                return await message.bot.__getattribute__(
                    f"send_{media.content_type.lower()}"
                )(
                    to_chat_id,
                    **{media.content_type.lower(): media.media_list[0]},
                    caption=text,
                    parse_mode="HTML",
                    disable_notification=disable_notification,
                    reply_to_message_id=reply_to_message_id,
                    reply_markup=reply_markup,
                )

            return await message.bot.send_message(
                to_chat_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=True,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
            )

    # except MessageNotModified:
    #    pass

    except Exception as e:
        if not skip_error:
            logger.exception(e)
            logger.error(f"Received error while processing message: {text}")


FileId = str


@dataclass
class Media:
    __media_groups = {
        ContentType.PHOTO: InputMediaPhoto,
        ContentType.VIDEO: InputMediaVideo,
        ContentType.DOCUMENT: InputMediaDocument,
        ContentType.AUDIO: InputMediaAudio,
        ContentType.ANIMATION: InputMediaAnimation,
    }

    content_type: str
    media_list: list[FileId]
    html_text: str
    text: str

    @property
    def is_media_group(self):
        return len(self.media_list) > 1

    def to_inputmedia(
        self, text: str = None
    ) -> list[
        Union[
            InputMediaPhoto,
            InputMediaVideo,
            InputMediaDocument,
            InputMediaAudio,
            InputMediaAnimation,
        ]
    ]:
        return [
            self.__media_groups[self.content_type](
                media=x,
                caption=(self.html_text if text is None else text) if i == 0 else None,
                parse_mode="HTML" if i == 0 else None,
            )
            for i, x in enumerate(self.media_list)
        ]

    def to_json(self):
        return {
            "content_type": self.content_type,
            "media_list": self.media_list,
            "html_text": self.html_text,
            "text": self.text,
        }

    @staticmethod
    def from_json(**json) -> "Media":
        return Media(**json)


def str_time_to_sec(number: str) -> int:
    """
    format: "1d", "2w", "3M", "4y", "1m+5s"
    """
    return sum(
        [
            int(x[:-1])
            * (
                60
                if x[-1] == "m"
                else 3600
                if x[-1] == "h"
                else 86400
                if x[-1] == "d"
                else 604800
                if x[-1] == "w"
                else 2592000
                if x[-1] == "M"
                else 31536000
                if x[-1] == "y"
                else 1
            )
            for x in number.split("+")
        ]
    )


def get_usdtrub(fee: float = 7.5) -> float:
    """
    Get USDT/RUB price from garantex
    """
    for i in range(3):
        try:
            resp = requests.get("https://garantex.org/api/v2/trades?market=usdtrub")
            if resp.status_code == 200:
                return round(float(resp.json()[0]["price"]) * (1 + fee / 100), 2)
        except Exception as e:
            logger.warning(f"[{i+1}] Failed to get usdtrub price: {e}")
            time.sleep(0.5)
