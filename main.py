import logging
import typing

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.storage import BaseStorage
from aiogram.utils import executor

from src.tg_keyboards.InlineAllServersCallback import prc_allservers_menu, prc_return_to_allservers_menu
from src.tg_keyboards.InlineMyServersCallback import prc_myservers_menu
from src.tg_commands.MainMenu import cmd_start, cmd_allservers, cmd_myservers, cmd_profile
from src.extensions.TGTimeoutCheck import Timeout
import configuration


bot = Bot(token=configuration.telegram_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)
Timeout.bot = bot # Костыль для проброски bot xD

for message_command in [
    cmd_start(),
    cmd_allservers(),
    cmd_myservers(),
    cmd_profile(),
]:
    dp.register_message_handler(
        callback=message_command["callback"],
        commands=message_command["commands"]
    )


for callback_query_handler in [
    # InlineAllServersCallback
    prc_allservers_menu(),
    prc_return_to_allservers_menu(),
    # InlineMyServersCallback
    prc_myservers_menu(),
]:
    dp.register_callback_query_handler(
        callback_query_handler["callback"],
        callback_query_handler["filter"]
    )

# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
