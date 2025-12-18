from fastapi import FastAPI

from .routers import items


def create_app() -> FastAPI:
    app = FastAPI(
        title="Items API",
        description="Простое тестовое CRUD API на FastAPI для работы с сущностью Item.",
        version="0.1.0",
    )

    app.include_router(items.router, prefix="/items", tags=["Items"])

    return app


app = create_app()




