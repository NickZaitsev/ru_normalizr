"""Russian text normalization library."""

from .options import NormalizeOptions

__all__ = ["NormalizeOptions", "Normalizer", "normalize", "preprocess_text"]
__version__ = "0.1.0"


def normalize(text: str, options: NormalizeOptions | None = None) -> str:
    from .pipeline import normalize as _normalize

    return _normalize(text, options)


def preprocess_text(text: str, options: NormalizeOptions | None = None) -> str:
    from .pipeline import preprocess_text as _preprocess_text

    return _preprocess_text(text, options)


class Normalizer:
    def __new__(cls, *args, **kwargs):  # type: ignore[no-untyped-def]
        from .pipeline import Normalizer as _Normalizer

        return _Normalizer(*args, **kwargs)
