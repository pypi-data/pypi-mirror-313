import os
import unittest
from pathlib import (
    Path,
)
from tempfile import (
    NamedTemporaryFile,
)

from simple_report.converter.abstract import (
    FileConverter,
)
from simple_report.report import (
    DocumentReport,
)
from simple_report.rtf.document import (
    DocumentRTF,
)

from .utils import (
    LegacyDocumentComparisonMixin,
)


__author__ = 'khalikov'
TESTS_DIR = Path(__file__).parent


class TestRTF(LegacyDocumentComparisonMixin, unittest.TestCase):
    """Тесты отчетов в формате RTF."""

    # Разные директории с разными файлами под linux и под windows
    # SUBDIR = ''

    def setUp(self):
        self.src_dir = Path(TESTS_DIR, 'test_data', 'rtf')
        self.reference_dir = self.src_dir / 'reference'

        self.test_files = dict(
            [(path, os.path.join(self.src_dir, path)) for path in os.listdir(self.src_dir) if path.startswith('test')]
        )

    # def test_libreoffice_replace(self):
    #    src_file = self.test_files['test_roll.rtf']
    #    dst_file = os.path.join(self.reference_dir, 'res_roll.rtf')
    #
    #    doc = DocumentReport(src_file, wrapper=DocumentRTF, type=FileConverter.RTF)
    #
    #    doc.build(
    #        dst_file,
    #        {'Employee_na32': 'Иванов И.И.',
    #         'region_name': 'Казань',
    #         'test': 'adsgh'},
    #        file_type=FileConverter.RTF
    #    )

    def test_word_replace(self):
        template_name = 'test-sluzh.rtf'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        doc = DocumentReport(src_path, wrapper=DocumentRTF, type=FileConverter.RTF)

        with NamedTemporaryFile(suffix='.rtf') as dst:
            doc.build(
                dst.name,
                {
                    'Employee_name': 'Иванов И.И.',
                    'region_name': 'Казань',
                    'test': 'adsgh',
                },
                file_type=FileConverter.RTF,
            )
            self.assertLegacyDocumentEqual(reference_path, dst.name)
