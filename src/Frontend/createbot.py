import psycopg2
import Backend.ISwork, Backend.DBwork
from src import config
from src.Backend import DBwork
from src.Backend import ISwork
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, URLInputFile
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


current_day = datetime.now().weekday()

start_router = Router()
scheduler = AsyncIOScheduler(timezone = 'Europe/Moscow')


logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token = config.TG_token , default = DefaultBotProperties(parse_mode = ParseMode.HTML))
dp = Dispatcher(storage = MemoryStorage())


@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('''
This is a bot that sends images of cats.
    
List of available commands:
/cat - request an image of a cat from today's pool of images
/subscribe - subscribe to daily cat images sent at 12:00 UTC+3
/subscription_modify <number> - change the amount of images sent daily
/unsubscribe - cancel your subscription(but why would you want to? :3)
''')


@dp.message(Command('cat'))
async def cmd_cat(message: Message):
    image_link = URLInputFile(ISwork.getDownloadURL(current_day), filename=datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    await message.answer_photo(image_link, caption='Look, a cat :3')


@dp.message(Command('subscription_modify'))
async def subscription_modify(message: Message, command: CommandObject):
    if command.args is None or command.args.isdigit() == False:
        await message.answer('Please write the number of images you would like\n'
                             'to receive in the same message as a command.\n'
                             'Example:'
                             '/subscription_modify <number of daily images>')
        return
    try:
        cursor, connection = DBwork.set_connection()
        chat_id = message.chat.id
        amount = command.args
        DBwork.change_images_amount(chat_id, amount, connection, cursor)
        DBwork.close_connection(connection, cursor)
    except psycopg2.Error:
        await message.answer('You are not yet subscribed.')
        return
    await message.answer('Amount of daily images was changed successfully!')


@dp.message(Command('subscribe'))
async def cmd_subscribe(message: Message):
    try:
        cursor, connection = DBwork.set_connection()
        chat_id = message.chat.id
        DBwork.add_user(chat_id, connection, cursor)
        DBwork.close_connection(connection, cursor)
    except psycopg2.Error as e:
        await message.answer('You are already subscribed.')
        print(e.pgerror)
        return
    await message.answer('''
    You have successfully subscribed to daily cat photos!
    You will get 1 photo a day by default,
    use /subscription_modify to change that amount.
    ''')


@dp.message(Command('unsubscribe'))
async def cmd_unsubscribe(message: Message):
    try:
        cursor, connection = DBwork.set_connection()
        chat_id = message.chat.id
        DBwork.delete_user(chat_id, connection, cursor)
        DBwork.close_connection(connection, cursor)
    except psycopg2.Error:
        await message.answer('You are not yet subscribed.')
        return
    await message.answer('You have successfully unsubscribed.')


async def send_daily_images():
    cursor, connection = DBwork.set_connection()
    max_id = DBwork.get_last_id(cursor)
    for id in range(1, max_id + 1):
        chat_id = DBwork.get_chat_id(id, cursor)
        images_amount = DBwork.get_images_amount(chat_id, cursor)
        for _ in range(images_amount):
            image_link = URLInputFile(ISwork.getDownloadURL(current_day), filename=datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
            await bot.send_photo(chat_id = chat_id, photo = image_link)
    DBwork.close_connection(connection, cursor)


scheduler.add_job(send_daily_images, 'cron', hour = 12, minute = 0)


async def main():
    scheduler.start()
    await dp.start_polling(bot)

