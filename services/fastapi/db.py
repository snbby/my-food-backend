import os

from sqlmodel import Session, create_engine

MYFOOD_DATABASE_HOST = os.getenv('MYFOOD_DATABASE_HOST', 'localhost')
MYFOOD_DATABASE_PORT = os.getenv('MYFOOD_DATABASE_PORT', '5432')
MYFOOD_DATABASE_NAME = os.getenv('MYFOOD_DATABASE_NAME', '')
MYFOOD_DATABASE_USER = os.getenv('MYFOOD_DATABASE_USER', '')
MYFOOD_DATABASE_PASS = os.getenv('MYFOOD_DATABASE_PASS', '')

DATABASE_URL = f'postgresql://{MYFOOD_DATABASE_USER}:{MYFOOD_DATABASE_PASS}@{MYFOOD_DATABASE_HOST}:{MYFOOD_DATABASE_PORT}/{MYFOOD_DATABASE_NAME}'
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session