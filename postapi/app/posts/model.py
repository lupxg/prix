from ..extensions import db
from sqlalchemy import (
    String, 
    DateTime, 
    Text,  
    ForeignKey, 
    Enum
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Post(db.Model):
    """ Post Entity
    """

    __tablename__ = "post"
    __abstract__ = False

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(150), 
        nullable=False
    )
    body: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    status: Mapped[str] = mapped_column(
        Enum("draft", "published", "archived", name="post_status"), 
        default="draft"
    )
