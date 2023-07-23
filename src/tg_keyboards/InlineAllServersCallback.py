import importlib
import random

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if __name__ != "__main__":
    from ..extensions.DBWorkerExtension import DataBase
    from ..extensions.DockerWorkerExtension import create_docker_container
    from ..extensions.TGTimeoutCheck import Timeout
    from ..extensions.DockerWorkerExtension import *


# Обработчик нажатия на кнопки "factorio", "astroneers"
def prc_allservers_menu_0():
    condition = lambda c: c.data in ['factorio_new', 'astroneer_new']
    async def process(callback_query: types.CallbackQuery):        
        Timeout.update(callback_query.message.chat.id, callback_query.message.message_id, 5*60)
        game_selected = "factorio" if "factorio_new" in callback_query.data else "astroneer"
        process_menu = InlineKeyboardMarkup(row_width=1)
        process_menu.add( # TODO выбор версии после new_container!!!!!!!!
            InlineKeyboardButton("Создать контейнер сервера", callback_data=f"new_container:{game_selected}"),
            InlineKeyboardButton("Вернуться к выбору", callback_data="return_to_allservers"),
        )
        await callback_query.message.edit_text(
            f"Выбрана игра: {game_selected}", # TODO 
            reply_markup=process_menu
        )
        await callback_query.answer()
    return {"filter": condition, "callback": process}


# Обработчик нажатия на кнопку "закрыть меню"
def prc_allservers_menu_1():
    condition = lambda c: c.data == "close_menu"
    async def process(callback_query: types.CallbackQuery):
        Timeout.remove(callback_query.message.chat.id, callback_query.message.message_id)
        await callback_query.message.delete()
        await callback_query.answer()
    return {"filter": condition, "callback": process}


# Обработчик нажатия на кнопку "Создать контейнер сервера" после выбора игры
def prc_new_container_menu():
    condition = lambda c: "new_container" in c.data
    async def process(callback_query: types.CallbackQuery):
        Timeout.remove(callback_query.message.chat.id, callback_query.message.message_id, 5*60)
        game_selected = "factorio" if "factorio" in callback_query.data else "astroneer"
        import time # temp random =)
        container_id = create_docker_container(f"factorio_test_{time.time()}", "factorio:1.1.87", 8672, 8672)
        if container_id: # TODO выбор версии после new_container!!!!!!!!
            msg =  f"Создан контейнер: {game_selected}!\n" \
                   f"id: {container_id}\n" \
                   f"Продолжить настройку: /myservers"
            try:
                db = DataBase("GamesHeadless.db")
                await db.connect()
                await db.run_que(
                    "INSERT INTO CreatedServers (ContainerOwner) VALUES (?)",
                    (callback_query.from_user.id,)
                )
            except:
                pass
            finally:
                await db.close()
        else:
            msg = f"Что-то пошло не так..."
        await callback_query.message.edit_text(
            msg, reply_markup=None
        )
        await callback_query.answer()
    return {"filter": condition, "callback": process}


# Обработчик нажатия на кнопку Вернуться к выбору после выбора игры
def prc_return_to_allservers_menu():
    condition = lambda c: c.data in ["return_to_allservers"]
    async def process(callback_query: types.CallbackQuery):
        Timeout.update(callback_query.message.chat.id, callback_query.message.message_id, 5*60)
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


allservers_handlers = [
    prc_allservers_menu_0,
    prc_allservers_menu_1,
    prc_new_container_menu,
    prc_return_to_allservers_menu
]



