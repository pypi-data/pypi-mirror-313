from sqlalchemy.orm import Mapped, mapped_column

from reling.db.base import Base
from reling.db.enums import ContentCategory

__all__ = [
    'IdIndex',
]


class IdIndex(Base):
    __tablename__ = 'id_index'

    id: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[ContentCategory]
