import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.domain.models import Base

# Inside docker compose this is overridden to point at the `db` service.
# The default lets you run uvicorn on your Mac against the compose DB (host port 5433).
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://devicelab:devicelab@localhost:5433/devicelab",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker[Session](autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    """One session per request. The service commits explicitly, so a failed
    commit still turns into an error response (not a 2xx)."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
