from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DSN = 'postgresql://postgres:Oo332211oo.@db:5432/habits_tracker'


engine = create_engine(DSN)

session_local = sessionmaker(autoflush=False, autocommit=False ,bind=engine)

Base = declarative_base()