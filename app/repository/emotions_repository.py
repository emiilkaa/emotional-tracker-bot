import datetime

from sqlalchemy import and_

from app.entity.emotions import Emotions
from app.repository.db import session

def find_emotions_by_user_id_and_date(user_id, date):
    return session.query(Emotions).filter(and_(Emotions.user_ext_id == user_id, Emotions.assessment_date == date.strftime('%Y-%m-%d'))).first()

def save_emotions(user_id, emojis, date):
    if find_emotions_by_user_id_and_date(user_id, date) is None:
        entry = Emotions(assessment_date=date, user_ext_id=user_id, emoji1=emojis[0], date_created=datetime.datetime.now())
        if len(emojis) > 1:
            entry.emoji2 = emojis[1]
            if len(emojis) > 2:
                entry.emoji3 = emojis[2]
        session.add(entry)
        session.commit()
    else:
        new_fields = {'emoji1': emojis[0]}
        if len(emojis) > 1:
            new_fields['emoji2'] = emojis[1]
            if len(emojis) > 2:
                new_fields['emoji3'] = emojis[2]
            else:
                new_fields['emoji3'] = None
        else:
            new_fields['emoji2'] = None
            new_fields['emoji3'] = None
        new_fields['date_updated'] = datetime.datetime.now()
        session.query(Emotions).filter(and_(Emotions.user_ext_id == user_id, Emotions.assessment_date == date.strftime('%Y-%m-%d'))).update(
            new_fields
        )
        session.commit()
