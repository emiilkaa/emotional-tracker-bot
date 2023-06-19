import datetime

from sqlalchemy import and_

from app.entity.user import User
from app.repository.db import session


def get_user_by_telegram_id(user_id):
    return session.query(User).filter(User.user_ext_id == user_id).first()


def save_user(user_id, first_name, second_name, username, subscribed, active=True):
    if get_user_by_telegram_id(user_id) is None:
        session.add(User(user_ext_id=user_id, first_name=first_name, second_name=second_name, username=username,
                         subscribed=subscribed, active=active, date_registered=datetime.datetime.now()))
        session.commit()
    else:
        session.query(User).filter(User.user_ext_id == user_id).update({'subscribed': subscribed, 'active': active})
        session.commit()


def get_subscribed_users():
    return session.query(User).filter(and_(User.active == True, User.subscribed == True)).all()


def delete_user(user_id):
    if get_user_by_telegram_id(user_id) is not None:
        session.query(User).filter(User.user_ext_id == user_id).update({'active': False})
        session.commit()
