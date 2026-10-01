from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.models import Device

SEED_DEVICES = [
    {"name": "core-router-01", "type": "Router", "location": "Server room"},
    {"name": "office-switch-01", "type": "Switch", "location": "3F office"},
    {"name": "lobby-ap-01", "type": "AP", "location": "1F lobby"},
]


def seed_if_empty(db: Session) -> None:
    """Insert the 3 seed devices only into an empty table, so restarts don't duplicate them."""
    count = db.scalar(select(func.count()).select_from(Device))
    if count:
        return
    db.add_all(Device(**data) for data in SEED_DEVICES)
    db.commit()
