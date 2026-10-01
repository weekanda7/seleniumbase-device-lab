from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers import router
from app.exceptions import DeviceNotFound, DomainError, DuplicateDeviceName, InvalidCredentials, Unauthorized
from app.infrastructure.database import SessionLocal, init_db
from app.seed import seed_if_empty

# Domain error -> HTTP status. Request-body validation errors are FastAPI's own 422.
_STATUS = {
    DeviceNotFound: 404,
    DuplicateDeviceName: 409,
    InvalidCredentials: 401,
    Unauthorized: 401,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with SessionLocal() as db:
        seed_if_empty(db)
    yield


app = FastAPI(title="Device Lab", lifespan=lifespan)
app.include_router(router)


@app.exception_handler(DomainError)
def handle_domain_error(request: Request, exc: DomainError):
    return JSONResponse(status_code=_STATUS.get(type(exc), 400), content={"detail": str(exc)})
