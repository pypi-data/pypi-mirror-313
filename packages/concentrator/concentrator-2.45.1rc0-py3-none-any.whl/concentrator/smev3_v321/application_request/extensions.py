from .changes import Smev3StorageHelper


def get_storage_helper(*args, **kwargs):
    """Возвращает класс для отслеживания изменений."""

    return Smev3StorageHelper
