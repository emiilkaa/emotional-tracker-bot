import datetime

from sqlalchemy import and_

from app.entity.note import Note
from app.repository.db import session


def get_notes_by_user_id_and_date(user_id, date):
    return session.query(Note).filter(and_(Note.user_ext_id == user_id, Note.assessment_date == date)).all()


def save_note(user_id, note, date):
    session.add(Note(assessment_date=date, user_ext_id=user_id, note=note, date_created=datetime.datetime.now()))
    session.commit()
