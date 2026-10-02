import uvicorn

from backend.infra.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host=settings.app_host,
        port=settings.app_port,

    )