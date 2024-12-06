from simple_report.converter.abstract import (
    FileConverter,
)
from simple_report.converter.open_office.wrapper import (
    OOWrapper,
)


class OpenOfficeConverter(FileConverter):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def convert(self, to_format):
        """Конвертирует документ в целевой формат.

        Метод должен исходя из исходного типа документа и требуемого типа
        найти метод у себя и вызвать его. Если этого метода нет - должно
        генериться исключение.
        """
        #        if to_format in (FileConverter.XLSX, FileConverter.DOCX):
        #            raise FileConverterException('Format "%s" not supported' % to_format)
        return OOWrapper(self.port).convert(self.file.get_path(), to_format)
