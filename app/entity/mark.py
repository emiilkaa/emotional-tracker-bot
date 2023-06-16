from sqlalchemy import Column, Integer, String, DateTime, Date

from app.entity.base import Base


class Mark(Base):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key=True)
    assessment_date = Column(Date, nullable=False)
    user_ext_id = Column(String, nullable=False)
    mark = Column(Integer, nullable=False)
    date_created = Column(DateTime(timezone=False), nullable=False)
    date_updated = Column(DateTime(timezone=False))
