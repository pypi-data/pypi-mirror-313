from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Sequence, Self, final, Literal

class XLSXBook:
    sheets: Sequence[XLSXSheet]

    def __init__(self) -> None:
        """
        Инициализация парсера
        """
        ...

    def add_sheet(
        self,
        name: str,
        rows: int | None = None,
        cols: int | None = None,
    ) -> XLSXSheet:
        """Добавление листа в книгу"""
        ...

    def get_sheet_index(self, idx: int) -> XLSXSheet | None:
        """Получение листа по индексу"""
        ...

    def get_sheet_name(self, name: str) -> XLSXSheet | None:
        """Получение листа по названию"""
        ...

    def to_json(self) -> str:
        """Преобразование книги в json"""
        ...

    def to_dict(self) -> dict[str, Any]:
        """Преобразование книги в dict"""
        ...

class XLSXSheet:
    """Тип данных листа с которыми работает парсер."""

    name: str
    max_row: int
    max_column: int
    index: int
    cells: Sequence[XLSXSheetCell]

    def __init__(
        self,
        name: str,
        index: int,
        rows: int = 50,
        cols: int = 30,
    ) -> None:
        """Инициализация"""
        ...

    @final
    def find_cell_by_cell(self, cell: str) -> XLSXSheetCell | None:
        """Функция для получения ячейки по cell (A1)."""
        ...

    @final
    def find_cell_by_coords(self, row: int, col: int) -> XLSXSheetCell | None:
        """Функция для ячейки по координатам."""
        ...

    @final
    def write_cell(self, row: int, col: int, value: str) -> XLSXSheetCell:
        """Добавление данных в cells"""
        ...

    @final
    def delete_cols(self, idx: int, cols: int) -> None:
        """Метод удаления колонок"""
        ...

    @final
    def delete_rows(self, idx: int, rows: int) -> None:
        """Метод удаления строк"""
        ...

    @final
    def set_merged_cells(
        self,
        start_row: int,
        end_row: int,
        start_column: int,
        end_column: int,
    ) -> None:
        """Метод для добавления данных по объединению ячеек."""
        ...

    @final
    def generate_empty_cells(self) -> None:
        """Метод для генерации пустых ячеек."""
        ...

    @final
    def iter_cells(
        self,
        min_row: int | None = None,
        max_row: int | None = None,
        min_col: int | None = None,
        max_col: int | None = None,
    ) -> Sequence[XLSXSheetCell]:
        """Получить список всех ячеек в заданном диапазоне."""
        ...

class XLSXSheetCell:
    """Тип данных ячеек листа с которыми работает парсер."""

    row: int
    column: int
    cell: str
    value: Any | None
    formula: str | None
    data_type: str
    number_format: str
    is_merge: bool
    start_column: int | None
    end_column: int | None
    start_row: int | None
    end_row: int | None
    style_id: str | None
    hidden_value: str | None
    comment: str | None

    def __init__(
        self,
        sheet: XLSXSheet,
        row: int,
        column: int,
        value: str | None,
    ) -> None:
        """Инициализация"""
        ...

    @final
    def set_value(self, value: str) -> None:
        """Метод для добавления значения ячейки."""
        ...

    @final
    def set_hidden_value(self, value: str) -> None:
        """Метод для добавления скрытого значения ячейки."""
        ...

    @final
    def set_comment(self, value: str) -> None:
        """Метод для добавления комментария ячейки."""
        ...

    @final
    def set_value_number(self, value: float) -> None:
        """Метод для добавления значения ячейки Numbers."""
        ...

    @final
    def set_value_bool(self, value: bool) -> None:
        """Метод для добавления значения ячейки Bool."""
        ...

    @final
    def set_value_str(self, value: str) -> None:
        """Метод для добавления значения ячейки String."""
        ...

    @final
    def set_value_datetime(self, value: datetime) -> None:
        """Метод для добавления значения ячейки Datetime."""
        ...

    @final
    def set_formula(self, value: str) -> None:
        """Метод для добавления формулы ячейки String."""
        ...

    @final
    def set_data_type(self, value: Literal["s", "n", "d", "b"]) -> None:
        """Метод для добавления значения ячейки data_type."""
        ...

    @final
    def set_number_format(self, value: str) -> None:
        """Метод для добавления значения ячейки number_format."""
        ...

    @final
    def is_formula(self) -> bool:
        """Метод для получения флага, ячейка с формулой или нет."""
        ...

    @final
    def is_value_bool(self) -> bool:
        """Проверить, является ли значение ячейки boolean"""
        ...

    @final
    def is_value_numeric(self) -> bool:
        """Проверить, является ли значение ячейки numeric"""
        ...

    @final
    def is_value_datetime(self) -> bool:
        """Проверить, является ли значение ячейки datetime"""
        ...

    @final
    def is_value_empty(self) -> bool:
        """Проверить, является ли значение ячейки empty"""
        ...

    @final
    def set_style_id(self, value: str) -> None:
        """Метод для добавления стиля к ячейки"""
        ...

class XLSXSheetRead:
    """Тип данных листа с которыми работает парсер."""

    name: str
    max_row: int
    max_column: int
    index: int
    cells: Sequence[XLSXSheetCellRead]

    @final
    def find_cell_by_pattern_regex(self, pattern: str) -> XLSXSheetCellRead | None:
        """Функция для поиска ячейки при помощи регулярных выражений."""
        ...

    @final
    def find_cells_by_pattern_regex(self, pattern: str) -> Sequence[XLSXSheetCellRead]:
        """Функция для поиска ячеек при помощи регулярных выражений."""
        ...

    @final
    def find_cells_for_rows_pattern_regex(
        self, pattern: str, column_stop: int | None = None
    ) -> Sequence[XLSXSheetCellRead]:
        """Функция поиска ячейеек колонок для строк которые соответствуют патерну."""
        ...

    @final
    def find_cells_for_cols_pattern_regex(
        self, pattern: str, row_stop: int | None = None
    ) -> Sequence[XLSXSheetCellRead]:
        """Функция поиска ячейеек строк для колонок которые соответствуют патерну."""
        ...

    @final
    def find_cells_multi_pattern_regex(
        self,
        pattern_1: str,
        pattern_2: str,
    ) -> Sequence[XLSXSheetCellRead]:
        """Функция для поиска ячеек при помощи регулярных выражений."""
        ...

    @final
    def find_cell_by_cell(self, cell: str) -> XLSXSheetCellRead | None:
        """Функция для получения ячейки по cell (A1)."""
        ...

    @final
    def find_cell_by_coords(self, row: int, col: int) -> XLSXSheetCellRead | None:
        """Функция для ячейки по координатам."""
        ...

    @final
    def find_cells_between_patterns(
        self,
        pattern_after: str,
        pattern_before: str,
    ) -> Sequence[XLSXSheetCellRead]:
        """Метод ищет ячейки между двумя патернами."""
        ...

    @final
    def find_cells_by_range_rows(
        self,
        start_row: int,
        end_row: int,
    ) -> Sequence[XLSXSheetCellRead]:
        """Возвращаем все ячейки, которые находятся в диапазоне строк"""
        ...

    @final
    def find_cells_by_range_cols(
        self,
        start_col: int,
        end_col: int,
    ) -> Sequence[XLSXSheetCellRead]:
        """Возвращаем все ячейки, которые находятся в диапазоне колонок"""
        ...

    @final
    def iter_cells(
        self,
        min_row: int | None = None,
        max_row: int | None = None,
        min_col: int | None = None,
        max_col: int | None = None,
    ) -> Sequence[XLSXSheetCellRead]:
        """Получить список всех ячеек в заданном диапазоне."""
        ...

class XLSXSheetCellRead:
    """Тип данных ячеек листа с которыми работает парсер."""

    row: int
    column: int
    cell: str
    value: Any | None
    formula: str | None
    data_type: str
    number_format: str
    is_merge: bool
    start_column: int | None
    end_column: int | None
    start_row: int | None
    end_row: int | None
    style_id: str | None
    hidden_value: str | None
    comment: str | None

    @final
    def is_formula(self) -> bool:
        """Метод для получения флага, ячейка с формулой или нет."""
        ...

    @final
    def is_value_bool(self) -> bool:
        """Проверить, является ли значение ячейки boolean"""
        ...

    @final
    def is_value_numeric(self) -> bool:
        """Проверить, является ли значение ячейки numeric"""
        ...

    @final
    def is_value_datetime(self) -> bool:
        """Проверить, является ли значение ячейки datetime"""
        ...

    @final
    def is_value_empty(self) -> bool:
        """Проверить, является ли значение ячейки empty"""
        ...

class HelperCell:
    """Утилита по работе со списком ячеек."""

    @final
    @staticmethod
    def find_cell_by_pattern_regex(
        pattern: str, cells: Sequence[XLSXSheetCellRead]
    ) -> XLSXSheetCellRead | None:
        """Функция для поиска ячейки при помощи регулярных выражений."""
        ...

    @final
    @staticmethod
    def find_cells_by_pattern_regex(
        pattern: str, cells: Sequence[XLSXSheetCellRead]
    ) -> Sequence[XLSXSheetCellRead]:
        """Функция для поиска ячеек при помощи регулярных выражений."""
        ...

    @final
    @staticmethod
    def find_cells_for_rows_pattern_regex(
        pattern: str, cells: Sequence[XLSXSheetCellRead], colunm_stop: int | None = None
    ) -> Sequence[XLSXSheetCellRead]:
        """Функция поиска ячейеек колонок для строк которые соответствуют патерну."""
        ...

    @final
    @staticmethod
    def find_cells_for_cols_pattern_regex(
        pattern: str, cells: Sequence[XLSXSheetCellRead], row_stop: int | None = None
    ) -> Sequence[XLSXSheetCellRead]:
        """Функция поиска ячейеек строк для колонок которые соответствуют патерну."""
        ...

    @final
    @staticmethod
    def find_cells_multi_pattern_regex(
        pattern_1: str, pattern_2: str, cells: Sequence[XLSXSheetCellRead]
    ) -> Sequence[XLSXSheetCellRead]:
        """Функция для поиска ячеек при помощи регулярных выражений."""
        ...

    @final
    @staticmethod
    def find_cell_by_cell(
        cell: str, cells: Sequence[XLSXSheetCellRead]
    ) -> XLSXSheetCellRead | None:
        """Функция для получения ячейки по cell (A1)."""
        ...

    @final
    @staticmethod
    def find_cell_by_coords(
        row: int, col: int, cells: Sequence[XLSXSheetCellRead]
    ) -> XLSXSheetCellRead | None:
        """Функция для ячейки по координатам."""
        ...

    @final
    @staticmethod
    def find_cells_between_patterns(
        pattern_1: str, pattern_2: str, cells: Sequence[XLSXSheetCellRead]
    ) -> Sequence[XLSXSheetCellRead]:
        """Метод ищет ячейки между двумя патернами."""
        ...

    @final
    @staticmethod
    def iter_cells(
        min_row: int | None,
        max_row: int | None,
        min_col: int | None,
        max_col: int | None,
        cells: Sequence[XLSXSheetCellRead],
    ) -> Sequence[XLSXSheetCellRead]:
        """Получить список всех ячеек в заданном диапазоне."""
        ...

    @final
    @staticmethod
    def find_cells_by_range_rows(
        start_row: int,
        end_row: int,
        cells: Sequence[XLSXSheetCellRead],
    ) -> Sequence[XLSXSheetCellRead]:
        """Возвращаем все ячейки, которые находятся в диапазоне строк."""
        ...

    @final
    @staticmethod
    def find_cells_by_range_cols(
        start_col: int,
        end_col: int,
        cells: Sequence[XLSXSheetCellRead],
    ) -> Sequence[XLSXSheetCellRead]:
        """Возвращаем все ячейки, которые находятся в диапазоне колонок."""
        ...

class HelperSheet:
    """Парсер"""

    def __init__(self: Self, sheets: Sequence[Any]) -> None:
        """
        Инициализация парсера
        """

    @property
    def sheets(self: Self) -> list[XLSXSheetRead]:
        """
        Данный метод позволяет получить список листов в парсере
        """
        ...
    @final
    def find_sheet_by_name(self: Self, name: str) -> XLSXSheetRead | None:
        """
        Данный метод позволяет сделать поиск по названию листа
        """
        ...

    @final
    def find_sheet_by_pattern(self, pattern: str) -> XLSXSheetRead | None:
        """
        Данный метод позволяет сделать поиск листа по шаблону regex
        """
        ...

    @final
    def find_sheet_by_index(self, idx: int) -> XLSXSheetRead | None:
        """
        Данный метод позволяет сделать поиск по индексу листа
        """
        ...

    @final
    def get_sheets_without_names(
        self, name_list: Sequence[str]
    ) -> Sequence[XLSXSheetRead]:
        """Метод для получения списка листов, исключая передаваесый список."""
        ...

    @final
    def get_sheets_with_names(
        self, name_list: Sequence[str]
    ) -> Sequence[XLSXSheetRead]:
        """Метод для получения списка листов, передаваесых названий в параметрах."""
        ...

class Service(ABC):
    """Сервис"""

    uow: Any

    def __init__(self: Self, uow: Any) -> None:
        """
        Инициализация парсера
        """
        ...

    @abstractmethod
    def summary_0(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    def summary_1(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    def summary_2(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    def summary_3(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    def summary_4(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    def summary_5(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    def summary_6(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    def summary_7(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    def summary_8(self: Self, sheets: Sequence[Any], /, **kwargs: Any) -> Any:
        """
        Данный метод для реализации генерации данных сервиса
        """
        ...

    @abstractmethod
    def fmt_0(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

    def fmt_1(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

    def fmt_2(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

    def fmt_3(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

    def fmt_4(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

    def fmt_5(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

    def fmt_6(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

    def fmt_7(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

    def fmt_8(self: Self, book: XLSXBook, /, **kwargs: Any) -> Any:
        """
        Данный метод для форматирования отчета сервиса.
        """
        ...

def column_number_to_letter(column: int) -> str:
    """Функция для преобразования номера колонки в букву"""
    ...

def get_letter_coordinate(row: int, column: int) -> str:
    """Функция для получения координаты ячейки в стиле A1"""
    ...

def version() -> str:
    """Для получения версии"""
    ...

__all__ = (
    "XLSXBook",
    "XLSXSheet",
    "XLSXSheetCell",
    "XLSXSheetRead",
    "XLSXSheetCellRead",
    "HelperSheet",
    "HelperCell",
    "Service",
    "column_number_to_letter",
    "get_letter_coordinate",
    "version",
)
