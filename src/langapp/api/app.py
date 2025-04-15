from fastapi import FastAPI

from src.langapp.api.routers import article_router

app = FastAPI()

app.include_router(article_router)
