from datetime import datetime

from pydantic import BaseModel


class ArticleData(BaseModel):
    title: str
    text: str


class ArticleUpdate(ArticleData):
    title: str | None = None
    text: str | None = None


class ArticlePublic(ArticleData):
    pk: int
    creation_date: datetime
