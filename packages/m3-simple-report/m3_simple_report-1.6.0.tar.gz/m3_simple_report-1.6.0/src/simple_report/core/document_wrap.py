from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
)

import six

from simple_report.utils import (
    ZipProxy,
)


if TYPE_CHECKING:
    from simple_report.interface import (
        ISpreadsheetWorkbook,
        ISpreadsheetWorkbookSheet,
    )


class BaseDocument(metaclass=ABCMeta):
    """Базовый класс для всех документов."""

    @abstractmethod
    def build(self, dst):
        """Сборка документа.

        :result:
        """


class SpreadsheetDocument(metaclass=ABCMeta):
    @property
    @abstractmethod
    def workbook(self) -> 'ISpreadsheetWorkbook':
        """Рабочая книга."""

    @property
    def active_sheet(self) -> 'ISpreadsheetWorkbookSheet':
        """Активный лист рабочей книги."""
        return self.workbook.active_sheet

    @active_sheet.setter
    def active_sheet(self, value: int):
        """Установить активный лист по его индексу в книге."""
        self.workbook.active_sheet = value

    def get_sections(self):
        """Возвращает все секции в активной странице шаблона."""
        return self.workbook.get_sections()

    def get_section(self, name):
        """Возвращает секцию по названию шаблона."""
        return self.workbook.get_section(name)

    @property
    def sheets(self) -> list['ISpreadsheetWorkbookSheet']:
        """Листы отчета."""
        return self.workbook.sheets

    def copy_sheet(self, sheet: 'ISpreadsheetWorkbookSheet', target_sheet_name: str) -> 'ISpreadsheetWorkbookSheet':
        """Копирует лист отчёта."""
        return self.workbook.copy_sheet(sheet, target_sheet_name)


class DocumentOpenXML(six.with_metaclass(ABCMeta, BaseDocument)):
    """Базовый класс для работы со структурой open xml."""

    def __init__(self, src_file, tags):
        self.extract_folder = ZipProxy.extract(src_file)

        self._tags = tags  # Ссылка на тэги

    def build(self, dst_file):
        """Сборка отчета."""
        ZipProxy.pack(dst_file, self.extract_folder)
