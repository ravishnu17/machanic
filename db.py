from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_url= 'postgresql://machanic:machanic@localhost:5432/machanic'

try:
    engine= create_engine(db_url)
    session= sessionmaker(autoflush=False, autocommit=False, bind= engine)
    print("Connected")
except Exception as err:
    print(err)


base= declarative_base()

def get_db():
    db= session()

    try:
        yield db
    finally:
        db.close()
