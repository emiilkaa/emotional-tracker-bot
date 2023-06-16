from sqlalchemy import Column, Integer, String, DateTime, Date

from app.entity.base import Base


class Emotions(Base):
    __tablename__ = 'emotions'

    id = Column(Integer, primary_key=True)
    assessment_date = Column(Date, nullable=False)
    user_ext_id = Column(String, nullable=False)
    emoji1 = Column(String, nullable=False)
    emoji2 = Column(String)
    emoji3 = Column(String)
    date_created = Column(DateTime(timezone=False), nullable=False)
    date_updated = Column(DateTime(timezone=False))
