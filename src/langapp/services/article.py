from datetime import datetime

from fastapi import HTTPException, status
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.langapp.models import Article
from src.langapp.schemas import ArticleData, ArticleUpdate


def create_article(db: Session, data: ArticleData) -> Article:
    try:
        article = Article(title=data.title, text=data.text)
        db.add(article)
        db.commit()
        return article
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error",
        ) from e


def find_all_articles(db: Session) -> list[Article]:
    all_articles = db.scalars(select(Article).order_by(Article.pk)).all()
    return all_articles


def find_article(db: Session, pk: PositiveInt) -> Article:
    article = db.scalar(select(Article).where(Article.pk == pk))
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Article {pk} not found"
        )
    return article


def replace_article(db: Session, pk: PositiveInt, data: ArticleData) -> Article:
    article = db.scalar(select(Article).where(Article.pk == pk))
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Article {pk} not found"
        )
    try:
        article.title = data.title
        article.text = data.text
        article.creation_date = datetime.now()
        db.commit()
        db.refresh(article)
        return article
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to replace the article",
        ) from e


def update_article(db: Session, pk: PositiveInt, data: ArticleUpdate) -> Article:
    article = db.scalar(select(Article).where(Article.pk == pk))
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Article {pk} not found"
        )
    try:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(article, field, value)
        db.commit()
        return article
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update the article",
        ) from e


def delete_article(db: Session, pk: PositiveInt) -> None:
    article = db.scalar(select(Article).where(Article.pk == pk))
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Article {pk} not found"
        )
    try:
        db.delete(article)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete the article",
        ) from e
