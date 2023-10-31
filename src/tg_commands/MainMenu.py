import inspect
import json
from typing import Final

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if __name__ != "__main__":
    from ..extensions.DBWorkerExtension import DataBase
    from ..extensions.TGTimeoutCheck import Timeout
else:
    pass


# Обработчик команды /start + а-ля замыкание
def cmd_start():
    names = ['start', 'help']
    async def command(message: types.Message):
        try:
            db = DataBase("GamesHeadless.db")
            await db.connect()
            user_profile = await db.get_one(
                "SELECT * FROM UserProfiles WHERE ProfileID=?",
                (message.from_id,)
            )
            if not user_profile:
                await db.run_que(
                    "INSERT INTO UserProfiles (ProfileID, BankAccount) VALUES (?, ?)",
                    (message.from_id, 0.0)
                )
        except:
            pass
        finally:
            await db.close()
        await message.reply(
            "Привет! Это бот проекта Games Headless.\n"
            "Вы можете создать свой сервер через /allservers\n"
            "Тут должно быть краткое описание, но оно будет готово позднее...",
            reply_markup=None
        )
    return {"commands": names, "callback": command}


# Обработчик команды /allservers + а-ля замыкание
def cmd_allservers():
    names = ['allservers']
    async def command(message: types.Message):
        Timeout(message.chat.id, message.message_id, 5*60)
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
    return {"commands": names, "callback": command}


# Обработчик команды /myservers + а-ля замыкание
def cmd_myservers(): # TODO а-ля чёт тут пусто чекние /allservers
    names = ['myservers']
    async def command(message: types.Message):
        try:
            db = DataBase("GamesHeadless.db")
            await db.connect()
            servers = [json.loads(server[0]) for server in await db.get_all(
                "SELECT ContainerSettings FROM CreatedServers WHERE ContainerOwner=?",
                (message.from_id,)
            )]
            await db.close()
        except:
            await message.reply("Что-то пошло не так...")
            await db.close()
            return
        myservers_menu = InlineKeyboardMarkup()
        myservers_menu.add(*[InlineKeyboardButton(
            text=server['container_name'],
            callback_data=f"container_info;{server['container_name']}"
        ) for server in servers])
        myservers_menu.add( 
            InlineKeyboardButton("закрыть меню", callback_data="close_menu"),
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
        try:
            db = DataBase("GamesHeadless.db")
            await db.connect()
            ...
        except:
            pass
        finally:
            await db.close()
        await message.reply(
            "Привет! Это информационное меню о профиле.",
            reply_markup=None
        )
    return {"commands": names, "callback": command}


menu_commands = [cmd_start, cmd_allservers, cmd_myservers, cmd_profile]

