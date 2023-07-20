from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Обработчик выбора личного сервера
def prc_myservers_menu():
    condition = lambda c: c.data.split(":")[0] == "factorio_my"
    async def process(callback_query: types.CallbackQuery):
        if callback_query.data.split(":")[1] == "123":
            factorio_server = 1
        else:
            factorio_server = 2 
        await callback_query.message.edit_text(
            f"Выбран сервер: {factorio_server}",
            reply_markup=None
        )
        await callback_query.answer()
    return {"filter": condition, "callback": process}
