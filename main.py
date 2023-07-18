import logging

from aiogram import Bot, Dispatcher, executor, types

import configuration

API_TOKEN = configuration.telegram_token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет я тестовый бот проекта Headless Games!")


if __name__ == '__main__':
    executor.start_polling(dp)
