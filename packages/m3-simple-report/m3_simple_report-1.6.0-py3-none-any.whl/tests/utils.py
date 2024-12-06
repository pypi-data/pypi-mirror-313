import zipfile


class OfficeOpenXMLDocumentComparisonMixin:
    """Примесь для сравнения офисных файлов (.docx, .xlsx)."""

    @staticmethod
    def _extract_zip_content(file_path, ignore_files=None):
        """Распаковывает содержимое ZIP-архива (docx/xlsx) в словарь.

        Игнорирует файлы из ignore_files.
        """
        if ignore_files is None:
            ignore_files = set()
        content_dict = {}
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for file_name in sorted(zip_ref.namelist()):  # Сортировка для стабильности
                if file_name in ignore_files:
                    continue
                with zip_ref.open(file_name) as file:
                    content_dict[file_name] = file.read()
        return content_dict

    def assertOfficeOpenXMLEqual(self, reference_document, document, ignore_files=None):
        """Проверяет, что содержимое двух документов (docx/xlsx) идентично.

        Игнорирует файлы, указанные в ignore_files.
        """
        reference_document_content = self._extract_zip_content(reference_document, ignore_files)
        document_content = self._extract_zip_content(document, ignore_files)

        # Проверка списков файлов
        self.assertEqual(
            reference_document_content.keys(),
            document_content.keys(),
            'Списки файлов внутри архивов отличаются: '
            f'{set(reference_document_content.keys()) ^ set(document_content.keys())}',
        )

        # Проверка содержимого каждого файла
        for file_name in reference_document_content:
            self.assertEqual(
                reference_document_content[file_name],
                document_content[file_name],
                f'Файл {file_name} внутри архивов отличается.',
            )


class LegacyDocumentComparisonMixin:
    """Примесь для сравнения документов устаревших форматов (.rtf .doc .xls)."""

    def assertLegacyDocumentEqual(self, reference_document, document):
        """Проверяет, что документы идентичны."""
        with open(reference_document, 'rb') as ref_doc, open(document, 'rb') as doc:
            reference_content = ref_doc.read()
            content = doc.read()

        self.assertEqual(reference_content, content, 'Документы отличаются.')
