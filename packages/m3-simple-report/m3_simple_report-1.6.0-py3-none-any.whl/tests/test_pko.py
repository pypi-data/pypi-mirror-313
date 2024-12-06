from pathlib import (
    Path,
)
from tempfile import (
    NamedTemporaryFile,
)

from simple_report.report import (
    SpreadsheetReport,
)


class TestPKO:
    dst_dir = test_files = None

    def test_pko(self):
        template_name = 'test-PF_PKO.xlsx'
        src_path = self.test_files[template_name]
        reference_path = Path(self.reference_dir, template_name)

        with NamedTemporaryFile(suffix='.xlsx') as dst:
            self.create_report(src_path, dst.name)
            self.assertOfficeOpenXMLEqual(reference_path, dst.name)

    def create_report(self, temp_path, res_path):
        header_params = {}
        # string_params = {}
        bottom_params = {}

        header_params['cashier'] = 'Иванов Иван Иваныч'  # document.cashier

        # enterprise = Enterprise.objects.filter(id=document.enterprise_id)
        # if enterprise:
        header_params['enterprise'] = 'Здесь название организации'  # enterprise[0].name
        header_params['okpo'] = '123947843'  # enterprise[0].okpo

        # if document.number:
        header_params['number'] = '1'  # document.number

        date = '01-01-2001'  # document.date_formatting
        base = 'Иванычу на похмел'  # document.base
        if date:
            header_params['date'] = date
            bottom_params['date'] = date
        if base:
            header_params['base'] = base
            bottom_params['base'] = base

        report = SpreadsheetReport(temp_path)

        header = report.get_section('Header')
        header.flush(header_params)

        # Строки, соответствующие операциям
        # operations = AccEntry.objects.filter(document_id = document_id).select_related('debet_kbk',
        #                                                                               'credit_kbk',
        #                                                                               'debit_account',
        #                                                                               'credit_account')
        # total_summa = 1000.21
        # for operation in operations:
        # if document.kvd:
        #    kvd = ' %s ' %document.kvd.code
        # else:
        #    kvd = ' '
        kvd = '1'

        debit_kbk_part = '123456789012'  # operation.debet_kbk if operation.debet_kbk else ''
        debit_account = '20104'  # operation.debet_account if operation.debet_account else ''

        credit_kbk_part = '976543223232'  # operation.credit_kbk if operation.credit_kbk else ''
        credit_account = '40110'  # operation.credit_account if operation.credit_account else ''

        debit_kbk = debit_kbk_part + kvd + debit_account
        credit_kbk = credit_kbk_part + kvd + credit_account

        # total_summa += operation.summa

        string_params = {'debit_kbk': debit_kbk, 'kredit_kbk': credit_kbk}

        # if credit_account:
        accounting = credit_account  # credit_account.code[-2:]
        string_params['accounting'] = accounting

        # if operation.summa:
        string_params['sum'] = 1000.21  # operation.summa

        string = report.get_section('String')
        for i in range(20):
            string.flush(string_params)

        # bottom_params = {'total_sum': total_summa,
        #                 'total_kopeks': two_decimal_kopeks(total_summa),
        #                 'total_sum_in_words': money_in_words(total_summa)
        #                 }
        bottom_params = {
            'total_sum': 1000.21,
            'total_kopeks': 21,
            'total_sum_in_words': 'Одна тысяча рублей',
            'annex': 'annex',
            'cashier': 'Иванов Иван Иваныч',
        }

        # if document.annex:
        # if document.cashier:

        bottom = report.get_section('Bottom')
        bottom.flush(bottom_params)

        report.build(res_path)
