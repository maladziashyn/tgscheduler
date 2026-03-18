from typing import Optional

from sqlalchemy import Integer, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Content(Base):
    __tablename__ = "content"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    message: Mapped[Optional[str]] = mapped_column(Text)
    img_id: Mapped[Optional[str]] = mapped_column(Text)
    added: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    used_count: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("0"))

