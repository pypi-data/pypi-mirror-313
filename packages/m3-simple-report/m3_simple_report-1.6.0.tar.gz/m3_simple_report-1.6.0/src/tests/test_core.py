import os
import unittest
from datetime import (
    datetime,
)
from pathlib import (
    Path,
)
from tempfile import (
    NamedTemporaryFile,
)

from freezegun import (
    freeze_time,
)

from simple_report.converter.abstract import (
    FileConverter,
)
from simple_report.core.tags import (
    TemplateTags,
)
from simple_report.interface import (
    ISpreadsheetSection,
)
from simple_report.report import (
    ReportGeneratorException,
    SpreadsheetReport,
)
from simple_report.utils import (
    ColumnHelper,
    FormulaWriteExcel,
    date_to_float,
)
from simple_report.xls.document import (
    DocumentXLS,
)
from simple_report.xls.section import (
    MergeXLS,
    XLSImage,
)
from simple_report.xlsx.formula import (
    Formula,
)
from simple_report.xlsx.section import (
    MergeXLSX,
    Section,
    simple_merge_cells,
)
from simple_report.xlsx.spreadsheet_ml import (
    SectionException,
    SectionNotFoundException,
)

from .oborot import (
    OperationsJournalReportFactory,
)
from .test_oo_wrapper import (
    TestOO,
)
from .test_pagebreaks import (
    TestPagebreaks,
)
from .test_pko import (
    TestPKO,
)
from .utils import (
    LegacyDocumentComparisonMixin,
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

_frozen_time = '2024-10-21'
TESTS_DIR = Path(__file__).parent


class TestXLSXMixin(OfficeOpenXMLDocumentComparisonMixin):
    maxDiff = None

    # Разные директории с разными файлами под linux и под windows
    SUBDIR = None

    def setUp(self):
        assert self.SUBDIR

        self.src_dir = Path(TESTS_DIR, 'test_data', self.SUBDIR, 'xlsx')
        self.reference_dir = self.src_dir / 'reference'

        self.test_files = dict(
            [(path, os.path.join(self.src_dir, path)) for path in os.listdir(self.src_dir) if path.startswith('test')]
        )

    def test_range_cols(self):
        section_range = list(ColumnHelper.get_range(('ALC'), ('AVB')))
        self.assertIn('ALC', section_range)
        self.assertIn('AVB', section_range)
        self.assertIn('AVA', section_range)
        self.assertNotIn('ALA', section_range)
        self.assertNotIn('AVC', section_range)

        section_range = list(ColumnHelper.get_range(('X'), ('AB')))
        self.assertIn('X', section_range)
        self.assertIn('Y', section_range)
        self.assertIn('AA', section_range)
        self.assertNotIn('Q', section_range)
        self.assertNotIn('AC', section_range)
        self.assertEqual(len(section_range), 5)

        section_range = list(ColumnHelper.get_range(('B'), ('CBD')))
        self.assertIn('B', section_range)
        self.assertIn('C', section_range)
        self.assertIn('AAA', section_range)
        self.assertIn('ZZ', section_range)
        self.assertIn('ABA', section_range)
        self.assertIn('CBD', section_range)
        self.assertIn('CAA', section_range)
        self.assertIn('BZZ', section_range)
        self.assertNotIn('CBE', section_range)

        section_range = list(ColumnHelper.get_range(('BCCC'), ('BCCD')))
        self.assertIn('BCCC', section_range)
        self.assertIn('BCCD', section_range)
        self.assertNotIn('A', section_range)
        self.assertNotIn('BCCE', section_range)
        self.assertEqual(len(section_range), 2)

    def test_workbook(self):
        template_name = 'test-simple.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path, tags=TemplateTags(test_tag=222))

        # self.assertGreater(len(report._wrapper.sheets), 0)

        self.assertNotEqual(report._wrapper.workbook, None)
        self.assertNotEqual(report._wrapper.workbook.shared_strings, None)

        # Тестирование получения секции
        section_a1 = report.get_section('A1')
        self.assertIsInstance(section_a1, Section)

        with self.assertRaises(SectionNotFoundException):
            report.get_section('G1')

        section_a1.flush({'user': 'Иванов Иван', 'date_now': 1})

        s_gor = report.get_section('GOR')
        s_gor.flush({'col': 'Данные'}, oriented=s_gor.HORIZONTAL)

        for i in range(10):
            report.get_section('B1').flush({'nbr': i, 'fio': 'Иванов %d' % i, 'sector': 'Какой-то сектор'})

            s_gor_str = report.get_section('GorStr')
            s_gor_str.flush({'g': i + i}, oriented=s_gor.HORIZONTAL)
            s_gor_str.flush({'g': i * i}, oriented=s_gor.HORIZONTAL)

        report.get_section('C1').flush({'user': 'Иван'})

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            with self.assertRaises(ReportGeneratorException):
                report.build(dst.name, FileConverter.XLS)

            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)


@freeze_time(_frozen_time)
class TestLinuxXLSX(TestXLSXMixin, TestOO, TestPKO, TestPagebreaks, unittest.TestCase):
    SUBDIR = 'linux'

    def test_fake_section(self):
        src = self.test_files['test-simple-fake-section.xlsx']
        with self.assertRaises(SectionException):
            report = SpreadsheetReport(src)
            report.build(src)

    def test_merge_cells(self):
        template_name = 'test-merge-cells.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)

        report.get_section('head').flush({'kassa_za': 'Ноябрь'})

        for i in range(10):
            report.get_section('table_dyn').flush({'doc_num': i})

        report.get_section('foot').flush({'glavbuh': 'Иван'})

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_formula_generation(self):
        template_name = 'test-formula_generation.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)

        all_change = report.get_section('all_change')
        all_not_change = report.get_section('all_not_change')
        row_not_change = report.get_section('row_not_change')
        column_not_change = report.get_section('column_not_change')
        other_section = report.get_section('other_section')
        row_insert_formula_section = report.get_section('row_insert_formula')
        check_insert_formula_section = report.get_section('check_insert_formula')

        all_change_formula = '(A1+B1)*3'
        all_not_change_formula = '($A$1+B1)*3'
        row_not_change_formula = '(A$1+B1)*3'
        column_not_change_formula = '($A1+B1)*3'

        all_change.flush({'p1': 1, 'p2': 1}, oriented=ISpreadsheetSection.VERTICAL)
        all_change.flush({'p1': 2, 'p2': 2}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(all_change_formula).formula, '(A2+B2)*3')
        other_section.flush({'p1': 1}, oriented=ISpreadsheetSection.VERTICAL)
        all_change.flush({'p1': 3, 'p2': 3}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(all_change_formula).formula, '(A4+B4)*3')

        other_section.flush({'p1': 1}, oriented=ISpreadsheetSection.VERTICAL)
        all_not_change.flush({'p1': 1, 'p2': 1}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(all_not_change_formula).formula, '($A$1+B1)*3')
        all_not_change.flush({'p1': 2, 'p2': 2}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(all_not_change_formula).formula, '($A$1+B2)*3')
        other_section.flush({'p1': 1}, oriented=ISpreadsheetSection.VERTICAL)
        all_not_change.flush({'p1': 3, 'p2': 3}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(all_not_change_formula).formula, '($A$1+B4)*3')

        other_section.flush({'p1': 1}, oriented=ISpreadsheetSection.VERTICAL)
        row_not_change.flush({'p1': 1, 'p2': 1}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(row_not_change_formula).formula, '(A$1+B1)*3')
        row_not_change.flush({'p1': 2, 'p2': 2}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(row_not_change_formula).formula, '(A$1+B2)*3')
        other_section.flush({'p1': 1}, oriented=ISpreadsheetSection.VERTICAL)
        row_not_change.flush({'p1': 3, 'p2': 3}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(row_not_change_formula).formula, '(A$1+B4)*3')

        other_section.flush({'p1': 1}, oriented=ISpreadsheetSection.VERTICAL)
        column_not_change.flush({'p1': 1, 'p2': 1}, oriented=ISpreadsheetSection.VERTICAL)
        self.assertEqual(Formula.get_instance(column_not_change_formula).formula, '($A1+B1)*3')
        other_section.flush({'p1': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
        column_not_change.flush({'p1': 2, 'p2': 2}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(Formula.get_instance(column_not_change_formula).formula, '($A1+F1)*3')
        other_section.flush({'p1': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
        column_not_change.flush({'p1': 3, 'p2': 3}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(Formula.get_instance(column_not_change_formula).formula, '($A1+J1)*3')

        insert_formulas(row_insert_formula_section, check_insert_formula_section)
        # Проверяем, что вписанные формулы попали в дерево и правильно
        # записались
        found_B21 = found_C21 = False
        for row in report.sheets[0].sheet_data.write_data.getchildren():
            if row.tag == 'row':
                for c_ in row.getchildren():
                    if c_.tag == 'c':
                        if c_.attrib.get('r') == 'B21':
                            found_B21 = True
                            func = c_.find('f')
                            assert func is not None
                            assert func.text == 'AVERAGE(B17:B20)'
                        elif c_.attrib.get('r') == 'C21':
                            found_C21 = True
                            func = c_.find('f')
                            assert func is not None
                            assert func.text == 'SUM((A17,A18,A19,A20))'
        assert found_B21 and found_C21

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_with_merge(self):
        """Конструкция with merge для обьединения ячеек вывода."""
        template_name = 'test-merge.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)
        s1 = report.get_section('s1')
        s2 = report.get_section('s2')
        s3 = report.get_section('s3')
        s4 = report.get_section('s4')
        s5 = report.get_section('s5')

        s5.flush({'p5': 1}, oriented=ISpreadsheetSection.VERTICAL)
        s5.flush({'p5': 2}, oriented=ISpreadsheetSection.VERTICAL)
        s5.flush({'p5': 3}, oriented=ISpreadsheetSection.HORIZONTAL)

        m1 = MergeXLSX(s1, s2, {'p1': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
        with m1:
            with MergeXLSX(s2, s3, {'p21': 1, 'p22': 21}, oriented=ISpreadsheetSection.HORIZONTAL):
                m3 = MergeXLSX(s3, s4, {'p3': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
                with m3:
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    for i in range(2, 4):
                        s4.flush({'p4': i}, oriented=ISpreadsheetSection.VERTICAL)

                m3_exp = (
                    m3._begin_merge_col == 'J'
                    and m3._end_merge_col == 'J'
                    and m3.begin_row_merge == 4
                    and m3.end_row_merge == 6
                )
                self.assertEqual(m3_exp, True)

                with MergeXLSX(s3, s4, {'p3': 2}, oriented=ISpreadsheetSection.HIERARCHICAL):
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    s4.flush({'p4': 2}, oriented=ISpreadsheetSection.VERTICAL)

            with MergeXLSX(s2, s3, {'p21': 2, 'p22': 21}, oriented=ISpreadsheetSection.HIERARCHICAL):
                with MergeXLSX(s3, s4, {'p3': 1}, oriented=ISpreadsheetSection.HORIZONTAL):
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    s4.flush({'p4': 2}, oriented=ISpreadsheetSection.VERTICAL)

        m1_exp = (
            m1._begin_merge_col == 'G'
            and m1._end_merge_col == 'G'
            and m1.begin_row_merge == 4
            and m1.end_row_merge == 10
        )
        self.assertEqual(m1_exp, True)

        with MergeXLSX(s1, s2, {'p1': 2}, oriented=ISpreadsheetSection.HIERARCHICAL):
            with MergeXLSX(s2, s3, {'p21': 1, 'p22': 21}, oriented=ISpreadsheetSection.HORIZONTAL):
                with MergeXLSX(s3, s4, {'p3': 1}, oriented=ISpreadsheetSection.HORIZONTAL):
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.HORIZONTAL)

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_383_value(self):
        template_name = 'test-383.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)

        report.get_section('header').flush({'period': 'Ноябрь'})

        for i in range(10):
            report.get_section('row').flush({'begin_year_debet': -i})

        report.get_section('footer').flush({'glavbuh': 'Иван'})

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_main_parameters(self):
        template_name = 'test-main_book.xlsx'
        src_path = self.test_files[template_name]

        report = SpreadsheetReport(src_path)

        params_header = list(report.get_section('header').get_all_parameters())
        self.assertEqual(0, len(params_header))

        params_row = list(report.get_section('row').get_all_parameters())
        self.assertEqual(13, len(params_row))
        self.assertIn('#num#', params_row)
        self.assertIn('#account_name#', params_row)
        self.assertIn('#journal_num#', params_row)

        params_footer = list(report.get_section('footer').get_all_parameters())
        self.assertEqual(12, len(params_footer))
        self.assertIn('#begin_year_debet_sum#', params_footer)
        self.assertIn('#glavbuh#', params_footer)
        self.assertIn('#username#', params_footer)

    def test_empty_cell(self):
        template_name = 'test-empty-section.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)

        header = report.get_section('row')

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 2))
        self.assertEqual(header.sheet_data.cursor.column, ('B', 1))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 2))
        self.assertEqual(header.sheet_data.cursor.column, ('C', 1))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 2))
        self.assertEqual(header.sheet_data.cursor.column, ('D', 1))

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 3))
        self.assertEqual(header.sheet_data.cursor.column, ('B', 2))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 3))
        self.assertEqual(header.sheet_data.cursor.column, ('C', 2))

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 4))
        self.assertEqual(header.sheet_data.cursor.column, ('B', 3))

        # result_file, result_url = create_office_template_tempnames(template_name)
        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_wide_cell_1(self):
        template_name = 'test-wide-section-1.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)
        report = SpreadsheetReport(src_path)

        header = report.get_section('row')

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 2))
        self.assertEqual(header.sheet_data.cursor.column, ('B', 1))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 2))
        self.assertEqual(header.sheet_data.cursor.column, ('C', 1))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 2))
        self.assertEqual(header.sheet_data.cursor.column, ('D', 1))

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 3))
        self.assertEqual(header.sheet_data.cursor.column, ('B', 2))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 3))
        self.assertEqual(header.sheet_data.cursor.column, ('C', 2))

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 4))
        self.assertEqual(header.sheet_data.cursor.column, ('B', 3))

        # result_file, result_url = create_office_template_tempnames(template_name)
        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_wide_cell_2(self):
        template_name = 'test-wide-section-2.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)
        report = SpreadsheetReport(src_path)

        header = report.get_section('row')

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 4))
        self.assertEqual(header.sheet_data.cursor.column, ('D', 1))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 4))
        self.assertEqual(header.sheet_data.cursor.column, ('G', 1))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 4))
        self.assertEqual(header.sheet_data.cursor.column, ('J', 1))

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 7))
        self.assertEqual(header.sheet_data.cursor.column, ('D', 4))

        header.flush({}, oriented=ISpreadsheetSection.HORIZONTAL)
        self.assertEqual(header.sheet_data.cursor.row, ('A', 7))
        self.assertEqual(header.sheet_data.cursor.column, ('G', 4))

        header.flush({})
        self.assertEqual(header.sheet_data.cursor.row, ('A', 10))
        self.assertEqual(header.sheet_data.cursor.column, ('D', 7))

        # result_file, result_url = create_office_template_tempnames(template_name)
        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_without_merge_cells(self):
        template_name = 'test-main_template.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)

        head_section = report.get_section('head')
        for head in range(10):
            head_section.flush({'head_name': str(head)}, 1)

        # result_file, result_url = create_office_template_tempnames(template_name)
        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_purchases_book(self):
        enterprise_name = 'Мегаэнтерпрайз'
        inn = 123123123
        kpp = 123123
        date_start = datetime.now()
        date_end = datetime.now()

        template_name = 'test-purchases_book.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)
        report = SpreadsheetReport(src_path)

        header = report.get_section('header')
        header.flush(
            {
                'enterprise_name': enterprise_name,
                'inn': inn,
                'kpp': kpp,
                'date_start': date_start,
                'date_end': date_end,
            }
        )

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_operations_journal(self):
        template_name = 'test-operations_journal.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = OperationsJournalReportFactory(src_path).generate()

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_cursor(self):
        """Правильность вычисления курсора."""
        template_name = 'test-simple.xlsx'
        src_path = self.test_files[template_name]

        report = SpreadsheetReport(src_path, tags=TemplateTags(test_tag=222))

        section_a1 = report.get_section('A1')
        section_a1.flush({'user': 'Иванов Иван', 'date_now': 1})

        # Проверяем курсор для колонки
        self.assertEqual(section_a1.sheet_data.cursor.row, ('A', 5))
        # Проверяем курсор для строки
        self.assertEqual(section_a1.sheet_data.cursor.column, ('D', 1))

        s_gor = report.get_section('GOR')
        s_gor.flush({'col': 'Данные'}, oriented=s_gor.HORIZONTAL)

        # Проверяем курсор для колонки
        self.assertEqual(s_gor.sheet_data.cursor.row, ('A', 5))
        # Проверяем курсор для строки
        self.assertEqual(s_gor.sheet_data.cursor.column, ('E', 1))

        for i in range(10):
            report.get_section('B1').flush({'nbr': i, 'fio': 'Иванов %d' % i, 'sectior': 'Какой-то сектор'})

            self.assertEqual(s_gor.sheet_data.cursor.row, ('A', i + 6))
            self.assertEqual(s_gor.sheet_data.cursor.column, ('D', i + 5))

            s_gor_str = report.get_section('GorStr')
            s_gor_str.flush({'g': i + 1}, oriented=s_gor.HORIZONTAL)

            self.assertEqual(s_gor.sheet_data.cursor.row, ('A', i + 6))
            self.assertEqual(s_gor.sheet_data.cursor.column, ('E', i + 5))

            s_gor_str.flush({'g': i * i}, oriented=s_gor.HORIZONTAL)

            self.assertEqual(s_gor.sheet_data.cursor.row, ('A', i + 6))
            self.assertEqual(s_gor.sheet_data.cursor.column, ('F', i + 5))

        section_last = report.get_section('C1')
        section_last.flush({'user': 'Иван'})
        self.assertEqual(section_last.sheet_data.cursor.row, ('A', 16))
        self.assertEqual(section_last.sheet_data.cursor.column, ('D', 15))

    def test_copy_sheet(self):
        """Проверяет копирование листа."""
        template_name = 'test-copy_sheet.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)

        # заполнение нулевого листа данными
        report.active_sheet = 0
        report.get_section('header').flush({'title': 'Отчёт по отчётам'})

        template_sheet_index = 1
        for sheet_num in range(3):
            target_sheet_name = f'Копия листа-шаблона №{sheet_num}'
            copied_sheet = report.copy_sheet(report.sheets[template_sheet_index], target_sheet_name)
            self.assertIn(copied_sheet, report.sheets)

            # заполнение скопированного листа данными
            self.assertEqual(target_sheet_name, copied_sheet.name)
            report.active_sheet = report.sheets.index(copied_sheet)
            self.assertEqual(copied_sheet, report.active_sheet)
            for row_num in range(1, 4):
                report.get_section('row').flush(
                    {
                        'foo': f'A{sheet_num} {row_num}',
                        'bar': f'B{sheet_num} {row_num}',
                        'baz': f'C{sheet_num} {row_num}',
                    }
                )

        self.assertEqual(5, len(report.sheets))

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def test_simple_merge_cells(self):
        """Проверяет простое объединение ячеек."""
        template_name = 'test-simple_merge_cells.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)

        year_header_section = report.get_section('year_header')
        cursor = year_header_section.sheet_data.cursor
        from_col_str, from_row = cursor.column
        from_col = ColumnHelper.column_to_number(from_col_str)

        num = 0
        for num, year in enumerate([2020, 2021, 2022, 2023]):
            year_header_section.flush(
                {'edition_year': year},
                ISpreadsheetSection.HORIZONTAL,
            )

        # склеиваем заголовок ячеек годов издания
        simple_merge_cells(
            section=year_header_section,
            from_row=from_row, to_row=from_row,
            from_col=from_col, to_col=from_col + num
        )

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

@freeze_time(_frozen_time)
class TestWriteXLSX(OfficeOpenXMLDocumentComparisonMixin, unittest.TestCase):
    """Тестируем правильность вывода для XLSX."""

    SUBDIR = 'linux'

    def setUp(self):
        assert self.SUBDIR

        self.src_dir = Path(TESTS_DIR, 'test_data', self.SUBDIR, 'xlsx')
        self.reference_dir = self.src_dir / 'reference'

        self.test_files = dict(
            [(path, os.path.join(self.src_dir, path)) for path in os.listdir(self.src_dir) if path.startswith('test')]
        )

    def _test_left_down(self, report=None):
        if report is None:
            return
        for i in range(2):
            section1 = report.get_section('Section1')
            section1.flush({'section1': i}, oriented=Section.LEFT_DOWN)
            self.assertEqual(section1.sheet_data.cursor.row, ('A', 2 * i + 3))
            self.assertEqual(section1.sheet_data.cursor.column, ('C', 2 * i + 1))

    def _test_left_down2(self, report=None):
        if report is None:
            return
        for i in range(2):
            section3 = report.get_section('Section3')
            section3.flush({'section3': 100}, oriented=Section.LEFT_DOWN)
            self.assertEqual(section3.sheet_data.cursor.row, ('A', 2 * i + 11))
            self.assertEqual(section3.sheet_data.cursor.column, ('C', 2 * i + 9))

    def _test_right_up(self, report):
        section1 = report.get_section('Section1')
        section1.flush({'section1': 2}, oriented=Section.RIGHT_UP)
        self.assertEqual(section1.sheet_data.cursor.row, ('C', 3))
        self.assertEqual(section1.sheet_data.cursor.column, ('E', 1))

    def _test_vertical(self, report):
        for i in range(3):
            section2 = report.get_section('Section2')
            section2.flush({'section2': i}, oriented=Section.VERTICAL)
            self.assertEqual(section2.sheet_data.cursor.row, ('C', 2 * i + 5))
            self.assertEqual(section2.sheet_data.cursor.column, ('E', 2 * i + 3))

    def _test_horizontal(self, report):
        for i in range(3):
            section3 = report.get_section('Section3')
            section3.flush({'section3': i}, oriented=Section.HORIZONTAL)
            self.assertEqual(section3.sheet_data.cursor.row, ('C', 9))
            self.assertEqual(section3.sheet_data.cursor.column, (ColumnHelper.add('G', 2 * i), 7))

    def test_report_write(self):
        template_name = 'test-report-output.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path)
        self._test_left_down(report)
        self._test_right_up(report)
        self._test_vertical(report)
        self._test_horizontal(report)
        self._test_left_down2(report)

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            report.build(dst.name)

            self.assertOfficeOpenXMLEqual(reference_path, dst.name)


@freeze_time(_frozen_time)
class TestWriteXLS(LegacyDocumentComparisonMixin, unittest.TestCase):
    """Тестируем правильность вывода для XSL."""

    SUBDIR = 'linux'

    def setUp(self):
        assert self.SUBDIR

        self.src_dir = Path(TESTS_DIR, 'test_data', self.SUBDIR, 'xls')
        self.reference_dir = self.src_dir / 'reference'

        self.test_files = dict(
            [(path, os.path.join(self.src_dir, path)) for path in os.listdir(self.src_dir) if path.startswith('test')]
        )

    def _test_left_down(self, report):
        for i in range(2):
            section1 = report.get_section('Section1')
            section1.flush({'section1': i}, oriented=Section.LEFT_DOWN)
            self.assertEqual(section1.sheet_data.cursor.row, (0, 2 * i + 2))
            self.assertEqual(section1.sheet_data.cursor.column, (2, 2 * i))

    def _test_left_down2(self, report):
        for i in range(2):
            section3 = report.get_section('Section3')
            section3.flush({'section3': 100}, oriented=Section.LEFT_DOWN)
            self.assertEqual(section3.sheet_data.cursor.row, (0, 2 * i + 10))
            self.assertEqual(section3.sheet_data.cursor.column, (2, 2 * i + 8))

    def _test_right_up(self, report):
        section1 = report.get_section('Section1')
        section1.flush({'section1': 2}, oriented=Section.RIGHT_UP)
        self.assertEqual(section1.sheet_data.cursor.row, (2, 2))
        self.assertEqual(section1.sheet_data.cursor.column, (4, 0))

    def _test_vertical(self, report):
        for i in range(3):
            section2 = report.get_section('Section2')
            section2.flush({'section2': i}, oriented=Section.VERTICAL)
            self.assertEqual(section2.sheet_data.cursor.row, (2, 2 * (i + 1) + 2))
            self.assertEqual(section2.sheet_data.cursor.column, (4, 2 * (i + 1)))

    def _test_horizontal(self, report):
        for i in range(3):
            section3 = report.get_section('Section3')
            section3.flush({'section3': i}, oriented=Section.HORIZONTAL)
            self.assertEqual(section3.sheet_data.cursor.row, (2, 8))
            self.assertEqual(section3.sheet_data.cursor.column, (6 + 2 * i, 6))

    def test_report_write(self):
        template_name = 'test-report-output.xls'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path, wrapper=DocumentXLS, type=FileConverter.XLS)
        self._test_left_down(report)
        self._test_right_up(report)
        self._test_vertical(report)
        self._test_horizontal(report)
        self._test_left_down2(report)

        with NamedTemporaryFile(suffix='.xls') as dst:
            report.build(dst.name)
            self.assertLegacyDocumentEqual(reference_path, dst.name)


@freeze_time(_frozen_time)
class TestReportFormatXLS(LegacyDocumentComparisonMixin, unittest.TestCase):
    """Тест на работоспособность отчета формата XLS."""

    SUBDIR = 'linux'

    def setUp(self):
        assert self.SUBDIR

        self.src_dir = Path(TESTS_DIR, 'test_data', self.SUBDIR, 'xls')
        self.reference_dir = self.src_dir / 'reference'

        self.test_files = dict(
            [(path, os.path.join(self.src_dir, path)) for path in os.listdir(self.src_dir) if path.startswith('test')]
        )

    def test_spreadsheet_with_flag(self):
        """Тест на использование класса SpreadsheetReport с переданным в конструктор wrapper-ом."""
        template_name = 'test_xls.xls'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path, wrapper=DocumentXLS, type=FileConverter.XLS)

        section1 = report.get_section('Section1')
        section1.flush({'tag1': 1})

        report.workbook.active_sheet = 1

        section2 = report.get_section('Section2')
        for i in range(10):
            section2.flush({'tag2': i})

        for i in range(10):
            section2.flush({'tag2': str(10)}, oriented=Section.HORIZONTAL)

        with NamedTemporaryFile(suffix='.xls') as dst:
            report.build(dst.name)
            self.assertLegacyDocumentEqual(reference_path, dst.name)

    def test_with_merge(self):
        """Конструкция with merge для обьединения ячеек вывода."""
        template_name = 'test_merge.xls'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path, wrapper=DocumentXLS, type=FileConverter.XLS)

        s1 = report.get_section('s1')
        s2 = report.get_section('s2')
        s3 = report.get_section('s3')
        s4 = report.get_section('s4')
        s5 = report.get_section('s5')

        s5.flush({'p5': 1}, oriented=ISpreadsheetSection.VERTICAL)
        s5.flush({'p5': 2}, oriented=ISpreadsheetSection.VERTICAL)
        s5.flush({'p5': 3}, oriented=ISpreadsheetSection.HORIZONTAL)

        m1 = MergeXLS(s1, s2, {'p1': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
        with m1:
            m2 = MergeXLS(s2, s3, {'p21': 1, 'p22': 21}, oriented=ISpreadsheetSection.HORIZONTAL)
            with m2:
                m3 = MergeXLS(s3, s4, {'p3': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
                with m3:
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    for i in range(2, 4):
                        s4.flush({'p4': i}, oriented=ISpreadsheetSection.VERTICAL)

                m3_exp = (
                    m3._begin_merge_col == 9
                    and m3._end_merge_col == 9
                    and m3.begin_row_merge == 3
                    and m3.end_row_merge == 5
                )
                self.assertEqual(m3_exp, True)

                m3 = MergeXLS(s3, s4, {'p3': 2}, oriented=ISpreadsheetSection.HIERARCHICAL)
                with m3:
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    s4.flush({'p4': 2}, oriented=ISpreadsheetSection.VERTICAL)

            m2 = MergeXLS(s2, s3, {'p21': 2, 'p22': 21}, oriented=ISpreadsheetSection.HIERARCHICAL)
            with m2:
                m3 = MergeXLS(s3, s4, {'p3': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
                with m3:
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    s4.flush({'p4': 2}, oriented=ISpreadsheetSection.VERTICAL)

        m1_exp = (
            m1._begin_merge_col == 6 and m1._end_merge_col == 6 and m1.begin_row_merge == 3 and m1.end_row_merge == 9
        )
        self.assertEqual(m1_exp, True)

        m1 = MergeXLS(s1, s2, {'p1': 2}, oriented=ISpreadsheetSection.HIERARCHICAL)
        with m1:
            m2 = MergeXLS(s2, s3, {'p21': 1, 'p22': 21}, oriented=ISpreadsheetSection.HORIZONTAL)
            with m2:
                m3 = MergeXLS(s3, s4, {'p3': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
                with m3:
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.HORIZONTAL)
        with NamedTemporaryFile(suffix='.xls') as dst:
            report.build(dst.name)
            self.assertLegacyDocumentEqual(reference_path, dst.name)

    def test_xls_formula_generation(self):
        """Генерация формул в xls."""
        template_name = 'test-formula_generation.xls'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)
        report = SpreadsheetReport(src_path, wrapper=DocumentXLS, type=FileConverter.XLS)

        row_insert_formula_section = report.get_section('row_insert_formula')
        check_insert_formula_section = report.get_section('check_insert_formula')

        insert_formulas(row_insert_formula_section, check_insert_formula_section)

        with NamedTemporaryFile(suffix='.xls') as dst:
            report.build(dst.name)
            self.assertLegacyDocumentEqual(reference_path, dst.name)

    def test_xls_image_insertion(self):
        """Вставка изображений."""
        template_name = 'test_insert_image.xls'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        src_image1 = self.test_files['test_image1.bmp']
        src_image2 = self.test_files['test_image2.bmp']

        report = SpreadsheetReport(src_path, wrapper=DocumentXLS, type=FileConverter.XLS)

        row_section = report.get_section('row')
        row_section.flush({'image1': XLSImage(src_image1)})
        row_section.flush({'image2': XLSImage(src_image2)})
        row_section.flush({'image1': XLSImage(src_image2), 'image2': XLSImage(src_image1)})
        with NamedTemporaryFile(suffix='.xls') as dst:
            report.build(dst.name)
            self.assertLegacyDocumentEqual(reference_path, dst.name)

    def test_rows_height(self):
        """Тест на выставление высоты строк."""
        template_name = 'test_rows_height.xls'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path, wrapper=DocumentXLS, type=FileConverter.XLS)
        report.get_section('row1').flush(
            {
                't1': LOREM_IPSUM[:20],
                't2': '. '.join(['Проверка на автоподбор высоты', LOREM_IPSUM]),
            }
        )

        report.get_section('row2').flush(
            {
                't1': LOREM_IPSUM[:20],
                't2': '. '.join(['Проверка на высоту строки, взятую из шаблона', LOREM_IPSUM]),
            }
        )
        with NamedTemporaryFile(suffix='.xls') as dst:
            report.build(dst.name)
            self.assertLegacyDocumentEqual(reference_path, dst.name)

    def test_copy_sheet(self):
        """Проверяет копирование листа."""
        template_name = 'test-copy_sheet.xls'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        report = SpreadsheetReport(src_path, wrapper=DocumentXLS, type=FileConverter.XLS)

        # заполнение нулевого листа данными
        report.active_sheet = 0
        report.get_section('header').flush({'title': 'Отчёт по отчётам'})

        template_sheet_index = 1
        for sheet_num in range(3):
            target_sheet_name = f'Копия листа-шаблона №{sheet_num}'
            copied_sheet = report.copy_sheet(report.sheets[template_sheet_index], target_sheet_name)
            self.assertIn(copied_sheet, report.sheets)

            # заполнение скопированного листа данными
            self.assertEqual(target_sheet_name, copied_sheet.name)
            report.active_sheet = report.sheets.index(copied_sheet)
            self.assertEqual(copied_sheet, report.active_sheet)
            for row_num in range(1, 4):
                report.get_section('row').flush(
                    {
                        'foo': f'A{sheet_num} {row_num}',
                        'bar': f'B{sheet_num} {row_num}',
                        'baz': f'C{sheet_num} {row_num}',
                    }
                )

        self.assertEqual(5, len(report.sheets))

        with NamedTemporaryFile(suffix='.xls') as dst:
            report.build(dst.name)

            self.assertLegacyDocumentEqual(reference_path, dst.name)


@freeze_time(_frozen_time)
class TestWindowsXLSX(TestXLSXMixin, unittest.TestCase):
    SUBDIR = 'win'


@freeze_time(_frozen_time)
class TestUtils(unittest.TestCase):
    def test_date_to_float(self):
        """Тест преобразования даты в число."""
        date_float = date_to_float(datetime(1899, 12, 30))
        self.assertEqual(date_float, 0)

        date_float = date_to_float(datetime(1899, 12, 31))
        self.assertEqual(date_float, 1)

        date_float = date_to_float(datetime(1899, 12, 29))
        self.assertEqual(date_float, 1)

        date_float = date_to_float(datetime(1899, 12, 29, 6))
        self.assertEqual(date_float, 1.25)

        date_float = date_to_float(datetime(1900, 1, 1))
        self.assertEqual(date_float, 2)

        date_float = date_to_float(datetime(1900, 1, 1, 6))
        self.assertEqual(date_float, 2.25)


def insert_formulas(row_insert_formula_section, check_insert_formula_section):
    for j in range(4):
        row_insert_formula_section.flush(
            {'p1': 5 + j, 'p2': 6 - j, 'p3': 4 * j},
            used_formulas={'p1': ['p1', 't1'], 'p2': ['p2']},
        )
    check_insert_formula_section.flush(
        {
            'f2': FormulaWriteExcel('p2', 'AVERAGE', True),
            'f3': FormulaWriteExcel('p1', 'SUM', False),
        },
        oriented=ISpreadsheetSection.VERTICAL,
    )
