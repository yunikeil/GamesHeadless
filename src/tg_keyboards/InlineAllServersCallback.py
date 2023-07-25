import importlib
import random
import json

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if __name__ != "__main__":
    from ..extensions.DBWorkerExtension import DataBase
    from ..extensions.DockerWorkerExtension import create_docker_container
    from ..extensions.TGTimeoutCheck import Timeout
    from ..extensions.DockerWorkerExtension import *


# Обработчик нажатия на кнопку "factorio" после выбора игры, также обрабатываю свои кнопки.
def prc_allservers_menu_0():
    condition = lambda c: c.data in ["factorio_new", "factorio_new:1.1.80", "factorio_new:1.1.87"]
    async def process(callback_query: types.CallbackQuery):
        Timeout.update(callback_query.message.chat.id, callback_query.message.message_id, 5 * 60)
        process_menu = InlineKeyboardMarkup(row_width=1)
        add_btn = lambda *b: process_menu.add(*b)
        if ":" not in callback_query.data:
            msg_text = f"Выберите нужную версию игры:"
            add_btn(*[InlineKeyboardButton(
                f"factorio {version}",
                callback_data=f"factorio_new:{version}"
            ) for version in ["1.1.80", "1.1.87"]])
        else: # version selected
            version = callback_query.data.split(":")[1]
            msg_text = f"Вы выбрали версию factorio: {version}"
            add_btn(
                InlineKeyboardButton(
                    "Создать контейнер factorio",
                    callback_data=f"new_container;factorio:{version}"
                ), 
                InlineKeyboardButton( # Не уверен в надобности данной кнопки
                    "Вернуться к выбору версии",
                    callback_data="factorio_new"
                )
            )
        add_btn(InlineKeyboardButton(
            "Вернуться к выбору игры",
            callback_data="return_to_allservers"
        ))
        await callback_query.message.edit_text(
            text=msg_text,
            reply_markup=process_menu
        )
        await callback_query.answer()
    return {"filter": condition, "callback": process}


# Обработчик нажатия на кнопку "astroneer" после выбора игры
def prc_allservers_menu_1():
    condition = lambda c: c.data == "astroneer_new"
    async def process(callback_query: types.CallbackQuery):  
        ...
    return {"filter": condition, "callback": process}


# Обработчик нажатия на кнопку "Создать контейнер сервера" после выбора игры
def prc_new_container_menu():
    condition = lambda c: "new_container" in c.data
    async def process(callback_query: types.CallbackQuery):
        Timeout.remove(callback_query.message.chat.id, callback_query.message.message_id, 5*60)
        container_port = 8672 # TODO сделать нормальное выделение портов
        image_name = callback_query.data.split(";")[1]
        container_name = f"{image_name.replace(':', '-')}-{container_port}"
        container_id = create_docker_container(container_name, image_name, container_port)
        if container_id:
            msg =  f"Создан контейнер: {container_name}!\n" \
                   f"id: {container_id}\n" \
                   f"Продолжить настройку: /myservers"
            try:
                db = DataBase("GamesHeadless.db")
                await db.connect()
                container_settings = {
                    "container_name": container_name,
                    "container_id": container_id,
                    "container_port": container_port
                }
                await db.run_que(
                    "INSERT INTO CreatedServers (ContainerOwner, ContainerSettings) VALUES (?, ?)",
                    (callback_query.from_user.id, json.dumps(container_settings))
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


# Обработчик нажатия на кнопку "закрыть меню"
def prc_close_menu():
    condition = lambda c: c.data == "close_menu"
    async def process(callback_query: types.CallbackQuery):
        Timeout.remove(callback_query.message.chat.id, callback_query.message.message_id)
        await callback_query.message.delete()
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
    prc_close_menu,
    prc_return_to_allservers_menu
]



