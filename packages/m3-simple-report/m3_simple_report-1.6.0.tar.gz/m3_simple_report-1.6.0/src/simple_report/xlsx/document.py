

from simple_report.core.document_wrap import (
    DocumentOpenXML,
    SpreadsheetDocument,
)
from simple_report.xlsx.spreadsheet_ml import (
    CommonPropertiesXLSX,
    Workbook,
)


class DocumentXLSX(DocumentOpenXML, SpreadsheetDocument):
    """Обертка для работы с форматом XLSX."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.common_properties = CommonPropertiesXLSX.create(self.extract_folder, self._tags)

    @property
    def workbook(self) -> Workbook:
        """Книга для таблицы."""
        return self.common_properties.main

    def build(self, dst_file):
        """Сохранение отчета в файл.

        :param dst_file: путь до выходного файла
        :type dst_file: str
        """
        self.workbook.build()
        super().build(dst_file)
