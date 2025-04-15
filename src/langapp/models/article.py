from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.langapp.database import Base


class Article(Base):
    __tablename__ = "article"

    pk: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    text: Mapped[str] = mapped_column(Text())
    creation_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
