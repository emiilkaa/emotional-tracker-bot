import datetime

from sqlalchemy import and_

from app.entity.media import Media
from app.repository.db import session


def get_media_by_user_id_and_date(user_id, date):
    return session.query(Media).filter(and_(Media.user_ext_id == user_id, Media.assessment_date == date)).all()


def save_media_url(user_id, url, file_type, date):
    session.add(Media(assessment_date=date, user_ext_id=user_id, media_url=url, file_type=file_type, date_created=datetime.datetime.now()))
    session.commit()
