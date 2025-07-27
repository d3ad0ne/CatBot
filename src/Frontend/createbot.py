from src import config
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler


start_router = Router()
scheduler = AsyncIOScheduler(timezone = 'Europe/Moscow')


logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token = config.TG_TOKEN , default = DefaultBotProperties(parse_mode = ParseMode.HTML))
dp = Dispatcher(storage = MemoryStorage())


@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()')


@dp.message(F.text)
async def basic_reaction(message: Message):
    if message.text != '':
        await message.answer(message.text)


async def main():
    await dp.start_polling(bot)

