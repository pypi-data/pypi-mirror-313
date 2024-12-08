from sqlalchemy import and_, ColumnElement

from reling.db.models import DialogueExam, Language, TextExam
from .modalities import Modality

__all__ = [
    'get_filter',
]


def get_filter(
        language: Language,
        paired: list[Language] | None,
        modality: Modality,
        model: type[TextExam | DialogueExam],
) -> ColumnElement[bool]:
    """Get the filtering condition for the given language, paired language(s), modality, and model."""
    main_language_id, secondary_language_id = ((model.source_language_id, model.target_language_id)
                                               if modality == Modality.COMPREHENSION else
                                               (model.target_language_id, model.source_language_id))
    return and_(main_language_id == language.id,
                paired is None or secondary_language_id.in_(language.id for language in paired))
