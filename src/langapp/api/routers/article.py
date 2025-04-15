from typing import List

from fastapi import APIRouter, status

from src.langapp import services
from src.langapp.database import DbSession
from src.langapp.schemas import ArticleData, ArticlePublic, ArticleUpdate

article_router = APIRouter(prefix="/article")


@article_router.post("")
async def create_article(db: DbSession, data: ArticleData):
    return services.create_article(db=db, data=data)


@article_router.get("")
async def find_all_articles(db: DbSession):
    return services.find_all_articles(db=db)


@article_router.get("/{pk}")
async def find_article(db: DbSession, pk: int):
    return services.find_article(db=db, pk=pk)


@article_router.udpade("/{pk}")
async def replace_article(db: DbSession, pk: int, data: ArticleUpdate):
    return services.replace_article(db=db, pk=pk, data=data)


@article_router.patch("/{pk}")
async def update_article(db: DbSession, pk: int, data: ArticleUpdate):
    return services.update_article(db=db, pk=pk, data=data)


@article_router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(db: DbSession, pk: int):
    services.delete_article(db=db, pk=pk)
