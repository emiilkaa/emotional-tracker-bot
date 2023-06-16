import datetime

from app.entity.user import User
from app.repository.db import session

def get_user_by_telegram_id(user_id):
    return session.query(User).filter(User.user_ext_id == user_id).first()

def save_user(user_id, first_name, second_name, username, subscribed):
    session.add(User(user_ext_id=user_id, first_name=first_name, second_name=second_name, username=username,
                     subscribed=subscribed, date_registered=datetime.datetime.now()))
    session.commit()
