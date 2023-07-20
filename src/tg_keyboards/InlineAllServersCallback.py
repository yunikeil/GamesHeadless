from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..extensions.TGTimeoutCheck import Timeout
#from ..extensions import DockerWorkerExtension as dc


# Обработчик нажатия на кнопки в меню allservers
def prc_allservers_menu():
    condition = lambda c: c.data in ['factorio_new', 'astroneer_new', "close_menu"]
    async def process(callback_query: types.CallbackQuery):
        if callback_query.data == "close_menu":
            Timeout.remove(callback_query.message.chat.id, callback_query.message.message_id)
            await callback_query.message.delete()
            await callback_query.answer()
            return
        Timeout.update(callback_query.message.chat.id, callback_query.message.message_id, 10)
        game_selected = "⚙ factorio" if "factorio" in callback_query.data else "🌌 astroneer"
        return_to_allservers_menu = InlineKeyboardMarkup()
        return_to_allservers_menu.add(
            InlineKeyboardButton("Вернуться к выбору", callback_data="return_to_allservers"),
        )
        await callback_query.message.edit_text(
            f"Выбрана игра: {game_selected}", # TODO 
            reply_markup=return_to_allservers_menu
        )
        await callback_query.answer()
    return {"filter": condition, "callback": process}


# Обработчик  нажатия на кнопки после меню allservers
def prc_return_to_allservers_menu():
    condition = lambda c: c.data in ["return_to_allservers"]
    async def process(callback_query: types.CallbackQuery):
        Timeout.update(callback_query.message.chat.id, callback_query.message.message_id, 10)
        allservers_menu = InlineKeyboardMarkup(row_width=2)
        allservers_menu.add(
            InlineKeyboardButton("factorio", callback_data="factorio_new"), 
            InlineKeyboardButton("astroneer", callback_data="astroneer_new"),
            InlineKeyboardButton("закрыть меню", callback_data="close_menu"),
        )
        await callback_query.message.edit_text(
            f"Привет! Это информационное меню о всех серверах для игр.",
            reply_markup=allservers_menu
        )
        await callback_query.answer()
    return {"filter": condition, "callback": process}






