from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



Base = declarative_base()

engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()






