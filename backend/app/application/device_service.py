from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.models import Device
from app.exceptions import DeviceNotFound, DuplicateDeviceName
from app.infrastructure.repositories import DeviceRepository


class DeviceService:
    """Business rules for devices: name must be unique, missing id -> 404."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = DeviceRepository(db)

    def list_devices(self, q: str | None = None, status: str | None = None) -> list[Device]:
        return self.repo.list(q=q, status=status)

    def get_device(self, device_id: int) -> Device:
        device = self.repo.get(device_id)
        if device is None:
            raise DeviceNotFound(device_id)
        return device

    def create_device(self, name: str, type: str, status: str = "online", location: str = "") -> Device:
        self._ensure_name_free(name)
        device = self.repo.add(Device(name=name, type=type, status=status, location=location))
        self._commit(name)
        self.db.refresh(device)
        return device

    def update_device(self, device_id: int, changes: dict[str, Any]) -> Device:
        """PUT passes every field, PATCH passes only the fields the client sent."""
        device = self.get_device(device_id)
        new_name = changes.get("name")
        if new_name is not None and new_name != device.name:
            self._ensure_name_free(new_name)
        for field, value in changes.items():
            setattr(device, field, value)
        self._commit(new_name or device.name)
        self.db.refresh(device)
        return device

    def delete_device(self, device_id: int) -> None:
        device = self.get_device(device_id)
        self.repo.delete(device)
        self.db.commit()

    def _ensure_name_free(self, name: str) -> None:
        if self.repo.get_by_name(name) is not None:
            raise DuplicateDeviceName(name)

    def _commit(self, name: str) -> None:
        # Two requests can pass _ensure_name_free at the same time;
        # the unique constraint catches the loser here.
        try:
            self.db.commit()
        except IntegrityError as err:
            self.db.rollback()
            raise DuplicateDeviceName(name) from err
