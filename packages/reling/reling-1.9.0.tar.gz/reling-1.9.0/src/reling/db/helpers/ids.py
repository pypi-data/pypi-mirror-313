from reling.db.models import IdIndex

from reling.db import single_session

__all__ = [
    'find_ids_by_prefix',
]


def find_ids_by_prefix(prefix: str) -> list[str]:
    """Find content IDs that start with the given prefix, ordered by ID."""
    with single_session() as session:
        return [
            result.id
            for result in session.query(IdIndex)
            .where(IdIndex.id.startswith(prefix))
            .order_by(IdIndex.id)
            .all()
        ]
