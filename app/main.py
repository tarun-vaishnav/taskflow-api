from fastapi import FastAPI

from app.config import settings
from app.routers.tasks import router as task_router

app = FastAPI(
    title=settings.app_name,
    description="A production grade Task management API",
    version=settings.app_version,
)

@app.get("/health")
def health_check():
    return {"status":"OK"}

app.include_router(task_router)