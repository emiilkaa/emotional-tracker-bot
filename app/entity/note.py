from sqlalchemy import Column, Integer, String, DateTime, Date

from app.entity.base import Base


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    assessment_date = Column(Date, nullable=False)
    user_ext_id = Column(String, nullable=False)
    note = Column(String, nullable=False)
    date_created = Column(DateTime(timezone=False), nullable=False)
