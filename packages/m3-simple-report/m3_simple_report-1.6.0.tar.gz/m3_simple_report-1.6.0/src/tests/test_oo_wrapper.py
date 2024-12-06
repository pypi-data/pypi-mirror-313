import os
from contextlib import (
    suppress,
)
from unittest import (
    skipUnless,
)

from simple_report.converter.abstract import (
    FileConverter,
)
from simple_report.report import (
    SpreadsheetReport,
)
from simple_report.xlsx.section import (
    Section,
)


OO_PORT = 2002

UNO_INSTALLED = False
OO_LISTENS = False

with suppress(ImportError):
    from simple_report.converter.open_office import (
        OOWrapper,
        OpenOfficeConverter,
    )
    from simple_report.converter.open_office.wrapper import (
        OOWrapperException,
    )

    UNO_INSTALLED = True


with suppress(OOWrapperException, ModuleNotFoundError):
    OOWrapper(OO_PORT)
    OO_LISTENS = True


class TestOO:
    @skipUnless(UNO_INSTALLED, 'Не установлен пакет python-uno')
    @skipUnless(OO_LISTENS, f'OpenOffice не слушает на порту {OO_PORT}')
    def test_oo_wrapper(self):
        """Тестирование OpenOffice конвертера."""
        src = self.test_files['test-PF_PKO.xlsx']

        converter = OOWrapper()
        file_path = converter.convert(
            src,
            'xls',
        )
        self.assertEqual(os.path.exists(file_path), True)

        with self.assertRaises(OOWrapperException):
            converter.convert(src, 'odt')  # Для Writera

    @skipUnless(UNO_INSTALLED, 'Не установлен пакет python-uno')
    @skipUnless(OO_LISTENS, f'OpenOffice не слушает на порту {OO_PORT}')
    def test_oo_wrapper_xls_to_xlsx(self):
        """Тестирование OpenOffice конвертера."""
        src = self.test_files['test-simple-converter.xls']

        dst = os.path.join(self.reference_dir, 'convert-simple-too.xlsx')

        converter = OOWrapper(OO_PORT)
        file_path = converter.convert(src, 'xlsx', dst)
        self.assertEqual(os.path.exists(file_path), True)

    @skipUnless(UNO_INSTALLED, 'Не установлен пакет python-uno')
    @skipUnless(OO_LISTENS, f'OpenOffice не слушает на порту {OO_PORT}')
    def test_work_document(self):
        #        with self.assertRaises(FileConverterException):
        #            src = self.test_files['test-simple-converter.xls']
        #            report = SpreadsheetReport(src, converter=OpenOfficeConverter(port=8100))

        src = self.test_files['test-simple-converter.xls']
        report = SpreadsheetReport(src, converter=OpenOfficeConverter(port=OO_PORT))
        dst = os.path.join(self.reference_dir, 'convert-simple.xlsx')

        if os.path.exists(dst):
            os.remove(dst)
        self.assertEqual(os.path.exists(dst), False)

        self.assertGreater(len(report._wrapper.sheets), 0)
        self.assertLessEqual(len(report._wrapper.sheets), 4)

        self.assertNotEqual(report._wrapper.workbook, None)
        self.assertNotEqual(report._wrapper.workbook.shared_strings, None)

        # Тестирование получения секции
        section_a1 = report.get_section('A1')
        self.assertIsInstance(section_a1, Section)

        with self.assertRaises(Exception):
            report.get_section('G1')

        section_a1.flush({'user': 'Иванов Иван', 'date_now': 1})
        for i in range(10):
            report.get_section('B1').flush({'nbr': i, 'fio': 'Иванов %d' % i})

        report.get_section('C1').flush({'user': 'Иван'})
        report.build(dst, FileConverter.XLS)

        self.assertEqual(os.path.exists(dst), True)
