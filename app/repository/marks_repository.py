import datetime

from sqlalchemy import and_

from app.entity.mark import Mark
from app.repository.db import session


def find_mark_by_user_id_and_date(user_id, date):
    return session.query(Mark).filter(
        and_(Mark.user_ext_id == user_id, Mark.assessment_date == date.strftime('%Y-%m-%d'))).first()


def save_mark(user_id, mark, date):
    if find_mark_by_user_id_and_date(user_id, date) is None:
        entry = Mark(assessment_date=date, user_ext_id=user_id, mark=mark, date_created=datetime.datetime.now())
        session.add(entry)
        session.commit()
    else:
        new_fields = {'mark': mark, 'date_updated': datetime.datetime.now()}
        session.query(Mark).filter(
            and_(Mark.user_ext_id == user_id, Mark.assessment_date == date.strftime('%Y-%m-%d'))).update(new_fields)
        session.commit()


def f(user_id, days_count):
    user_emoji = get_marks_by_user_id_and_date_in(user_id,
                                                  datetime.datetime.today() - datetime.timedelta(days=days_count))
    mark_date = dict()
    for el in user_emoji:
        mark_date[el.assessment_date.strftime('%d.%m.%Y')] = el.mark
    today = datetime.datetime.today()
    dates = []
    for i in range(days_count, -1, -1):
        dates.append((today - datetime.timedelta(days=i)).strftime('%d.%m.%Y'))
    plt.plot(dates, [mark_date.get(date, None) for date in dates])
