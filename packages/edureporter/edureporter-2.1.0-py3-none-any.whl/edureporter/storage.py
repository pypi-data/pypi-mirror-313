# pylint: disable=import-outside-toplevel
from django.conf import (
    settings,
)
from django.core.files.storage import (
    FileSystemStorage,
)


REPORTS_STORAGE_ALIAS = 'reports'


class ReportsStorage(FileSystemStorage):

    def __init__(self, *args, location=None, base_url=None, **kwargs):
        if location is None:
            location = settings.REPORTS_DIR

        if base_url is None:
            base_url = settings.REPORTS_URL

        super().__init__(*args, location=location, base_url=base_url, **kwargs)


def get_storage():
    """Получение хранилища под разные версии Django."""
    try:
        from django.core.files.storage import (
            storages,
        )
        storage = storages[REPORTS_STORAGE_ALIAS]

    except ImportError:
        from django.core.files.storage import (
            get_storage_class,
        )
        storage = get_storage_class('edureporter.storage.ReportsStorage')()

    return storage
