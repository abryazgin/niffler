from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from niffler import app

url = app.config.get('DATABASE_URL')
engine = create_engine(url)
Session = sessionmaker(bind=engine)
