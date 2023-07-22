import logging
import typing

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.storage import BaseStorage
from aiogram.utils import executor

from src.tg_keyboards.InlineAllServersCallback import allservers_handlers
from src.tg_keyboards.InlineMyServersCallback import myservers_handlers
from src.tg_commands.MainMenu import menu_commands
from src.extensions.TGTimeoutCheck import Timeout
import configuration


bot = Bot(token=configuration.telegram_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)
Timeout.bot = bot # Костыль для проброски bot xD

message_commands = menu_commands
for message_command in message_commands:
    message_command = message_command()
    dp.register_message_handler(
        callback=message_command["callback"],
        commands=message_command["commands"]
    )

callback_query_handlers = allservers_handlers \
    + myservers_handlers 
for callback_query_handler in callback_query_handlers:
    dp.register_callback_query_handler(
        callback_query_handler["callback"],
        callback_query_handler["filter"]
    )

# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
