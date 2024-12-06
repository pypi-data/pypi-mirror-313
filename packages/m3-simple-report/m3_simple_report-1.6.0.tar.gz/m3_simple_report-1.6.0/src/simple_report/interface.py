from abc import (
    ABCMeta,
    abstractmethod,
)
from collections.abc import (
    Mapping,
)

import six


class IReport:
    def show(self, *args, **kwargs):
        """Deprecated: use build."""
        self.build(*args, **kwargs)

    @abstractmethod
    def build(self, *args, **kwargs):
        """Построение отчета."""


class IDocumentReport(six.with_metaclass(ABCMeta, IReport)):
    @abstractmethod
    def build(self, dst_file_path, params, file_type):  # pylint:disable=arguments-differ
        """Генерирует выходной файл в нужном формате.

        :param dst_file_path: путь до выходного файла
        :type dst_file_path: str
        :param params: словарь ключ: параметр в шаблоне,
                       значение: заменяющая строка

        :type params: dict
        :param file_type: тип файла
        :type file_type: str
        """

    @abstractmethod
    def get_all_parameters(self):
        """Возвращает все параметры документа."""


class ISpreadsheetReport(six.with_metaclass(ABCMeta, IReport)):
    @abstractmethod
    def get_sections(self):
        """Возвращает все секции."""

    @abstractmethod
    def get_section(self, section_name):
        """Возвращает секцию по имени.

        :param section_name: имя секции
        :type section_name: str
        """

    @property
    @abstractmethod
    def sections(self):
        """Секции отчета."""

    @property
    @abstractmethod
    def workbook(self):
        """Возвращает объект рабочей книги."""

    @property
    @abstractmethod
    def sheets(self):
        """Возвращает объекты листов."""

    @abstractmethod
    def copy_sheet(self, sheet: 'ISpreadsheetWorkbookSheet', target_sheet_name: str):
        """Копирует лист рабочей книги."""

    @abstractmethod
    def build(self, dst_file_path, file_type):  # pylint:disable=arguments-differ
        """Генерирует выходной файл в нужном формате.

        :param dst_file_path: путь до выходного файла
        :type dst_file_path: str
        :param file_type: тип файла
        :type file_type: str
        """


class ISpreadsheetSection(metaclass=ABCMeta):
    VERTICAL = 0
    HORIZONTAL = 1
    RIGHT_UP = 2
    LEFT_DOWN = 3
    RIGHT = 4
    HIERARCHICAL = 5

    @abstractmethod
    def flush(self, params, oriented=LEFT_DOWN):
        """Записать данные в секцию.

        :param params: словарь параметров
        :type params: dict
        :param oriented: направление вывода секций
        :type oriented: int
        """

    @abstractmethod
    def get_all_parameters(self):
        """Возвращает все параметры секции."""


class ISpreadsheetWorkbookSheet(metaclass=ABCMeta):
    """Лист книги документа."""

    @abstractmethod
    def get_section(self, name: str) -> ISpreadsheetSection:
        """Получение секции по имени."""

    @abstractmethod
    def get_sections(self) -> Mapping[str, ISpreadsheetSection]:
        """Получение всех секций."""

    @abstractmethod
    def get_name(self) -> str:
        """Получение названия листа."""


class ISpreadsheetWorkbook(metaclass=ABCMeta):
    """Рабочая книга документа."""

    @property
    @abstractmethod
    def active_sheet(self) -> ISpreadsheetWorkbookSheet:
        """Активный лист рабочей книги."""

    @active_sheet.setter
    @abstractmethod
    def active_sheet(self, value: int):
        """Установить активный лист по его индексу в книге."""

    @property
    @abstractmethod
    def sheets(self) -> list[ISpreadsheetWorkbookSheet]:
        """Список листов рабочей книги."""

    def get_section(self, name) -> ISpreadsheetSection:
        """Получить секцию активного листа по её имени."""
        return self.active_sheet.get_section(name)

    def get_sections(self) -> Mapping[str, ISpreadsheetSection]:
        """Получить все секции секцию активного листа."""
        return self.active_sheet.get_sections()

    def get_sheet_name(self):
        return self.active_sheet.get_name()

    @abstractmethod
    def copy_sheet(self, sheet: ISpreadsheetWorkbookSheet, target_sheet_name: str) -> ISpreadsheetWorkbookSheet:
        """Копировать лист рабочей книги."""
