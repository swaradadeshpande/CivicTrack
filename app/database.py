import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/civictrack")

# pool_pre_ping checks a connection is still alive before handing it out —
# avoids "MySQL server has gone away" errors after periods of idle time.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session per request, always closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
