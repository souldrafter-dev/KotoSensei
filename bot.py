import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
# Опять что то новое 
from aiogram.client.session.aiohttp import AiohttpSession

# Сюда вставляется токен, полученный от @BotFather
BOT_TOKEN = ""

# Включаем логирование, чтобы в консоли было видно, если что то пойдет не так
logging.basicConfig(level=logging.INFO)




# Инициализируем обьект бота и главный диспетчер (маршрутизатор команд)
session = AiohttpSession(proxy="http://192.168.0.17:10809")
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

# Хэндлер (обработчик) на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Этот код сработает, когда пользователь нажмёт кнопку Старт.abs
    await message.answer(
        "こんにちは！(Konnichiwa!) Привет! 🌸\n"
        "Я твой локальный ментор Кото-сенсей. Готов учить японский язык?\n"
        "Напиши мне что-нибудь, и мы начнем!"
    )

# Хэндлер на любые текстовые сообщения (Эхо-режим для теста)
@dp.message()
async def echo_message(message: types.Message):
    """Этот код перехватывает любой текст и отправляет его обратно."""
    # await означает, что программа отдает команду серверу ТГ и не ждет ответа, 
    # а переключается на другие задачи, чтобы бот не зависал!
    await message.answer(f"Ты написал: {message.text}")

# Главная точка входа в асинхронную программу
async def main():
    print("[Успех] Telegram-бот KotoSensei запущен в режиме ожидания сообщений...")
    # Запускаем polling (бесконечный опрос серверов Telegram на наличие новых сообщений)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запускаем асинхронный цикл событий (Event Loop)
    asyncio.run(main())