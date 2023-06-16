from sqlalchemy import Column, Integer, String, DateTime, Date

from app.entity.base import Base


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    assessment_date = Column(Date, nullable=False)
    user_ext_id = Column(String, nullable=False)
    media_url = Column(String, nullable=False)
    date_created = Column(DateTime(timezone=False), nullable=False)
