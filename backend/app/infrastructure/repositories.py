from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.domain.models import Device


class DeviceRepository:
    """All SQL for devices lives here; the service never writes queries."""

    def __init__(self, db: Session):
        self.db = db

    def list(self, q: str | None = None, status: str | None = None) -> list[Device]:
        stmt = select(Device).order_by(Device.id)
        if q:
            pattern = f"%{q}%"
            # ILIKE = case-insensitive LIKE; search both name and location
            stmt = stmt.where(or_(Device.name.ilike(pattern), Device.location.ilike(pattern)))
        if status:
            stmt = stmt.where(Device.status == status)
        return list(self.db.scalars(stmt))

    def get(self, device_id: int) -> Device | None:
        return self.db.get(Device, device_id)

    def get_by_name(self, name: str) -> Device | None:
        return self.db.scalar(select(Device).where(Device.name == name))

    def add(self, device: Device) -> Device:
        self.db.add(device)
        self.db.flush()
        return device

    def delete(self, device: Device) -> None:
        self.db.delete(device)
