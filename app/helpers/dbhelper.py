import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, class_mapper
 

engine = create_engine(config.database_url, encoding="utf8", pool_size=100, max_overflow=20)

Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def serialize(model):
  columns = [c.key for c in class_mapper(model.__class__).columns]
  return dict((c, getattr(model, c)) for c in columns)