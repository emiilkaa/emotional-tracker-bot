import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

hostname = os.environ['EMOTIONS_DB_HOST']
username = os.environ['EMOTIONS_DB_USER']
password = os.environ['EMOTIONS_DB_PASS']
db_name = os.environ['EMOTIONS_DB_NAME']
url = f'postgresql://{username}:{password}@{hostname}/{db_name}'

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
