from datetime import (
    date,
)
from pathlib import (
    Path,
)
from unittest.case import (
    TestCase,
)

from edureporter.storage import (
    ReportsStorage,
    get_storage,
)
from testapp.app.reports.simple_report.report import (
    Reporter,
    build_report,
)


class StoragesTestCase(TestCase):
    def test_get_storage(self):
        self.assertIsInstance(get_storage(), ReportsStorage)

    def test_storage_operations(self):
        title = 'SimpleReport'

        storage = get_storage()

        path = Path(build_report(
            provider_params={'date': date.today()},
            builder_params={'title': title}
        ))

        self.assertTrue(storage.exists(path.name))
        self.assertIn(title, path.stem)
        self.assertEqual(Reporter.extension, path.suffix)

        storage.delete(path.name)

        self.assertFalse(storage.exists(path.name))
