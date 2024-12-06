import copy
import os
import re
import shutil
from pathlib import (
    Path,
)

from lxml import (
    etree,
)
from lxml.etree import (
    QName,
    fromstring,
    tostring,
)

from simple_report.core.exception import (
    SectionException,
    SectionNotFoundException,
    SheetNotFoundException,
)
from simple_report.core.shared_table import (
    SharedStringsTable,
)
from simple_report.core.xml_wrap import (
    CommonProperties,
    OpenXMLFile,
    ReletionOpenXMLFile,
    ReletionTypes,
)
from simple_report.interface import (
    ISpreadsheetWorkbook,
    ISpreadsheetWorkbookSheet,
)
from simple_report.utils import (
    get_addr_cell,
)
from simple_report.xlsx.cursor import (
    Cursor,
)
from simple_report.xlsx.section import (
    Section,
    SheetData,
)


class Comments(OpenXMLFile):
    """Комментарии в XLSX."""

    NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    NS_XDR = 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing'

    section_pattern = re.compile(r'[\+|\-]+[A-Za-zА-яА-я0-9_]+')

    def __init__(self, sheet_data, *args, **kwargs):
        """Инициализация комментариев.

        :param sheet_data: данные для листа
        :type sheet_data: xlsx.section.SheetData
        """
        super().__init__(*args, **kwargs)

        assert isinstance(sheet_data, SheetData)
        self._sheet_data = sheet_data

        self.sections = {}

        self.comment_list = self._root.find(QName(self.NS, 'commentList'))
        self._create_section()

        # Проверка, правильно ли указаны секции и есть ли конец секции
        self._test_sections()

    def _test_sections(self):
        """Проверка секций на валидность."""
        for section_object in self.sections.values():
            if not section_object.name or not section_object.begin or not section_object.end:
                raise ValueError(f'Bad section: {section_object}')

    def _parse_sections(self, comment_list):
        """Распознаем секции.

        :param comment_list: Список комментариев
        :type comment_list: iterable
        """
        for comment in comment_list:
            cell = comment.get('ref')
            for text in comment:
                for r in text:
                    for t in r.findall(QName(self.NS, 't')):
                        yield t.text, cell

    def _create_section(self):
        """Создание объектов секций из комментариев."""
        for section in self._parse_sections(self.comment_list):
            self._add_section(section)

    def _add_section(self, values):
        text = values[0]
        cell = values[1]

        values = self.section_pattern.findall(text)
        addr = get_addr_cell(cell)
        for value in values:
            section_name = self._get_name_section(value)

            # Такой объект должен быть
            if value.startswith('-'):
                # Такой элемент уже должен быть
                if not self.sections.get(section_name):
                    raise SectionException(f'Start section "{section_name}" not found')

                section = self.sections[section_name]

                # Второго конца быть не может
                if section.end:
                    raise SectionException(f'For section "{section_name}" more than one ending tag')

                section.end = addr
            else:
                # Второго начала у секции быть не может
                if self.sections.get(section_name):
                    raise SectionException(f'For section "{section_name}" more than one beging tag')

                self.sections[section_name] = Section(self._sheet_data, section_name, begin=addr)

    def _get_name_section(self, text):
        """Возвращает из наименования ++A - название секции.

        :param text: комментарий
        :type text: basestring
        """
        for i, s in enumerate(text):
            if s.isalpha():
                return text[i:]
        raise SectionException(f'Section name bad format "{text}"')

    def get_section(self, section_name):
        """Получение секции по имени.

        :param section_name:
        :type section_name:
        """
        try:
            section = self.sections[section_name]
        except KeyError as ke:
            raise SectionNotFoundException(f'Section "{section_name}" not found') from ke
        return section

    def get_sections(self):
        """Получение всех секций."""
        return self.sections

    @classmethod
    def create(cls, cursor, *args, **kwargs):  # pylint:disable=arguments-differ
        return cls(cursor, *args, **kwargs)

    def build(self):
        """Сборка файла с комментариями, предварительно удалив их."""
        if len(self.comment_list) > 0:
            self.comment_list.clear()

        with open(self.file_path, 'wb') as f:
            f.write(tostring(self._root, encoding='utf-8', xml_declaration=True))

    def copy(self, target_sheet_index: int):
        """Создаёт свою копию."""
        dst_sheet_path = Path(self.current_folder) / f'comments{target_sheet_index}.xml'
        shutil.copy(self.file_path, dst_sheet_path)


class SharedStrings(OpenXMLFile):
    """XML-файл с общими строками, на каждую из которых могут ссылаться из других xml-файлов XLSX."""

    NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = SharedStringsTable(self._root)

    def build(self):
        """Сборка файла."""
        new_root = self.table.to_xml()
        with open(self.file_path, 'wb') as f:
            f.write(tostring(new_root, encoding='utf-8', xml_declaration=True))


class WorkbookSheet(ReletionOpenXMLFile, ISpreadsheetWorkbookSheet):
    """Лист книги документа в формате XLSX."""

    NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

    def __init__(self, shared_table, tags, name, sheet_id, *args, **kwargs):
        """Инициализация листа рабочей книги.

        :param shared_table:
        :type shared_table:
        :param tags:
        :type tags:
        :param name:
        :type name:
        :param sheet_id:
        :type sheet_id:
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.sheet_id = sheet_id

        # Первый элемент: начало вывода по вертикали, второй по горизонтали
        self.sheet_data = SheetData(
            self._root,
            cursor=Cursor(),
            ns=self.NS,
            shared_table=shared_table,
            tags=tags,
        )

        self.drawing, self.comments = self.walk_reletion()

    def walk_reletion(self):
        drawing = comments = None
        if self._reletion_root is not None:
            for elem in self._reletion_root:
                param = (elem.attrib['Id'], elem.attrib['Target'])
                if elem.attrib['Type'] == ReletionTypes.DRAWING:
                    drawing = self._get_drawing(*param)  # pylint:disable=assignment-from-no-return

                elif elem.attrib['Type'] == ReletionTypes.COMMENTS:
                    comments = self._get_comment(*param)

        return drawing, comments

    def _get_comment(self, rel_id, target):
        """Получение объекта комментария."""
        return Comments.create(self.sheet_data, rel_id, *self._get_path(target))

    def _get_drawing(self, rel_id, target):
        """Unused."""

    def __str__(self):
        res = [f'Sheet name "{self.name}":']
        if self.comments:
            for section in self.sections:
                res.append(f'\t {section}')
        return '\n'.join(res)

    def __repr__(self):
        return self.__str__()

    def get_name(self) -> str:
        return self.name

    @property
    def sections(self):
        return self.comments.get_sections()

    def get_section(self, name):
        """Получение секции по имени."""
        return self.comments.get_section(name)

    def get_sections(self):
        """Получение всех секций."""
        return self.sections

    def build(self):
        """Сборка xml-файла."""
        new_root = self.sheet_data.new_sheet()

        with open(self.file_path, 'wb') as f:
            f.write(tostring(new_root, encoding='utf-8', xml_declaration=True))

        if self.comments:
            self.comments.build()

    def get_rowbreaks(self):
        return self.sheet_data.get_rowbreaks()

    def get_colbreaks(self):
        return self.sheet_data.get_colbreaks()

    # pylint:disable-next=too-many-positional-arguments,too-many-arguments
    def copy(self, tags, shared_table, target_rid: str, target_sheet_index: int, target_name: str) -> 'WorkbookSheet':
        """Создаёт свою копию."""
        # копирование xml самого листа
        dst_sheet_path = Path(self.current_folder) / f'sheet{target_sheet_index}.xml'
        shutil.copy(self.file_path, dst_sheet_path)
        # копирование комментариев листа
        self.comments.copy(target_sheet_index)

        # копирование связей листа
        # ----------------------------------------------------------------------
        dst_sheet_reletion_path = Path(
            self.current_folder,
            self.RELETION_FOLDER,
            f'sheet{target_sheet_index}.xml{self.RELETION_EXT}',
        )

        sheet_rels_tree_root = copy.deepcopy(self._reletion_root)
        for rel in sheet_rels_tree_root.findall(
            f".//ns0:Relationship[@Target='../comments{self.sheet_id}.xml']",
            namespaces={'ns0': CommonPropertiesXLSX.NS},
        ):
            target = rel.get('Target')
            if target and 'comments' in target:
                # Заменяем комментарии на копию
                rel.set('Target', f'../comments{target_sheet_index}.xml')

        # сохраняем обновленный .rels файл
        with Path(dst_sheet_reletion_path).open('wb') as sheet_rels_xml:
            sheet_rels_xml.write(tostring(sheet_rels_tree_root, xml_declaration=True, encoding='UTF-8'))

        # ----------------------------------------------------------------------
        return WorkbookSheet(
            name=target_name,
            sheet_id=target_sheet_index,
            file_name=dst_sheet_path.name,
            file_path=dst_sheet_path,
            folder=dst_sheet_path.parent,
            rel_id=target_rid,
            tags=tags,
            shared_table=shared_table,
        )


class WorkbookStyles(OpenXMLFile):
    """Unused."""


class Workbook(ReletionOpenXMLFile, ISpreadsheetWorkbook):
    """Книга в формате XLSX."""

    NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

    _sheets: list[WorkbookSheet]
    _copied_sheets: set
    _activated_sheets: set

    def __init__(self, tags, *args, **kwargs):
        """Инициализация рабочей книги.

        :param tags:
        :type tags:
        """
        super().__init__(*args, **kwargs)

        self.tags = tags

        (self.workbook_style, tmp_sheets, self.shared_strings, self.calc_chain) = self.walk_reletions()
        self._sheets = self.walk(tmp_sheets)

        if self.sheets:
            # По-умолчанию активным считается первый лист
            self._active_sheet = self.sheets[0]
        else:
            raise SheetNotFoundException('Sheets not found')

        self._copied_sheets = set()
        self._activated_sheets = set()

    def walk_reletions(self):
        workbook_style = shared_strings = calc_chain = None
        sheets = {}
        for elem in self._reletion_root:
            param = (elem.attrib['Id'], elem.attrib['Target'])
            if elem.attrib['Type'] == ReletionTypes.WORKBOOK_STYLE:
                workbook_style = self._get_style(*param)  # pylint:disable=assignment-from-no-return

            elif elem.attrib['Type'] == ReletionTypes.WORKSHEET:
                sheets[elem.attrib['Id']] = elem.attrib['Target']

            elif elem.attrib['Type'] == ReletionTypes.SHARED_STRINGS:
                shared_strings = self._get_shared_strings(*param)
            elif elem.attrib['Type'] == ReletionTypes.CALC_CHAIN:
                calc_chain = self._get_calc_chain(*param)
                self._reletion_root.remove(elem)

        return workbook_style, sheets, shared_strings, calc_chain

    def walk(self, sheet_reletion):
        sheets = []
        sheets_elem = self._root.find(QName(self.NS, 'sheets'))
        for sheet_elem in sheets_elem:
            name = sheet_elem.attrib['name']
            sheet_id = sheet_elem.attrib['sheetId']
            # state = sheet_elem.attrib['state'] -- В win файле нет такого свойства

            rel_id = sheet_elem.attrib.get(QName(self.NS_R, 'id'))
            target = sheet_reletion[rel_id]
            sheet = self._get_worksheet(rel_id, target, name, sheet_id)
            sheets.append(sheet)

        return sheets

    def _get_style(self, _id, target):
        """Unused."""

    def _get_worksheet(self, rel_id, target, name, sheet_id):
        """Получение листа книги.

        :param rel_id:
        :type rel_id:
        :param target:
        :type target:
        :param name:
        :type name:
        :param sheet_id:
        :type sheet_id:
        """
        worksheet = WorkbookSheet.create(
            self.shared_table,
            self.tags,
            name,
            sheet_id,
            rel_id,
            *self._get_path(target),
        )
        return worksheet

    def _get_shared_strings(self, _id, target):
        """Получение общих строк.

        :param _id: идентификатор строки
        :type _id:
        :param target:
        :type target:
        """
        return SharedStrings.create(_id, *self._get_path(target))

    def _get_calc_chain(self, _id, target):
        return CalcChain.create(_id, *self._get_path(target))

    def _add_sheet(self, sheet: WorkbookSheet):
        # регистрируем новый лист в workbook.xml
        # ----------------------------------------------------------------------
        new_sheet_element = etree.Element(
            etree.QName(self.NS, 'sheet'),
            {
                'name': sheet.name,
                'sheetId': str(sheet.sheet_id),
                etree.QName(self.NS_R, 'id'): sheet.reletion_id,
            },
        )

        sheets = self._root.xpath('.//n:sheets/n:sheet', namespaces={'n': self.NS})
        sheets[-1].addnext(new_sheet_element)

        with Path(self.file_path).open('wb') as worksheet_xml:
            worksheet_xml.write(tostring(self._root, xml_declaration=True, encoding='UTF-8'))

        # обновляем основной workbook.xml.rels для добавления связи с новым листом
        new_rel_element = etree.Element(
            etree.QName(CommonProperties.NS, 'Relationship'),
            {
                'Id': sheet.reletion_id,
                'Type': ReletionTypes.WORKSHEET,
                'Target': f'worksheets/{sheet.file_name}',
            },
        )
        self._reletion_root.append(new_rel_element)

        with Path(
            self.current_folder, self.RELETION_FOLDER, f'{self.file_name}{self.RELETION_EXT}'
        ).open('wb') as workbook_xml_rels:
            workbook_xml_rels.write(tostring(self._reletion_root, xml_declaration=True, encoding='UTF-8'))

        # добавление объёкта листа в объект рабочей книги
        # ----------------------------------------------------------------------
        self.sheets.append(sheet)

    def _hide_template_sheets(self):
        """Скрывает листы, которые скопированы, но не были активированы (в них не происходила запись).

        Предполагается, что запись (.flush()) ведётся в активный лист, а значит, если лист был скопирован и не был
        активирован, значит это лист-шаблон и в конечном отчёте он не требуется.
        """
        for template_sheet in self._copied_sheets.difference(self._activated_sheets):
            self.hide_sheet(template_sheet)

    @property
    def active_sheet(self):
        return self._active_sheet

    @active_sheet.setter
    def active_sheet(self, value):
        assert isinstance(value, int)
        self._active_sheet = self.sheets[value]

        self._activated_sheets.add(self._active_sheet)

    @property
    def sheets(self) -> list[WorkbookSheet]:
        return self._sheets

    def build(self):
        for sheet in self.sheets:
            sheet.build()

        self.shared_strings.build()
        if self.calc_chain:
            self.calc_chain.build()

        # Сокрытие листов-шаблонов. Повторяет `simple_report.xls.workbook.Workbook`, за тем исключением,
        # что скрываются из конечного отчёта только ранее скопированные листы (для сохранения обратной совместимости).
        self._hide_template_sheets()

    @property
    def shared_table(self):
        return self.shared_strings.table

    def get_rowbreaks(self):
        return self._active_sheet.get_rowbreaks()

    def get_colbreaks(self):
        return self._active_sheet.get_colbreaks()

    def copy_sheet(self, sheet: WorkbookSheet, target_sheet_name: str) -> WorkbookSheet:
        """Копировать лист рабочей книги."""
        self._copied_sheets.add(sheet)

        next_sheet_id = max(int(i.sheet_id) for i in self.sheets) + 1
        next_rid = self.next_rid()

        copied_sheet = sheet.copy(self.tags, self.shared_table, next_rid, next_sheet_id, target_sheet_name)
        self._add_sheet(copied_sheet)

        return copied_sheet

    def hide_sheet(self, sheet: WorkbookSheet):
        """Скрыть лист."""
        sheet_index = self.sheets.index(sheet)
        sheet = self._root.xpath('.//n:sheets/n:sheet', namespaces={'n': self.NS})[sheet_index]

        sheet.set('state', 'hidden')
        with Path(self.file_path).open('wb') as workbook_xml:
            workbook_xml.write(tostring(self._root, xml_declaration=True, encoding='UTF-8'))


class CommonPropertiesXLSX(CommonProperties):
    def _get_app_common(self, _id, target) -> Workbook:
        return Workbook.create(self.tags, _id, *self._get_path(target))


class CalcChain(OpenXMLFile):
    """Цепочка вычислений. Указывает порядок вычислений в ячейках а также является кешем значений.

    (http://stackoverflow.com/questions/9004848/working-with-office-open-xml-just-how-hard-is-it)
    Поскольку довольно сложно в автоматическом режиме указывать порядок
    вычисления, просто удаляем файл + ссылки на него.
    Еще 1 плюс такого подхода - больше не должна повторяться ошибка при
    открытии файла в MS Office 2007/2010, шаблон которого был сохранен
    то в Libre/Openoffice, то в MS Office
    """

    NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

    def build(self):
        """Удаляем файл с цепочкой вычислений."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    @classmethod
    def from_file(cls, file_path: str):
        assert file_path
        # if os.path.exists(file_path):
        #     with open(file_path) as f:
        #         return parse(f).getroot()
        # else:
        return fromstring('<fake_root/>')
