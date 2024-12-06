from sqlalchemy.orm import Mapped, mapped_column

from reling.db.base import Base

__all__ = [
    'Speaker',
    'Style',
    'Topic',
]


class Topic(Base):
    __tablename__ = 'topics'

    name: Mapped[str] = mapped_column(primary_key=True)


class Style(Base):
    __tablename__ = 'styles'

    name: Mapped[str] = mapped_column(primary_key=True)


class Speaker(Base):
    __tablename__ = 'speakers'

    name: Mapped[str] = mapped_column(primary_key=True)
