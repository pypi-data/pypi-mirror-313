import abc
import os

import six

from simple_report.converter.abstract import (
    FileConverter,
)
from simple_report.core.document_wrap import (
    BaseDocument,
    SpreadsheetDocument,
)
from simple_report.core.exception import (
    WrongDocumentType,
)
from simple_report.core.tags import (
    TemplateTags,
)
from simple_report.docx.document import (
    DocumentDOCX,
)
from simple_report.interface import (
    IDocumentReport,
    ISpreadsheetReport,
    ISpreadsheetWorkbookSheet,
)
from simple_report.rtf.document import (
    DocumentRTF,
)
from simple_report.utils import (
    ColumnHelper,
    FileProxy,
)
from simple_report.xls.document import (
    DocumentXLS,
)
from simple_report.xls.output_options import (
    XSL_OUTPUT_SETTINGS,
)
from simple_report.xlsx.document import (
    DocumentXLSX,
)


class ReportGeneratorException(Exception):
    """Исключение при генерации отчета."""


class Report(six.with_metaclass(abc.ABCMeta)):
    """Абстрактный класс отчета."""

    # pylint:disable-next=redefined-builtin,too-many-arguments,too-many-positional-arguments
    def __init__(self, src_file, converter=None, tags=None, wrapper=None, type=None, **kwargs):
        """Инициализация отчёта.

        :param src_file: путь до файла с шаблоном
        :type src_file: basestring
        :param converter: конвертор
        :type converter:
        :param tags: теги
        :type tags:
        :param wrapper: обертка над форматом отчета
        :type wrapper: type (class)
        :param type: тип отчета
        :type type: str
        """
        self.TYPE = type

        self.tags = tags or TemplateTags()
        assert isinstance(self.tags, TemplateTags)

        self.file = FileProxy(src_file)

        self.converter = None
        if converter is not None:
            assert isinstance(converter, FileConverter)
            self.converter = converter

        ffile = self.convert(self.file, self.TYPE)

        assert issubclass(wrapper, BaseDocument)
        self._wrapper = wrapper(ffile, self.tags, **kwargs)

    def convert(self, src_file, to_format):
        """Преобразование файла в определенный формат.

        :param src_file: исходный файл
        :type src_file: FileProxy
        :param to_format: формат, в который конвертируем
        :type to_format: str
        """
        if self.converter is not None:
            self.converter.set_src_file(src_file)
            return FileProxy(self.converter.build(to_format))
        return src_file

    def build(self, dst_file_path, file_type=None):
        """Построение отчета.

        Параметр `file_type` используется для конвертации полученного xlsx файла в нужный формат.

        :param dst_file_path: Путь до выходного файла
        :type dst_file_path: basestring
        :param file_type: тип файла
        :type file_type: str
        """
        assert self.TYPE, 'Document Type is not defined'

        if file_type is None:
            file_type = self.TYPE

        if self.converter is None and file_type != self.TYPE:
            raise ReportGeneratorException('Converter is not defined')

        file_name, _file_extension = os.path.splitext(dst_file_path)

        xlsx_path = os.path.extsep.join((file_name, self.TYPE))
        xlsx_file = FileProxy(xlsx_path, new_file=True)

        # Всегда вернет файл с расширением open office (xlsx, docx, etc.)

        self._wrapper.build(xlsx_file)

        if file_type == self.TYPE:
            return xlsx_path
        return self.convert(xlsx_file, file_type)


class DocumentReport(Report, IDocumentReport):
    """Отчет в форматах DOCX, RTF."""

    def __init__(  # pylint:disable=too-many-arguments,too-many-positional-arguments
        self,
        src_file,
        converter=None,
        tags=None,
        wrapper=DocumentDOCX,
        type=FileConverter.DOCX,  # pylint:disable=redefined-builtin
    ):
        assert issubclass(wrapper, DocumentDOCX) or issubclass(wrapper, DocumentRTF), 'wrong wrapper type'
        assert type in (FileConverter.DOCX, FileConverter.RTF)

        super().__init__(src_file, converter, tags, wrapper, type)

    def build(self, dst_file_path, params, file_type=FileConverter.DOCX):
        """Генерирует выходной файл в нужном формате.

        :param dst_file_path: Путь до выходного файла
        :type dst_file_path: basestring
        :param params: словарь с ключом - параметром шаблона,
                значением - заменяемой строкой
        :type params: dict
        :param file_type: тип файла
        :type file_type: str, FileConverter.*
        """
        self._wrapper.set_params(params)
        return super().build(dst_file_path, file_type)

    def get_all_parameters(self):
        """Возвращает параметры отчета."""
        return self._wrapper.get_all_parameters()

    def get_section(self, section_name):
        """Получение секции.

        :param section_name: имя секции таблицы
        :type section_name: str
        """
        return self._wrapper.get_section(section_name)


class SpreadsheetReport(Report, ISpreadsheetReport):
    """Отчет в форматах XSLX, XLS."""

    _wrapper: SpreadsheetDocument

    def __init__(  # pylint:disable=too-many-arguments,too-many-positional-arguments
        self,
        src_file,
        converter=None,
        tags=None,
        wrapper=DocumentXLSX,
        type=FileConverter.XLSX,  # pylint:disable=redefined-builtin
        **kwargs,
    ):
        """Инициализация отчёта в форматах XLSX, XLS.

        :param src_file: путь до исходного файла
        :type src_file: str
        :param converter: конвертор
        :type converter:
        :param tags: теги
        :type tags:
        :param wrapper: обертка над форматом отчета
        :type wrapper: core.document_wrap.SpreadsheetDocument
        :param type: тип документа
        :type type: str, FileConverter.*
        """
        assert issubclass(wrapper, DocumentXLSX) or issubclass(wrapper, DocumentXLS)
        assert type in (FileConverter.XLSX, FileConverter.XLS)

        super().__init__(src_file, converter, tags, wrapper, type, **kwargs)

    @property
    def sections(self):
        """Секции отчета."""
        return self.get_sections()

    def get_sections(self):
        """Возвращает все секции."""
        return self._wrapper.get_sections()

    def get_section(self, section_name):
        """Возвращает секцию по имени.

        :param section_name: имя секции
        :type section_name: basestring
        """
        if not hasattr(self._wrapper, 'get_section'):
            raise WrongDocumentType()
        return self._wrapper.get_section(section_name)

    def build(self, *args, **kwargs):
        """Дополнительные действия перед построением отчета."""
        self._reset_caches()

        return super().build(*args, **kwargs)

    def _reset_caches(self):
        """Сброс кэшей."""
        ColumnHelper.reset_caches()

    @property
    def workbook(self):
        """Возвращает объект рабочей книги XLS(X)."""
        return self._wrapper.workbook

    @property
    def sheets(self):
        """Возвращает объекты листов XLS(X)."""
        return self._wrapper.sheets

    @property
    def active_sheet(self) -> ISpreadsheetWorkbookSheet:
        """Активный лист рабочей книги."""
        return self._wrapper.active_sheet

    @active_sheet.setter
    def active_sheet(self, value: int):
        """Установить активный лист по его индексу в книге."""
        self._wrapper.active_sheet = value

    def copy_sheet(self, sheet: 'ISpreadsheetWorkbookSheet', target_sheet_name: str) -> ISpreadsheetWorkbookSheet:
        """Копирует лист рабочей книги."""
        return self._wrapper.copy_sheet(sheet=sheet, target_sheet_name=target_sheet_name)

    def __setattr__(self, key, value):
        if key in XSL_OUTPUT_SETTINGS:
            setattr(self._wrapper, key, value)
        else:
            super().__setattr__(key, value)
