
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)

from config import Config


logging.basicConfig(level=logging.INFO)

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть Spendly",
                    web_app=WebAppInfo(
                        url=Config.WEBAPP_URL
                    )
                )
            ]
        ]
    )

    await message.answer(
        "Привет! 👋\n\n"
        "Добро пожаловать в Spendly — "
        "сервис управления подписками и регулярными платежами.\n\n"
        "Нажми кнопку ниже, чтобы начать.",
        reply_markup=keyboard
    )


async def main():
    if not Config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN не указан в .env")

    logging.info("Spendly Bot запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
