from pathlib import (
    Path,
)
from tempfile import (
    NamedTemporaryFile,
)

from simple_report.report import (
    SpreadsheetReport,
)


class TestPagebreaks:
    def test_pagebreaks(self):
        template_name = 'test-pagebreaks.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            result = self.create_pagebreaks_report(src_path, dst.name)
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

        self.check_pagebreaks_results(result)

    def create_pagebreaks_report(self, temp_path, res_path):
        section_params = {}
        report = SpreadsheetReport(temp_path)

        # проверим начальное количество разделителей
        rb = report.workbook.get_rowbreaks()
        self.assertEqual(len(rb), 0)

        cb = report.workbook.get_colbreaks()
        self.assertEqual(len(cb), 0)

        section = report.get_section('line')
        for i in range(20):
            section.flush(section_params)

        bottom_section = report.get_section('bottom')
        for i in range(2):
            bottom_section.flush(section_params)

        report.build(res_path)

        return report

    def check_pagebreaks_results(self, report):
        # проверим конечное количество разделителей
        rb = report.workbook.get_rowbreaks()
        self.assertEqual(len(rb), 4)

        cb = report.workbook.get_colbreaks()
        self.assertEqual(len(cb), 2)

        return report
