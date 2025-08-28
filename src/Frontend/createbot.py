from loguru import logger
import psycopg2
import Backend.ISwork, Backend.DBwork
from src import config
from src.Backend import DBwork
from src.Backend import ISwork
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, URLInputFile, BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import DeleteMyCommands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


current_day = datetime.now().weekday()

scheduler = AsyncIOScheduler(timezone = 'Europe/Moscow')

logger.add(
    "sys.stdout",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{line} - {message}",
    colorize=True,
    level="INFO"
)

bot = Bot(token = config.TG_token , default = DefaultBotProperties(parse_mode = ParseMode.HTML))
dp = Dispatcher(storage = MemoryStorage())

schema_name = 'catbot'
table_name = 'Users'


@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('''
This is a bot that sends images of cats.

List of available commands:
/cat - request an image of a cat from today's pool of images
/subscribe - subscribe to daily cat images sent at 12:00 UTC+3
/subscription_modify <number> - change the amount of images sent daily
/unsubscribe - cancel your subscription(but why would you want to? :3)
''', parse_mode=None)
    logger.info(f'Command /start executed successfully. ChatID: {message.chat.id}')


@dp.message(Command('cat'))
async def cmd_cat(message: Message):
    chat_id = message.chat.id
    image_link = URLInputFile(ISwork.getDownloadURL(current_day), filename=datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    if image_link is None:
        await bot.send_message(chat_id=chat_id, text="We are sorry, but there seems to be a problem with finding images for today.")
    else:
        await message.answer_photo(image_link, caption='Look, a cat :3')
        logger.info(f'Command /cat executed successfully. ChatID: {chat_id}')


@dp.message(Command('subscription_modify'))
async def subscription_modify(message: Message, command: CommandObject):
    chat_id = message.chat.id
    if command.args is None or command.args.isdigit() == False:
        await message.answer('Please write the number of images you would like\n'
                             'to receive in the same message as a command.\n'
                             'Example:'
                             '/subscription_modify <number of daily images>')
        return
    try:
        cursor, connection = DBwork.set_connection()
        amount = command.args
        DBwork.change_images_amount(chat_id, amount, connection, cursor)
        DBwork.close_connection(connection, cursor)
    except psycopg2.Error:
        if psycopg2.errors.IntegrityError:
            await message.answer('You are not yet subscribed.')
            logger.warning(f'A non-subscribed user in chat {chat_id} tried to modify subscription')
        else:
            await message.answer('There seems to be a problem on our side.')
        return
    await message.answer('Amount of daily images was changed successfully!')
    logger.info(f'Command /subscription_modify executed successfully. ChatID: {chat_id}')


@dp.message(Command('subscribe'))
async def cmd_subscribe(message: Message):
    chat_id = message.chat.id
    try:
        cursor, connection = DBwork.set_connection()
        DBwork.add_user(chat_id, connection, cursor)
        DBwork.close_connection(connection, cursor)
    except psycopg2.Error as e:
        if psycopg2.errors.UniqueViolation:
            await message.answer('You are already subscribed.')
            logger.warning(f'An already subscribed user in chat {chat_id} tried to subscribe again')
        else:
            await message.answer('There seems to be a problem on our side.')
            logger.error(f'PostgreSQL error occurred. ChatID: {chat_id}. Error: {str(e.pgerror)}')
        return
    await message.answer('''
    You have successfully subscribed to daily cat photos!
    You will get 1 photo a day by default,
    use /subscription_modify to change that amount.
    ''')
    logger.info(f'Command /subscribe executed successfully. ChatID: {chat_id}')


@dp.message(Command('unsubscribe'))
async def cmd_unsubscribe(message: Message):
    chat_id = message.chat.id
    try:
        cursor, connection = DBwork.set_connection()
        DBwork.delete_user(chat_id, connection, cursor)
        DBwork.close_connection(connection, cursor)
    except psycopg2.Error as e:
        if psycopg2.errors.NoData:
            await message.answer('You are not yet subscribed.')
            logger.warning(f'A non-subscribed user in chat {chat_id} tried to unsubscribe')
        else:
            await message.answer('There seems to be a problem on our side.')
            logger.error(f'PostgreSQL error occurred. ChatID: {chat_id}. Error: {str(e.pgerror)}')
        return
    await message.answer('You have successfully unsubscribed.')
    logger.info(f'Command /unsubscribe executed successfully. ChatID: {chat_id}')


async def send_daily_images():
    cursor, connection = DBwork.set_connection()
    max_id = DBwork.get_last_id(cursor)
    for id in range(1, max_id + 1):
        chat_id = DBwork.get_chat_id(id, cursor)
        images_amount = DBwork.get_images_amount(chat_id, cursor)
        for _ in range(images_amount):
            image_link = URLInputFile(ISwork.getDownloadURL(current_day), filename=datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
            if image_link is None:
                await bot.send_message(chat_id=chat_id, text="We are sorry, but there seems to be a problem with finding images for today.")
            else:
                await bot.send_photo(chat_id = chat_id, photo = image_link)
    DBwork.close_connection(connection, cursor)
    logger.info('Daily mass sending to subscribers has finished')


async def set_commands_for_menu():
    # await bot(DeleteMyCommands(scope=BotCommandScopeDefault()))
    logger.info('Bot command list cleared')
    commands = [
        BotCommand(command='start', description='Get info about the bot and its commands'),
        BotCommand(command='cat', description='Request an image of a cat from today\'s pool of images'),
        BotCommand(command='subscribe', description='Subscribe to daily cat images sent at 12:00 UTC+3'),
        BotCommand(command='subscription_modify', description='Change the amount of images sent daily'),
        BotCommand(command='unsubscribe', description='Cancel your subscription')
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllGroupChats())
    logger.info('Command menu for bot has been set')


scheduler.add_job(send_daily_images, 'cron', hour = 12, minute = 0)


async def main():
    DBwork.schema_creator(schema_name)
    DBwork.table_creator(schema_name, table_name)
    await set_commands_for_menu()
    scheduler.start()
    await dp.start_polling(bot)