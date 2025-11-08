# constants.py
"""
Модуль с константами и базовыми классами для машины Тьюринга.

Содержит:
- Исключения для обработки ошибок машины Тьюринга
- Перечисление направлений движения головки
- Классы для представления переходов и состояния машины
- Базовые константы
"""

from enum import Enum
from dataclasses import dataclass
from typing import List


class InvalidDirectionError(Exception):
    """Исключение при указании недопустимого направления движения."""

    def __init__(self, direction=''):
        super().__init__(f"""Направления {direction} не может существовать! 
        Допустимые направления: {Direction.ALL.value}""")


class Direction(Enum):
    """Перечисление допустимых направлений движения головки машины Тьюринга."""

    LEFT = '<'
    RIGHT = '>'
    STOP = '!'
    STAY = '.'
    ALL = [LEFT, RIGHT, STOP, STAY]
    _VALUE_INT_MAPPING = {LEFT: -1, RIGHT: 1, STAY: 0, STOP: 0}

    @property
    def to_int(self):
        """Возвращает числовое представление направления (-1, 0, 1)."""
        return Direction._VALUE_INT_MAPPING.value[self.value]


@dataclass
class Transition:
    """Класс, представляющий переход машины Тьюринга.

    Атрибуты:
        next_state: следующее состояние
        write_symbol: символ для записи на ленту
        direction: направление движения головки
    """

    next_state: str
    write_symbol: str
    direction: Direction

    def to_str(self):
        """Преобразует переход в строковое представление."""
        return f'{self.write_symbol} {self.next_state} {self.direction.value}'

    @classmethod
    def from_str(cls, data: str):
        """Создает объект Transition из строки."""
        symbol, state, direction = data.strip().split()
        if direction not in Direction.ALL.value:
            raise InvalidDirectionError
        direction = Direction(direction)
        return cls(
            next_state=state,
            write_symbol=symbol,
            direction=direction
        )


@dataclass
class StateInfo:
    """Класс для хранения полного состояния машины Тьюринга в определенный момент.

    Используется для отката изменений и отображения истории.
    """

    current_state: str
    head_position: int
    tape: List[str]
    step_count: int


# Базовые константы машины Тьюринга
BLANK_SYMBOL = '_'  # Символ пустой ячейки
LEFT_END = 0  # Начальная позиция головки
MAX_HISTORY_LEN = 1000  # Максимальная глубина истории для отката
