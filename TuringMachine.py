# TuringMachine.py
"""
Реализация детерминированной машины Тьюринга.

Класс TuringMachine предоставляет функциональность для:
- Загрузки и сохранения конфигураций
- Пошагового выполнения программы
- Отката изменений
- Валидации переходов
"""

from constants import *
import json


class TuringMachineError(Exception):
    """Базовое исключение для всех ошибок машины Тьюринга."""
    pass


class InvalidStateError(TuringMachineError):
    """Исключение при переходе в несуществующее состояние."""

    def __init__(self, state_name=""):
        super().__init__(f"Переход в несуществующее состояние {state_name}")


class NoTransitionError(TuringMachineError):
    """Исключение при отсутствии перехода для текущего символа."""

    def __init__(self, symbol=''):
        super().__init__(f"В текущем состоянии нет инструкций для символа {symbol}")


class InvalidTransitionError(TuringMachineError):
    """Исключение при некорректном формате инструкции перехода."""

    def __init__(self, state, symbol):
        super().__init__(f"Некорректная инструкция для состояния {state} символа {symbol}. "
                         f"\nФормат правильной инструкции: <новый символ> <состояние> <направление>"
                         f"\nГде направление - один из символов {Direction.ALL.value}")


class TuringMachine:
    """Основной класс, реализующий машину Тьюринга.

    Атрибуты:
        current_state: текущее состояние управления
        states: словарь переходов (state -> symbol -> Transition)
        tape: лента, представленная списком символов
        head_position: текущая позиция головки (0-based индекс)
        step_count: счетчик выполненных шагов
        saved_state: сохраненное состояние для восстановления
        symbols: множество используемых символов
        history: история состояний для реализации отката
    """

    def __init__(self):
        """Инициализация машины Тьюринга с начальными значениями."""
        self.current_state: str = 'q0'
        self.states: dict = {'q0': {}}  # state -> symbol -> Transition
        self.tape: list = [BLANK_SYMBOL]
        self.head_position: int = LEFT_END
        self.step_count: int = 0
        self.saved_state: StateInfo = None
        self.symbols = {BLANK_SYMBOL}
        self.history = []

    def new_transition(self, state: str, symbol: str, instruction: str):
        """Добавляет или заменяет переход в таблице переходов.

        Args:
            state: исходное состояние
            symbol: читаемый символ
            instruction: строка инструкции в формате "символ состояние направление"

        Raises:
            InvalidTransitionError: если инструкция имеет некорректный формат
        """
        try:
            transition = Transition.from_str(instruction)
            self.states.setdefault(state, {})[symbol] = transition
            self.symbols.add(symbol)
        except Exception as e:
            raise InvalidTransitionError(state, symbol)

    def set_tape(self, s: list):
        """Устанавливает новое содержимое ленты.

        Args:
            s: список символов для ленты
        """
        self.tape = s or [BLANK_SYMBOL]
        self.current_state = 'q0'
        self.head_position = LEFT_END

    def _move_head(self, direction: Direction):
        """Перемещает головку в заданном направлении, расширяя ленту при необходимости."""
        self.head_position += direction.to_int

        # Расширение ленты влево при достижении начала
        if self.head_position == -1:
            self.tape.insert(0, BLANK_SYMBOL)
            self.head_position = LEFT_END

        # Расширение ленты вправо при достижении конца
        if self.head_position == len(self.tape):
            self.tape.append(BLANK_SYMBOL)

    def _set_state(self, state: str):
        """Устанавливает новое состояние машины с проверкой его существования."""
        if state not in self.states:
            raise InvalidStateError(state)
        self.current_state = state

    def run_transition(self):
        """Выполняет один шаг машины Тьюринга.

        Returns:
            0 если машина останавливается, 1 если может продолжать

        Raises:
            NoTransitionError: если нет перехода для текущего символа
        """
        symbol = self.current_symbol

        if symbol not in self.states[self.current_state]:
            raise NoTransitionError(symbol)

        # Сохраняем текущее состояние в истории
        self.history.append(self.get_state_info())
        if len(self.history) > MAX_HISTORY_LEN:
            self.history.pop(0)

        # Выполняем инструкцию перехода
        instruction: Transition = self.states[self.current_state][symbol]
        self.tape[self.head_position] = instruction.write_symbol
        self._set_state(instruction.next_state)
        self.step_count += 1

        # Проверяем не является ли переход остановочным
        if instruction.direction == Direction.STOP:
            return 0

        self._move_head(instruction.direction)
        return 1

    def run(self):
        """Выполняет программу до завершения (остановки машины)."""
        while self.run_transition():
            pass

    def get_state_info(self):
        """Возвращает объект StateInfo с текущим состоянием машины."""
        return StateInfo(
            self.current_state,
            self.head_position,
            self.tape.copy(),
            self.step_count
        )

    def save_to_file(self, filename: str):
        """Сохраняет текущую конфигурацию машины в JSON файл."""
        data = {
            'tape': self.tape,
            'states': {
                state_name: {
                    symbol: transition.to_str() for symbol, transition in state.items()
                } for state_name, state in self.states.items()
            }
        }
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def load_from_file(cls, filename: str):
        """Загружает конфигурацию машины из JSON файла."""
        with open(filename, 'r') as f:
            data = json.load(f)

        machine = cls()
        machine.set_tape(data['tape'])

        # Восстанавливаем таблицу переходов
        for state_name, state in data['states'].items():
            for symbol, transition in state.items():
                machine.new_transition(state_name, symbol, transition)

        return machine

    def save_tape(self):
        """Сохраняет текущее состояние ленты и позиции головки."""
        self.saved_state = self.get_state_info()

    def load_tape(self):
        """Восстанавливает ранее сохраненное состояние ленты."""
        if self.saved_state:
            self.head_position = self.saved_state.head_position
            self.tape = self.saved_state.tape.copy()
            self.current_state = self.saved_state.current_state
            self.step_count = self.saved_state.step_count

    def get_symbols(self):
        """Возвращает отсортированный список всех используемых символов."""
        return sorted(self.symbols, key=lambda x: ord(x) if x != '_' else -1)

    def get_states(self):
        """Возвращает список всех состояний машины."""
        return list(self.states.keys())

    def step_back(self):
        """Откатывает машину на один шаг назад используя историю.

        Returns:
            1 если откат выполнен, 0 если история пуста
        """
        if self.history:
            prev: StateInfo = self.history.pop()
            self.head_position = prev.head_position
            self.tape = prev.tape.copy()
            self.current_state = prev.current_state
            self.step_count = prev.step_count
            return 1
        return 0

    @property
    def current_symbol(self):
        """Возвращает символ под текущей позицией головки."""
        return self.tape[self.head_position]