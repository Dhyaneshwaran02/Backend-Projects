from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL="postgresql://postgres:123@localhost/fastapi"

engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",
#         password="123", cursor_factory=RealDictCursor)

#         cur = conn.cursor()
#         print("Db connection was successful")
#         break
#     except Exception as error:
#         print("Error:",error)
#         print("Db connection failed")
#         time.sleep(2)
