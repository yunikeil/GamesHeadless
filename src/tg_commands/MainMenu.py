from typing import Final

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..extensions.TGTimeoutCheck import Timeout

"""
# Inline-клавиатура для примера
example_keyboard = InlineKeyboardMarkup(row_width=2)
example_keyboard.add(
    InlineKeyboardButton("example1", callback_data="example1"),
    InlineKeyboardButton("example2", callback_data="example2"),
)
"""


# Обработчик команды /start + а-ля замыкание
def cmd_start():
    names = ['start', 'help']
    async def command(message: types.Message):
        await message.reply(
            "Привет! Это бот проекта Games Headless. Тут должно быть" \
            " краткое описание, но оно будет готово позднее...",
            reply_markup=None
        )
    return {"commands": names, "callback": command}


# Обработчик команды /allservers + а-ля замыкание
def cmd_allservers():
    names = ['allservers']
    async def command(message: types.Message):
        allservers_menu = InlineKeyboardMarkup(row_width=2)
        allservers_menu.add(
            InlineKeyboardButton("factorio", callback_data="factorio_new"), 
            InlineKeyboardButton("astroneer", callback_data="astroneer_new"),
            InlineKeyboardButton("закрыть меню", callback_data="close_menu"),
        )
        message = await message.reply(
            "Привет! Это информационное меню о всех серверах для игр.",
            reply_markup=allservers_menu
        )
        Timeout(message.chat.id, message.message_id, 10)
    return {"commands": names, "callback": command}


# Обработчик команды /myservers + а-ля замыкание
def cmd_myservers():
    names = ['myservers']
    async def command(message: types.Message):
        ...
        # TODO работа с бд (чтение конфигов, составление клавы)
        myservers_menu = InlineKeyboardMarkup()
        myservers_menu.add( 
            InlineKeyboardButton("⚙ Test123Save ", callback_data="factorio_my:123"),
            InlineKeyboardButton("⚙ Test321Save", callback_data="factorio_my:312"),
        )
        await message.reply(
            "Привет! Это информационное меню о купленных серверах.",
            reply_markup=myservers_menu
        )
    return {"commands": names, "callback": command}


# Обработчик команды /profile + а-ля замыкание
def cmd_profile():
    names = ['profile']
    async def command(message: types.Message):
        ...
        await message.reply(
            "Привет! Это информационное меню о профиле.",
            reply_markup=None
        )
    return {"commands": names, "callback": command}


