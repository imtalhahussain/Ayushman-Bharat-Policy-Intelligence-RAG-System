from backend.app.db.session import engine
from backend.app.db.base import Base
from backend.app.db import models  # noqa: F401  # ensures models are registered

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
