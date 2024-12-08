from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from reling.db.base import Base

__all__ = [
    'Language',
]


class Language(Base):
    __tablename__ = 'languages'

    id: Mapped[str] = mapped_column(primary_key=True)
    short_code: Mapped[str] = mapped_column(index=True)
    name: Mapped[str]
    extra_name_a: Mapped[str | None]
    extra_name_b: Mapped[str | None]

    __table_args__ = (
        Index('language_name', func.lower('name')),
        Index('language_extra_name_a', func.lower('extra_name_a')),
        Index('language_extra_name_b', func.lower('extra_name_b')),
    )
