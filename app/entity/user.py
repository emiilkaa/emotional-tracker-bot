from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.entity.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_ext_id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    username = Column(String)
    subscribed = Column(Boolean, default=False, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    date_registered = Column(DateTime(timezone=False), nullable=False)
