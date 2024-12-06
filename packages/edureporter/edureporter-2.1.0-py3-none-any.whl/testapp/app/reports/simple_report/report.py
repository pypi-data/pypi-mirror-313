import datetime
from typing import (
    TYPE_CHECKING,
    Optional,
)

from edureporter import (
    AbstractDataProvider,
    AbstractReportBuilder,
)
from edureporter.reporter import (
    SimpleReporter,
)


if TYPE_CHECKING:
    from simple_report.report import (
        Report,
    )


class Provider(AbstractDataProvider):

    date: datetime.date

    def init(self, **params):
        self.date = params['date']

    def load_data(self):
        return {'date': self.date}


class Builder(AbstractReportBuilder):

    def __init__(self, provider: Provider, report: 'Report', *args, **kwargs):
        self._provider = provider
        self._report = report

    def build(self):
        self._flush_header()

    def _flush_header(self):
        self._flush_section('header', {
            'build_date': datetime.date.today().strftime('%d.%m.%Y'),
            'date': self._provider.date.strftime('%d.%m.%Y'),
        })

    def _flush_section(self, name: str, params: dict):
        self._report.get_section(name).flush(params)


class Reporter(SimpleReporter):

    extension = '.xlsx'
    builder_class = Builder
    data_provider_class = Provider


def build_report(
    provider_params: Optional[dict] = None,
    builder_params: Optional[dict] = None,
    **kwargs
) -> str:
    return Reporter(provider_params or {}, builder_params or {}).make_report()
