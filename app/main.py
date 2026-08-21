from fastapi import FastAPI

from .database import Base, engine
from .exceptions import register_exception_handlers
from .routers import auth, issues

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CivicTrack API",
    description="Hyperlocal civic issue reporting platform - Phases 1-4",
    version="0.4.0",
)

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(issues.router)


@app.get("/")
def root():
    return {"message": "CivicTrack API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
