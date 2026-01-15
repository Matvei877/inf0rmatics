import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand, Message
from aiohttp import web  # Добавляем веб-сервер

# --- ВАШ ТОКЕН ---
TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Настройка команд ---
async def setup_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Перезапустить"),
        BotCommand(command="olimpiads", description="Олимпиады"),
        BotCommand(command="oge", description="ОГЭ"),
        BotCommand(command="ege", description="ЕГЭ"),
        BotCommand(command="python", description="Python"),
    ]
    await bot.set_my_commands(commands)

# --- Обработчики ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Привет! Я бот-навигатор. Меню слева или команды:\n\n"
        "/olimpiads — Олимпиады\n"
        "/oge — ОГЭ\n"
        "/ege — ЕГЭ\n"
        "/python — Python"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(Command("olimpiads"))
async def cmd_olimpiads(message: Message):
    await message.answer("Канал про Олимпиады: https://t.me/olimpiads1")

@dp.message(Command("oge"))
async def cmd_oge(message: Message):
    await message.answer("Канал ОГЭ: https://t.me/OGE9class9")

@dp.message(Command("ege"))
async def cmd_ege(message: Message):
    await message.answer("Канал ЕГЭ: https://t.me/EGE11class11")

@dp.message(Command("python"))
async def cmd_python(message: Message):
    await message.answer("Канал по Python: https://t.me/Pythonabcd")

# --- ФЕЙКОВЫЙ ВЕБ-СЕРВЕР ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Бот работает! I am alive!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    # Render выдает порт через переменную окружения PORT, иначе берем 8080
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- ГЛАВНАЯ ФУНКЦИЯ ---
async def main():
    print("Запуск веб-сервера и бота...")
    
    # Запускаем веб-сервер параллельно с ботом
    await start_web_server()
    
    await setup_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")