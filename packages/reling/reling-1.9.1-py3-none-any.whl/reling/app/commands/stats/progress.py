from typing import Iterable

from tqdm import tqdm

from reling.db.models import DialogueExam, TextExam
from .modalities import Modality

__all__ = [
    'progress',
]


def progress[T](
        iterable: Iterable[T],
        *,
        total: int,
        modality: Modality,
        model: type[TextExam | DialogueExam] | None = None,
) -> Iterable[T]:
    """Display the progress of the given iterable."""
    return tqdm(
        iterable,
        desc=f'Computing {modality.value} stats'
             + (f' for {'texts' if model == TextExam else 'dialogues'}' if model else ''),
        total=total,
        leave=False,
    )
