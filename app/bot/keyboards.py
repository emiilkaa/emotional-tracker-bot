from aiogram import types

def get_subscribe_menu():
    subscribe_menu = types.InlineKeyboardMarkup(row_width=2)
    subscribe_menu.add(types.InlineKeyboardButton(text='Да', callback_data='subscribe_true'))
    subscribe_menu.insert(types.InlineKeyboardButton(text='Нет', callback_data='subscribe_false'))
    return subscribe_menu

def get_main_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    menu.add('Оценить сегодняшний день')
    menu.add('Оценить вчерашний день')
    menu.add(*['Воспоминания', 'Статистика'])
    menu.add('Настройки уведомлений')
    return menu
