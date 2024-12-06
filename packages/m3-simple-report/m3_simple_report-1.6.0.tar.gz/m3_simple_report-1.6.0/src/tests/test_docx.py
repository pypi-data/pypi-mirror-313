import os
import unittest
from contextlib import (
    contextmanager,
)
from pathlib import (
    Path,
)
from tempfile import (
    NamedTemporaryFile,
)
from unittest.mock import (
    patch,
)
from uuid import (
    UUID,
)

from simple_report.docx.drawing import (
    DocxImage,
)
from simple_report.report import (
    DocumentReport,
)
from simple_report.xlsx.spreadsheet_ml import (
    SectionException,
)

from .utils import (
    OfficeOpenXMLDocumentComparisonMixin,
)


LOREM_IPSUM = (
    'Lorem ipsum dolor sit amet, consectetur adipisicing elit, '
    'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
    'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris '
    'nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in '
    'reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla '
    'pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa '
    'qui officia deserunt mollit anim id est laborum.'
)

TESTS_DIR = Path(__file__).parent


class TestLinuxDOCX(OfficeOpenXMLDocumentComparisonMixin, unittest.TestCase):
    SUBDIR = 'linux'

    def setUp(self):
        self.src_dir = Path(TESTS_DIR, 'test_data', self.SUBDIR, 'docx')
        self.reference_dir = self.src_dir / 'reference'

        self.test_files = dict(
            [(path, os.path.join(self.src_dir, path)) for path in os.listdir(self.src_dir) if path.startswith('test')]
        )

        # Фиксированный набор идентификаторов. Эталонные результаты содержат идентификаторы из этого набора.
        self._uuid_list = [
            '2b844a79-c514-422e-afb1-d7830779e532',
            '7fa206e4-7e3f-4d8b-b096-34448e7caeed',
            '6ddfc888-5287-40b8-b669-1f322b4db0fb',
            'fff25923-2ec6-40ed-8458-63f4f0e10ea4',
            '314ae234-7f50-4c35-bc6e-ca5539af737c',
            '28ea4e86-1842-452b-afd0-bb3298579455',
            'b207015e-52c1-491d-b66e-ec028f005495',
            'bbc1af10-5d23-488e-8b3a-8dbc2be2c310',
            '29499d4a-00e1-43ba-a376-e4fe4555a195',
            '5c666ba0-3fd1-4b03-b4b6-87c70bd0401b',
        ]
        self._uuid_iterator = iter(self._uuid_list)

    @contextmanager
    def _patch_uuid4(self):
        """Менеджер контекста, подменяющий uuid4."""
        with patch('uuid.uuid4', return_value=UUID(next(self._uuid_iterator))) as cm:
            yield cm

    def test_simple_docx(self):
        template_name = 'test-sluzh.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        doc = DocumentReport(src_path)

        with NamedTemporaryFile(suffix='.docx') as dst:
            doc.build(dst.name, {'Employee_name': 'Иванова И.И.', 'region_name': 'Казань'})
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_spreadsheet_docx(self):
        """Текст внутри таблицы."""
        template_name = 'test_spreadsheet.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        doc = DocumentReport(src_path)

        tag1 = next(doc.get_all_parameters())
        self.assertEqual(tag1, '#sometext#')

        with NamedTemporaryFile(suffix='.docx') as dst:
            doc.build(dst.name, {'sometext': 'Некий текст'})
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_picture_docx(self):
        """Текст внутри прямоугольника."""
        template_name = 'test_rect.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        with self._patch_uuid4():
            doc = DocumentReport(src_path)

            tags = []
            for tag in doc.get_all_parameters():
                tags.append(tag)

            self.assertFalse(tags[0] != '#brandgroupname#' and tags[0] != '#category#')
            self.assertFalse(tags[1] != '#brandgroupname#' and tags[1] != '#category#')

            with NamedTemporaryFile(suffix='.docx') as dst:
                doc.build(dst.name, {'brandgroupname': 'Брэнд', 'category': 'Категория'})
                self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_picture_shape(self):
        template_name = 'test_pict_shape_2.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = DocumentReport(src_path)
        params = {}

        params['fname'] = '1'
        params['sname'] = '2'
        params['pname'] = '3'
        params['issued_by'] = '4'
        params['date_of_birth'] = '5'

        params['date_start_day'] = '6'
        params['date_start_month'] = '7'
        params['date_start_year'] = '8'
        params['date_start'] = '9'
        params['date_end_day'] = '10'
        params['date_end_month'] = '11'
        params['date_end_year'] = '12'
        params['date_end'] = '13'
        params['region_number'] = '14'
        params['date_start_plus'] = '15'
        params['date_start_plus_day'] = '16'
        params['date_start_plus_month'] = '17'
        params['date_start_plus'] = '18'
        params['date_start_plus_year'] = '19'
        params['habaddr'] = '20'
        params['regaddr1'] = '21'
        params['regaddr2'] = '22'
        params['regaddr3'] = '23'
        params['inspect1'] = '24'
        params['inspect2'] = '25'
        params['is_AI'] = 'AI'
        params['is_AII'] = 'AII'
        params['is_AIII'] = 'AIII'
        params['is_AIV'] = 'AIV'
        params['is_B'] = 'B'
        params['is_C'] = 'C'
        params['is_D'] = 'D'
        params['is_E'] = 'E'
        params['is_F'] = 'F'
        params['#komment#'] = 'd'

        with NamedTemporaryFile(suffix='.docx') as dst:
            report.build(dst.name, params)
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_tables_flush(self):
        template_name = 'test_table.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = DocumentReport(src_path)
        # report.set_docx_table_sections()
        s1 = report.get_section('section1')
        s2 = report.get_section('section2')
        s2.flush({'test': 'Lorem ipsum'})
        s1.flush(
            {
                'test_table_row1col1': 'Hello',
                'test_table_row1col2': 'simple_report',
                'test_table_row1col3': 'user',
                'test_table_row1col4': LOREM_IPSUM,
            }
        )
        params = {}
        with NamedTemporaryFile(suffix='.docx') as dst:
            report.build(dst.name, params)
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_table_section_double(self):
        template_name = 'test_table_double_section.docx'
        src_path = self.test_files[template_name]

        report = DocumentReport(src_path)
        try:
            report.get_section('section1')
        except SectionException:
            pass
        else:
            raise Exception('Docx tables sections doubling test failed')

    def test_divisible_keys(self):
        template_name = 'test_divisibles.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)
        report = DocumentReport(src_path)

        params = {
            'tasks': '',
            'kind_tostring': 'документарная и выездная',
            'normative_list': '',
            'finish_date': '13.12.2012',
            'expert_list': '',
            'docs': '',
            'num': '1',
            'purpose': '',
            'address': '420101, Респ Татарстан (Татарстан), г Казань, ул Карбышева, д. 37, кв. 44',
            'events': '',
            'subject3': 'x',
            'articles': '',
            'inspectors_list': '',
            'supervisionobj_name': 'Малыши и малышки',
            'oyear': 2013,
            'type_tostring': 'внеплановая',
            'start_date': '14.02.2013',
            'subject1': 'x',
            'subject2': 'x',
            'oday': 21,
            'subject4': 'x',
            'subject5': 'x',
            'subject6': 'x',
            'subject7': 'x',
            'authority_parent': '',
            'omonth': 3,
        }
        with NamedTemporaryFile(suffix='.docx') as dst:
            report.build(dst.name, params)
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_flush_order(self):
        template_name = 'test_flush_order.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = DocumentReport(src_path)

        params = {
            'example': 'output_one',
            'example_two': 'ouput_two',
            'example_two_three': 'output_two_three',
            'exampl': 'no_output',
        }
        with NamedTemporaryFile(suffix='.docx') as dst:
            report.build(dst.name, params)
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_tabs(self):
        template_name = 'test_tabs.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = DocumentReport(src_path)

        params = {
            'tfoms_to': 'TFOMS',
            'tfoms_to_address': 'TFOMS_ADDRESS',
            'tfoms_to_director_fio': 'TFOMS_TO_DIR_FIO',
        }
        with NamedTemporaryFile(suffix='.docx') as dst:
            report.build(dst.name, params)
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_insert_picture(self):
        template_name = 'test_insert_image.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        with self._patch_uuid4():
            report = DocumentReport(src_path)
            params = {
                'test': 'Тестовый комментарий',
                'image': DocxImage(self.test_files['test_insert_image.jpg'], 3, 2),
                'tfoms_to_director_fio': 'TFOMS_TO_DIR_FIO',
            }

            with NamedTemporaryFile(suffix='.docx') as dst:
                report.build(dst.name, params)
                self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_table_insert_picture(self):
        template_name = 'test_table.docx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, 'test_table_insert_picture.docx')

        with self._patch_uuid4():
            report = DocumentReport(src_path)
            # report.set_docx_table_sections()
            s1 = report.get_section('section1')
            s2 = report.get_section('section2')
            s2.flush({'test': DocxImage(self.test_files['test_insert_image.jpg'], 3, 2)})
            s1.flush(
                {
                    'test_table_row1col1': 'Hello',
                    'test_table_row1col2': 'simple_report',
                    'test_table_row1col3': DocxImage(self.test_files['test_table_image.gif'], 3.5, 2.5),
                    'test_table_row1col4': LOREM_IPSUM,
                }
            )
            params = {}

            with NamedTemporaryFile(suffix='.docx') as dst:
                report.build(dst.name, params)
                self.assertOfficeOpenXMLEqual(reference_path, dst.name)
