import datetime
import os.path
import uuid

import matplotlib.pyplot as plt

from app.repository.marks_repository import get_marks_by_user_id_and_date_in


def marks_histogram(user_id, days_count):
    plt.clf()
    user_marks = get_marks_by_user_id_and_date_in(user_id,
                                                  datetime.datetime.today() - datetime.timedelta(days=days_count))
    if user_marks is None or len(user_marks) == 0:
        return None
    marks = list()
    for el in user_marks:
        marks.append(el.mark)
    possible_numbers = [1, 2, 3, 4, 5]
    counts = [marks.count(num) for num in possible_numbers]
    percentages = [count / len(marks) * 100 for count in counts]
    colors = ['red', 'orange', 'yellow', 'limegreen', 'green']
    numbers_to_show = [num for num in possible_numbers if num in marks]
    fig, ax = plt.subplots()
    ax.pie([percentages[possible_numbers.index(num)] for num in numbers_to_show], labels=numbers_to_show,
           autopct='%1.1f%%', colors=[colors[possible_numbers.index(num)] for num in numbers_to_show])
    ax.set_title(f'Процентное соотношение каждой оценки за последние {days_count + 1} дней')
    name_of_file = os.path.join('bot', 'files', f'{user_id}_{uuid.uuid4().hex}.png')
    plt.savefig(name_of_file)
    return name_of_file


def marks_linegraph(user_id, days_count):
    plt.clf()
    user_marks = get_marks_by_user_id_and_date_in(user_id,
                                                  datetime.datetime.today() - datetime.timedelta(days=days_count))
    if user_marks is None or len(user_marks) == 0:
        return None
    mark_date = dict()
    for el in user_marks:
        mark_date[el.assessment_date.strftime('%d.%m.%Y')] = el.mark
    today = datetime.datetime.today()
    dates = []
    for i in range(days_count, -1, -1):
        dates.append((today - datetime.timedelta(days=i)).strftime('%d.%m.%Y'))
    plt.figure(figsize=(10, 8))
    plt.plot([mark_date.get(date, None) for date in dates], marker='o')
    if len(dates) > 10:
        plt.xticks(range(len(dates)), [dates[i] if i % 5 == 0 or i == len(dates) - 1 else '' for i in range(len(dates))], rotation=20)
    else:
        plt.xticks(range(len(dates)), dates, rotation=20)
    plt.yticks(range(7), ['', '1', '2', '3', '4', '5', ''])
    plt.title(f'Тренд по оценкам за последние {days_count + 1} дней')
    plt.xlabel('Дата')
    plt.ylabel('Оценка дня')
    name_of_file = os.path.join('bot', 'files', f'{user_id}_{uuid.uuid4().hex}.png')
    plt.savefig(name_of_file)
    return name_of_file
