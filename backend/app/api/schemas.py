from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

DeviceType = Literal["Router", "Switch", "AP", "Sensor"]
DeviceName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)]
Location = Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)]


class LoginIn(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DeviceCreate(BaseModel):
    # extra="forbid": unknown fields -> 422 instead of being silently ignored
    model_config = ConfigDict(extra="forbid")

    name: DeviceName
    type: DeviceType
    location: Location = ""


class DeviceReplace(DeviceCreate):
    """PUT = full replacement; an omitted location resets to ""."""


class DevicePatch(BaseModel):
    """PATCH = partial update; only fields present in the body change."""

    model_config = ConfigDict(extra="forbid")

    name: DeviceName | None = None
    type: DeviceType | None = None
    location: Location | None = None

    @field_validator("name", "type", "location")
    @classmethod
    def reject_explicit_null(cls, value):
        # Runs only for fields the client actually sent, so {"name": null} -> 422.
        if value is None:
            raise ValueError("must not be null")
        return value


class DeviceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    location: str
    created_at: datetime
