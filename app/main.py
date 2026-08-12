from fastapi import FastAPI

from .database import Base, engine
from .routers import issues

# Creates any tables that don't exist yet, based on the models imported
# above. Fine for development; once your schema is live with real data,
# schema changes should go through Alembic migrations instead (Stage 2 —
# see the "what's next" note in the README).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CivicTrack API",
    description="Hyperlocal civic issue reporting platform — Phase 1 & 2",
    version="0.1.0",
)

app.include_router(issues.router)


@app.get("/")
def root():
    return {"message": "CivicTrack API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
