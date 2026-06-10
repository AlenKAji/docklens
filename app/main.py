from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import Settings

settings = Settings.from_env()

app = FastAPI(
    title=settings.app_name,
    description="Docker fleet health and drift monitor",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse("app/static/index.html")
