import datetime

from aiogram import types

def get_subscribe_menu():
    subscribe_menu = types.InlineKeyboardMarkup(row_width=2)
    subscribe_menu.add(types.InlineKeyboardButton(text='Да', callback_data='subscribe_true'))
    subscribe_menu.insert(types.InlineKeyboardButton(text='Нет', callback_data='subscribe_false'))
    return subscribe_menu

def get_settings_menu():
    subscribe_menu = types.InlineKeyboardMarkup(row_width=1)
    subscribe_menu.add(types.InlineKeyboardButton(text='Присылать напоминания', callback_data='subscribe_true'))
    subscribe_menu.insert(types.InlineKeyboardButton(text='Не присылать напоминания', callback_data='subscribe_false'))
    return subscribe_menu

def get_main_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    menu.add('Оценить сегодняшний день')
    menu.add('Оценить вчерашний день')
    menu.add('Добавить заметку')
    # TODO: Добавить раздел "Статистика"
    # menu.add(*['Воспоминания', 'Статистика'])
    menu.add('Воспоминания')
    menu.add('Настройки уведомлений')
    return menu

def get_change_day_menu(date: datetime.date):
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(types.InlineKeyboardButton(text='Поменять оценку/эмодзи', callback_data=f'change_day_{date.strftime("%d_%m_%Y")}'))
    menu.add(types.InlineKeyboardButton(text='Оставить как есть', callback_data='keep_old_mark'))
    return menu

def get_marks(date: datetime.date):
    menu = types.InlineKeyboardMarkup(row_width=5)
    marks = [('5', '😍'), ('4', '🙂'), ('3', '😐'), ('2', '😕'), ('1', '☹️')]
    menu.add(types.InlineKeyboardButton(text=f'{marks[0][0]} {marks[0][1]}',
                                        callback_data=f'set_mark_{marks[0][0]}_{date.strftime("%d_%m_%Y")}'))
    for i in range(1, 5):
        menu.insert(types.InlineKeyboardButton(text=f'{marks[i][0]} {marks[i][1]}',
                                               callback_data=f'set_mark_{marks[i][0]}_{date.strftime("%d_%m_%Y")}'))
    return menu
