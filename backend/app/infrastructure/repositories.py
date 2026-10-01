from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Device


class DeviceRepository:
    """All SQL for devices lives here; the service never writes queries."""

    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Device]:
        return list(self.db.scalars(select(Device).order_by(Device.id)))

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
