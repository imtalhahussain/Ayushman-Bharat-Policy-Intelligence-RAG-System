from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# For now, use SQLite; later: set DATABASE_URL in env to a Postgres URL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
