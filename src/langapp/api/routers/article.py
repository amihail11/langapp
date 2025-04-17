from fastapi import APIRouter, status
from pydantic import PositiveInt

from src.langapp import services
from src.langapp.database import DbSession
from src.langapp.schemas import ArticleData, ArticlePublic, ArticleUpdate

article_router = APIRouter(prefix="/article")


@article_router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=ArticlePublic
)
async def create_article(db: DbSession, data: ArticleData) -> ArticlePublic:
    return services.create_article(db=db, data=data)


@article_router.get("", response_model=list[ArticlePublic])
async def find_all_articles(db: DbSession) -> list[ArticlePublic]:
    return services.find_all_articles(db=db)


@article_router.get("/{pk}", response_model=ArticlePublic)
async def find_article(db: DbSession, pk: PositiveInt) -> ArticlePublic:
    return services.find_article(db=db, pk=pk)


@article_router.put("/{pk}", response_model=ArticlePublic)
async def replace_article(
    db: DbSession, pk: PositiveInt, data: ArticleUpdate
) -> ArticlePublic:
    return services.replace_article(db=db, pk=pk, data=data)


@article_router.patch("/{pk}", response_model=ArticlePublic)
async def update_article(
    db: DbSession, pk: PositiveInt, data: ArticleUpdate
) -> ArticlePublic:
    return services.update_article(db=db, pk=pk, data=data)


@article_router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(db: DbSession, pk: PositiveInt) -> None:
    services.delete_article(db=db, pk=pk)
