import os
import shutil
import uuid
import zipfile
from collections import (
    namedtuple,
)
from datetime import (
    datetime,
)
from tempfile import (
    gettempdir,
)


class FileException(Exception):
    """Исключение работы с файл-прокси."""


class ZipProxy:
    """Распаковка/упаковка Open XML."""

    @classmethod
    def _extract(cls, src_file_path, dst_files_path):
        """Распаковывает zip файл.

        :param src_file_path: путь до исходного файла
        :type src_file_path: str
        :param dst_files_path: путь до выходного файла/директории
        :type dst_files_path: str

        """
        with zipfile.ZipFile(src_file_path) as zip_file:
            zip_file.extractall(dst_files_path)

    @classmethod
    def _pack_dir_files(
        cls,
        files_dir_path,
        file_names,
        src_files_path,
        zip_file,
    ):
        """Запаковывает zip файлы заданной директории.

        :param files_dir_path: путь до директории с входными файлами
        :type files_dir_path: str
        :param file_names: названия файлов
        :type file_names: list
        :param src_files_path: путь до корневой директори
        :type src_files_path: str
        :param zip_file: zip файл
        :type zip_file: zipfile.ZipFile
        """
        for file_name in file_names:
            # Абсолютный путь до файла
            abs_path = os.path.join(files_dir_path, file_name)

            # Путь до директории
            dir_path = abs_path[len(src_files_path) + len(os.sep) :]

            zip_file.write(abs_path, dir_path, compress_type=zipfile.ZIP_DEFLATED)

    @classmethod
    def _pack(cls, dst_file_path, src_files_path):
        """Запаковывает zip файл.

        :param dst_file_path: путь до выходного файла
        :type dst_file_path: str
        :param src_files_path: путь до директории с входными файлами
        :type src_files_path: str
        """
        with zipfile.ZipFile(dst_file_path, 'w') as zip_file:
            for root, _, file_names in os.walk(src_files_path):
                # файлы из docProps запаковываем в последнюю очередь
                # для установления корректного mime type
                if os.path.split(root)[1] == 'docProps':
                    props_root, props_file_names = root, file_names
                    continue

                cls._pack_dir_files(root, file_names, src_files_path, zip_file)

            # pylint:disable=possibly-used-before-assignment
            cls._pack_dir_files(props_root, props_file_names, src_files_path, zip_file)
            # pylint:enable=possibly-used-before-assignment

    @classmethod
    def extract(cls, src_file):
        """Распаковывает zip архив во временную папку.

        :param src_file: путь до архива
        :type src_file: str
        """
        assert isinstance(src_file, FileProxy)

        extract_folder = os.path.join(gettempdir(), '_'.join([str(uuid.uuid4())[:8], src_file.get_file_name()]))

        cls._extract(src_file.get_path(), extract_folder)

        return extract_folder

    @classmethod
    def pack(cls, dst_file, extract_folder):
        """Запаковывает директорию в архив и удаляет ее.

        :param dst_file: выходной файл
        :type dst_file: FileProxy
        :param extract_folder: исходная директория
        :type extract_folder: str
        """
        assert isinstance(dst_file, FileProxy)
        cls._pack(dst_file.get_path(), extract_folder)
        shutil.rmtree(extract_folder)


class FileProxy:
    """Прокси работы с файлами."""

    def __init__(self, file_like_object, new_file=False):
        """Инициализация прокси для работы с файлами.

        :param file_like_object: Путь до файла
        :type file_like_object: str
        :param new_file: создавать ли новый файл?
        :type new_file: bool
        """
        if isinstance(file_like_object, FileProxy):
            file_like_object = file_like_object.file

        self.is_file_like_object = False
        if hasattr(file_like_object, 'read'):
            raise FileException('File like object temporarily not supported.')

        if not os.path.exists(file_like_object) and not new_file:
            raise FileException(f'File "{file_like_object}" not found.')

        if not os.path.isfile(file_like_object) and not new_file:
            raise FileException(f'"{file_like_object}" is not file')

        self.file = file_like_object

    def get_path(self):
        """Возвращает путь до файла."""
        return self.file

    def get_file_like_object(self):
        """Возвращает открытый файл."""
        return self.file

    def get_file_name(self):
        """Возвращает только имя файла."""
        if self.is_file_like_object:
            file_name = self.file.name
        else:
            file_name = self.file

        return os.path.split(file_name)[-1]


class ColumnHelper:
    """Существенно облегчает работу с ячейками.

    По данными ('ALC'), ('AVB') возврашает итератор по диапазону ячеек
    ('ALC', 'ALD', 'ALE', ..., 'AVA', 'AVB')

    Так же умеет работать, если переданы данные: ('A'), ('ALP')

    """

    # Кэши соответствия номеров колонок и их строковых представлений
    _num_to_col_cache = {}
    _col_to_num_cache = {}

    @classmethod
    def number_to_column(cls, n):
        """Преобразует номер колонки в ее строковое представление.

        :param n: номер колонки
        :type n: int
        """
        column = cls._num_to_col_cache.get(n)
        if not column:
            column = ~n and cls.number_to_column(n // 26 - 1) + chr(65 + n % 26) or ''
            cls._num_to_col_cache[n] = column

        return column

    @classmethod
    def column_to_number(cls, index):
        """Преобразует строковое представление колонки в число.

        :param index: номер
        :type index: int
        """
        number = cls._col_to_num_cache.get(index)
        if not number:
            s = 0
            pow_ = 1
            for letter in index[::-1]:
                d = int(letter, 36) - 9
                s += pow_ * d
                pow_ *= 26
                # excel starts column numeration from 1
            number = s - 1
            cls._col_to_num_cache[index] = number

        return number

    @classmethod
    def get_range(cls, begin, end):
        """Итератор, выдающий строковые представления колонок между начальной и конечной колонкой.

        :param begin: строковое представление начальной колонки
        :type begin: str
        :param end: строковое представление конечной колонки
        :type end: str
        """
        for i in range(cls.column_to_number(begin), cls.column_to_number(end) + 1):
            yield cls.number_to_column(i)

    @classmethod
    def add(cls, column, i):
        """Добавляет к колонке column i колонок.

        :param column: строковое представление колонки
        :type column: str
        :param i: число дополнительных колонок
        :type i: int
        """
        return cls.number_to_column(cls.column_to_number(column) + i)

    @classmethod
    def difference(cls, col1, col2):
        """Разница (расстояние) между двумя колонками.

        :param col1: строковое представление первой колонки
        :type col1: str
        :param col2: строковое представление второй колонки
        :type col2: str
        """
        return cls.column_to_number(col1) - cls.column_to_number(col2)

    @classmethod
    def reset_caches(cls):
        """Сброс кэшэй, созданных в процессе работы."""
        cls._num_to_col_cache = {}
        cls._col_to_num_cache = {}


def get_addr_cell(text):
    """Возвращает адрес ячейки.

    То есть из представления 'AZ12' выдается ('AZ', 12).

    :param text: полное строковое представление ячейки
    :type text: str
    """
    for i, s in enumerate(text):
        if s.isdigit():
            return text[:i], int(text[i:])

    raise ValueError(f'Addr cell is bad format value "{text}"')


def date_to_float(date):
    """Конвертирует дату в число с плавающей точкой относительно 1900 года.

    Значение даты OLE-автоматизации реализовано как число с плавающей запятой,
    равное количеству дней, прошедших с полуночи 30 декабря 1899 г.
    Например, полночь 31 декабря 1899 г. представляется числом 1,0;
    06:00 1 января 1900 г. — числом 2,25;
    полночь 29 декабря 1899 г. — числом 1,0
    и 06:00 29 декабря 1899 г. — числом 1,25.

    http://msdn.microsoft.com/ru-ru/library/system.datetime.tooadate%28v=vs.90%29.aspx

    ps: Спасибо Вадиму, который предотвратил распространение кастылей,
    типо кастомного форматирования параметров

    :param date: Дата-время
    :type date: datetime.datetime
    """
    assert isinstance(date, datetime)

    date_1900 = datetime(1899, 12, 30)

    days = abs((date - date_1900).days)

    hours = date.time().hour - date_1900.time().hour

    minute = date.time().minute - date_1900.time().minute

    return days + (hours + minute / 60.0) / 24.0


FormulaWriteExcel = namedtuple('FormulaWriteExcel', ['formula_id', 'excel_function', 'ranged'])


class FormulaWriteExcelFromStr:
    """Для переноса текстовой формулы из Python в Excel по принципу "как есть".

    Но не стоит забывать об особенностях, например, что ";" при перечислении
    образуется с помощью ",", а если использовано будет в строке ";",
    то в Excel получим "|". По-хорошему этот перенос для простой арифметики.
    """

    def __init__(self, text):
        self.text = text


def split_string(string, line_length):
    """Разбить строку на подстроки, по возможности, не превышающие заданной длины.

    :param basestring string: разбиваемая строка
    :param int line_length: желаемая длина подстроки
    :return: список подстрок строки
    :rtype: list
    """
    name_words = string.split()
    lines = [[]]
    cur_line_length = 0
    for word in name_words:
        if cur_line_length and cur_line_length + 1 + len(word) > line_length:
            lines.append([])
            cur_line_length = len(word)
        else:
            cur_line_length += len(word) + 1
        lines[-1].append(word)

    return [' '.join(line) for line in lines]
