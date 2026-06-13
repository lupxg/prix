from ..extensions import db
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Post(db.Model):
    """ Post Entity
    """

    __tablename__ = "post"
    __abstract__ = False

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    # slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), default="draft")
