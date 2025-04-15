from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.langapp.models import Article
from src.langapp.schemas import ArticleData, ArticlePublic, ArticleUpdate


def create_article(db: Session, data: ArticleData):
    article = Article(title=data.title, text=data.text)
    db.add(article)
    db.commit()
    return article


def find_all_articles(db: Session):
    all_articles = db.scalars(select(Article).order_by(Article.pk))
    return all_articles


def find_article(db: Session, pk: int):
    article = db.scalar(select(Article).where(Article.pk == pk))
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    return article


def replace_article(db: Session, pk: int, data: ArticleUpdate):
    article = db.scalar(select(Article).where(Article.pk == pk))
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    article.title = data.title
    article.text = data.text
    db.commit()
    return article


def update_article(db: Session, pk: int, data: ArticleUpdate) -> Article:
    article = db.scalar(select(Article).where(Article.pk == pk))
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields for updating provided",
        )
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(article, field, value)
    db.commit()
    return article


def delete_article(db: Session, pk: int) -> None:
    article = db.scalar(select(Article).where(Article.pk == pk))
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    try:
        db.delete(article)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete the article",
        )
