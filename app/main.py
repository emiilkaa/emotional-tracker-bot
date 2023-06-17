import datetime
import emoji
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputMediaPhoto, InputMediaVideo

from repository.media_repository import save_media_url, get_media_by_user_id_and_date
from repository.notes_repository import save_note, get_notes_by_user_id_and_date
from bot.keyboards import get_subscribe_menu, get_main_menu, get_change_day_menu, get_marks, get_settings_menu
from repository.emotions_repository import find_emotions_by_user_id_and_date, save_emotions
from repository.marks_repository import find_mark_by_user_id_and_date, save_mark
from repository.user_repository import get_user_by_telegram_id, save_user

bot = Bot(token=os.environ['EMOTIONS_TG_TOKEN'], parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    emojis = State()
    get_date = State()
    note_date = State()
    note = State()
    media_date = State()
    media = State()


processing_date = dict()
processing_note_date = dict()
processing_media_date = dict()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    user_row = get_user_by_telegram_id(str(message.from_user.id))
    if user_row is None:
        start_message = 'Привет! Я Ваш личный помощник для отслеживания настроения. Я могу помочь Вам делать записи ' \
                        'о своём настроении, оценивать, как Вы проводите дни, оставлять заметки. Для ' \
                        'начала ответьте, хотели ли бы Вы получать напоминания о необходимости оставить запись о ' \
                        'проведённом дне?'
        await message.answer(start_message, reply_markup=get_subscribe_menu())
    else:
        start_message = 'Привет! Я Ваш личный помощник для отслеживания настроения. Я могу помочь Вам делать записи ' \
                        'о своём настроении, оценивать, как Вы проводите дни, оставлять заметки.'
        await message.answer(start_message, reply_markup=get_main_menu())


@dp.message_handler(state='*', commands='cancel')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите функцию:', reply_markup=get_main_menu())


@dp.callback_query_handler(Text(startswith='subscribe_'))
async def subscribe(call: types.CallbackQuery):
    subscribe_choice = call.data[10:]
    if subscribe_choice == 'true':
        save_user(str(call.from_user.id), call.from_user.first_name, call.from_user.last_name, call.from_user.username,
                  True)
    else:
        save_user(str(call.from_user.id), call.from_user.first_name, call.from_user.last_name, call.from_user.username,
                  False)
    start_message = 'Отлично, настройки сохранены! Можно пользоваться ботом 😌'
    await call.message.answer(start_message, reply_markup=get_main_menu())


async def evaluate(message: types.Message, date: datetime.date):
    mark = find_mark_by_user_id_and_date(str(message.from_user.id), date)
    if mark is not None:
        emotions = find_emotions_by_user_id_and_date(str(message.from_user.id), date)
        if emotions is not None:
            msg = f'Вы уже оценивали этот день.\n\nОценка за {date.strftime("%d.%m.%Y")}: {mark.mark}\n' \
                  f'Эмоции за {date.strftime("%d.%m.%Y")}: {emotions.get_emojis()}'
            await message.reply(msg, reply_markup=get_change_day_menu(date))
        else:
            msg = f'Кажется, Вы поставили оценку за день, но не описали его с помощью эмодзи.\n\n' \
                  f'Пожалуйста, отправьте не более трёх эмодзи (слитно, без пробелов и других символов), которыми ' \
                  f'Вы можете описать пройденный день:'
            processing_date[message.from_user.id] = date
            await Form.emojis.set()
            await message.reply(msg)
    else:
        msg = f'Пожалуйста, выберите оценку, которую бы Вы поставили пройденному дню ({date.strftime("%d.%m.%Y")}):'
        await message.reply(msg, reply_markup=get_marks(date))


@dp.callback_query_handler(Text(startswith='set_mark_'))
async def set_mark(call: types.CallbackQuery):
    mark = call.data[9:10]
    date = datetime.datetime.strptime(call.data[11:], '%d_%m_%Y')
    save_mark(str(call.from_user.id), mark, date)

    msg = 'Теперь отправьте не более трёх эмодзи (слитно, без пробелов и других символов), ' \
          'которыми Вы можете описать пройденный день:'
    processing_date[call.from_user.id] = date
    await Form.emojis.set()
    await call.message.reply(msg)


def is_emojis_message_correct(msg):
    emojis_count = 0
    for c in msg:
        if not c.isspace() and not emoji.is_emoji(c):
            return False
        if emoji.is_emoji(c):
            emojis_count += 1
    if emojis_count > 3:
        return False
    return True


@dp.message_handler(state=Form.emojis)
async def set_emojis(message: types.Message, state: FSMContext):
    if not is_emojis_message_correct(message.text):
        msg = 'Пожалуйста, введите не более трёх эмодзи без разделителей и лишних символов.'
        await message.reply(msg)
    else:
        emojis = []
        for c in message.text:
            if emoji.is_emoji(c):
                emojis.append(c)
        save_emotions(str(message.from_user.id), emojis, processing_date[message.from_user.id])
        processing_date.pop(message.from_user.id)
        await state.finish()
        await message.reply('Описание дня успешно сохранено!', reply_markup=get_main_menu())


@dp.callback_query_handler(Text(startswith='change_day_'))
async def change_day_mark(call: types.CallbackQuery):
    date = datetime.datetime.strptime(call.data[11:], '%d_%m_%Y')
    msg = f'Пожалуйста, выберите оценку, которую бы Вы поставили пройденному дню ({date.strftime("%d.%m.%Y")}):'
    await call.message.reply(msg, reply_markup=get_marks(date))


@dp.callback_query_handler(Text(equals='keep_old_mark'))
async def keep_old_mark(call: types.CallbackQuery):
    await call.message.reply('Хорошо, оставляем прежнюю оценку.', reply_markup=get_main_menu())


@dp.message_handler(Text(equals='Оценить сегодняшний день'))
async def evaluate_today(message: types.Message):
    await evaluate(message, datetime.datetime.today())


@dp.message_handler(Text(equals='Оценить вчерашний день'))
async def evaluate_yesterday(message: types.Message):
    await evaluate(message, datetime.datetime.today() - datetime.timedelta(days=1))


@dp.message_handler(Text(equals='Воспоминания'))
async def get_old_records(message: types.Message):
    await Form.get_date.set()
    await message.reply('Пожалуйста, введите дату, за которую Вы хотите получить информацию, в формате ДД.ММ.ГГГГ')


@dp.message_handler(state=Form.get_date)
async def print_record(message: types.Message, state: FSMContext):
    date = datetime.datetime.strptime(message.text, '%d.%m.%Y')
    mark = find_mark_by_user_id_and_date(str(message.from_user.id), date)
    emotions = find_emotions_by_user_id_and_date(str(message.from_user.id), date)
    msg = ''
    if mark is None and emotions is None:
        msg = 'К сожалению, оценка за этот день не найдена.'
    else:
        if mark is not None:
            msg = f'Оценка за {date.strftime("%d.%m.%Y")}: {mark.mark}'
        if emotions is not None:
            msg += f'\nЭмоции за {date.strftime("%d.%m.%Y")}: {emotions.get_emojis()}'

    notes = get_notes_by_user_id_and_date(str(message.from_user.id), date)
    if notes is not None and len(notes) > 0:
        msg += '\n\nНайдены следующие записи:\n'
        for i, note in enumerate(notes, 1):
            msg += f'\n<b><i>Запись #{i}:</i></b>\n{note.note}\n'

    files = get_media_by_user_id_and_date(str(message.from_user.id), date)
    if files is not None and len(files) > 0:
        msg += '\n\nНайдены следующие медиафайлы за этот день:'
    await state.finish()
    await message.reply(msg, reply_markup=get_main_menu())

    MEDIA_TYPE_MAPPING = {'PHOTO': InputMediaPhoto, 'VIDEO': InputMediaVideo}
    if len(files) == 1:
        if files[0].file_type == 'PHOTO':
            await bot.send_photo(message.from_user.id, files[0].media_url)
        elif files[0].file_type == 'VIDEO':
            await bot.send_video(message.from_user.id, files[0].media_url)
    elif len(files) > 1:
        for i in range(0, len(files), 10):
            group = files[i:i + 10]
            media_group = list(
                map(lambda media_file: MEDIA_TYPE_MAPPING[media_file.file_type](media_file.media_url), group)
            )
            await bot.send_media_group(message.from_user.id, media_group)


@dp.message_handler(Text(equals='Настройки уведомлений'))
async def change_settings(message: types.Message):
    await message.reply('Выберите, присылать ли Вам ежедневные уведомления с напоминанием воспользоваться ботом?',
                        reply_markup=get_settings_menu())


@dp.message_handler(Text(equals='Добавить заметку'))
async def get_note_date(message: types.Message):
    await Form.note_date.set()
    await message.reply('Пожалуйста, напишите дату, за какой день Вы хотите добавить заметку, в формате ДД.ММ.ГГГГ')


@dp.message_handler(state=Form.note_date)
async def get_note(message: types.Message, state: FSMContext):
    date = datetime.datetime.strptime(message.text, '%d.%m.%Y')
    processing_note_date[message.from_user.id] = date
    await state.finish()
    await Form.note.set()
    await message.reply('Теперь напишите саму заметку, которую Вы хотите сохранить:')


@dp.message_handler(state=Form.note)
async def add_note(message: types.Message, state: FSMContext):
    date = processing_note_date[message.from_user.id]
    processing_note_date.pop(message.from_user.id)
    save_note(str(message.from_user.id), message.text, date)
    await state.finish()
    await message.reply('Заметка успешно сохранена!', reply_markup=get_main_menu())


@dp.message_handler(Text(equals='Добавить фото/видео'))
async def get_media_date(message: types.Message):
    await Form.media_date.set()
    await message.reply('Пожалуйста, напишите дату, к какому дню Вы хотите прикрепить фото/видео, в формате ДД.ММ.ГГГГ')


@dp.message_handler(state=Form.media_date)
async def get_media(message: types.Message, state: FSMContext):
    date = datetime.datetime.strptime(message.text, '%d.%m.%Y')
    processing_media_date[message.from_user.id] = date
    await state.finish()
    await Form.media.set()
    await message.reply('Теперь отправьте ровно ОДНО фото или видео, которое Вы хотите сохранить (НЕ файлом):')


@dp.message_handler(state=Form.media, content_types=types.ContentTypes.ANY)
async def add_media(message: types, state: FSMContext):
    date = processing_media_date[message.from_user.id]
    processing_media_date.pop(message.from_user.id)
    err = False
    if message.photo:
        save_media_url(str(message.from_user.id), message.photo[-1].file_id, 'PHOTO', date)
    elif message.video:
        save_media_url(str(message.from_user.id), message.video.file_id, 'VIDEO', date)
    else:
        err = True
    if err:
        await message.reply('Хм, кажется, это не фото и не видео... Пожалуйста, попробуйте ещё раз или воспользуйтесь '
                            'командой /cancel')
    else:
        await state.finish()
        await message.reply('Медиафайл успешно сохранён!', reply_markup=get_main_menu())


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
