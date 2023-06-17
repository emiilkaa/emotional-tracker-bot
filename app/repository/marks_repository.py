import datetime

from sqlalchemy import and_, func

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


def get_marks_by_user_id_and_date_in(user_id, date_start, date_end=None):
    if date_end is None:
        date_end = datetime.datetime.today()
    return session.query(Mark).filter(and_(Mark.user_ext_id == user_id, func.date(Mark.assessment_date) >= date_start,
                                           func.date(Mark.assessment_date) <= date_end)).all()
