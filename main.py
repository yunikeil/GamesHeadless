import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from src.tg_keyboards.Inline import start_menu, servers_menu, profile_menu
from src.tg_commands.MainMenu import cmd_start, cmd_servers, cmd_profile
import configuration


bot = Bot(token=configuration.telegram_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)

for message_command in [
    cmd_start(),
    cmd_servers(),
    cmd_profile(),
]:
    dp.register_message_handler(
        callback=message_command[1],
        commands=message_command[0]
    )


# Обработчик нажатия на кнопки в старт
@dp.callback_query_handler(lambda c: c.data in ['servers', 'profile', 'back_to_start'])
async def process_callback_button(callback_query: types.CallbackQuery):
    # Отправляем ответное сообщение согласно нажатой кнопке
    if callback_query.data == 'servers':
        await callback_query.message.edit_text("Выберите сервер:", reply_markup=servers_menu)
    elif callback_query.data == 'profile':
        await callback_query.message.edit_text("Выберите пункт меню профиля:", reply_markup=profile_menu)
    elif callback_query.data == 'back_to_start':
        await callback_query.message.edit_text("Вернулись в стартовое меню.", reply_markup=start_menu)

    # Отмечаем обработанным callback
    await callback_query.answer()


# Обработчик нажатия на кнопки в меню серверов
@dp.callback_query_handler(lambda c: c.data in ['server_1', 'server_2'])
async def process_servers_menu(callback_query: types.CallbackQuery):
    # Отправляем ответное сообщение согласно выбранному серверу
    server_name = "Сервер 1" if callback_query.data == 'server_1' else "Сервер 2"
    await callback_query.message.edit_text(f"Выбран сервер: {server_name}", reply_markup=start_menu)

    # Отмечаем обработанным callback
    await callback_query.answer()


# Обработчик нажатия на кнопки в меню профиля
@dp.callback_query_handler(lambda c: c.data in ['my_profile', 'settings'])
async def process_profile_menu(callback_query: types.CallbackQuery):
    # Отправляем ответное сообщение согласно выбранному пункту профиля
    menu_item = "Мой профиль" if callback_query.data == 'my_profile' else "Настройки"
    await callback_query.message.edit_text(f"Выбран пункт меню профиля: {menu_item}", reply_markup=start_menu)

    # Отмечаем обработанным callback
    await callback_query.answer()


# Запуск бота
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
