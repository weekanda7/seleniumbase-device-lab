import os

from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.api.schemas import (
    DeviceCreate,
    DeviceOut,
    DevicePatch,
    DeviceReplace,
    DeviceStatus,
    LoginIn,
    LoginOut,
    VersionOut,
)
from app.application import auth_service
from app.application.device_service import DeviceService
from app.exceptions import InvalidCredentials, Unauthorized
from app.infrastructure.database import get_db

router = APIRouter(prefix="/api")
_bearer = HTTPBearer(auto_error=False)


def require_token(credentials: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> str:
    if credentials is None or not auth_service.is_valid(credentials.credentials):
        raise Unauthorized()
    return credentials.credentials


def get_device_service(db: Session = Depends(get_db)) -> DeviceService:
    return DeviceService(db)


@router.get("/health")
def health():
    return {"status": "ok"}


# Public, like /health: a deploy check or the UI footer can read it without logging in.
# Values are baked into the image at build time (Dockerfile ARG -> ENV).
@router.get("/version", response_model=VersionOut)
def version():
    return VersionOut(version=os.getenv("APP_VERSION", "dev"), commit=os.getenv("GIT_SHA", "unknown"))


@router.post("/auth/login", response_model=LoginOut)
def login(body: LoginIn):
    token = auth_service.login(body.username, body.password)
    if token is None:
        raise InvalidCredentials()
    return LoginOut(access_token=token)


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: str = Depends(require_token)):
    auth_service.logout(token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Every /api/devices endpoint needs a valid Bearer token.
devices = APIRouter(prefix="/devices", tags=["devices"], dependencies=[Depends(require_token)])


@devices.get("", response_model=list[DeviceOut])
def list_devices(
    q: str | None = Query(None, max_length=50, description="Search name or location (case-insensitive)"),
    device_status: DeviceStatus | None = Query(None, alias="status"),
    service: DeviceService = Depends(get_device_service),
):
    return service.list_devices(q=q, status=device_status)


@devices.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: int, service: DeviceService = Depends(get_device_service)):
    return service.get_device(device_id)


@devices.post("", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(body: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    return service.create_device(**body.model_dump())


@devices.put("/{device_id}", response_model=DeviceOut)
def replace_device(device_id: int, body: DeviceReplace, service: DeviceService = Depends(get_device_service)):
    return service.update_device(device_id, body.model_dump())


@devices.patch("/{device_id}", response_model=DeviceOut)
def patch_device(device_id: int, body: DevicePatch, service: DeviceService = Depends(get_device_service)):
    return service.update_device(device_id, body.model_dump(exclude_unset=True))


@devices.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, service: DeviceService = Depends(get_device_service)):
    service.delete_device(device_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


router.include_router(devices)
