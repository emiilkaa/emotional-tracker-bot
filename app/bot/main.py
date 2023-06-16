import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text

from app.bot.keyboards import get_subscribe_menu, get_main_menu
from app.repository.user_repository import get_user_by_telegram_id, save_user

bot = Bot(token=os.environ['EMOTIONS_TG_TOKEN'], parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    user_row = get_user_by_telegram_id(str(message.from_user.id))
    if user_row is None:
        start_message = 'Привет! Я твой личный помощник для отслеживания настроения. Я могу помочь тебе делать записи ' \
                        'о твоём настроении, оценивать, как ты проводишь дни, оставлять заметки. Для ' \
                        'начала ответь, хотел ли бы ты получать напоминания о необходимости оставить запись о ' \
                        'проведённом дне?'
        await message.answer(start_message, reply_markup=get_subscribe_menu())
    else:
        start_message = 'Привет! Я твой личный помощник для отслеживания настроения. Я могу помочь тебе делать записи ' \
                        'о твоём настроении, оценивать, как ты проводишь дни, оставлять заметки.'
        await message.answer(start_message, reply_markup=get_main_menu())

@dp.callback_query_handler(Text(startswith='subscribe_'))
async def subscribe(call: types.CallbackQuery):
    subscribe_choice = call.data[10:]
    if subscribe_choice == 'true':
        save_user(str(call.from_user.id), call.from_user.first_name, call.from_user.last_name, call.from_user.username, True)
    else:
        save_user(str(call.from_user.id), call.from_user.first_name, call.from_user.last_name, call.from_user.username, False)
    start_message = 'Отлично! Теперь ты можешь пользоваться ботом 😌'
    await call.message.answer(start_message, reply_markup=get_main_menu())


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
