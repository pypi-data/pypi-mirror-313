from nanoid import generate

__all__ = [
    'generate_id',
]


def generate_id() -> str:
    """Generate a unique identifier."""
    return generate(size=12)
