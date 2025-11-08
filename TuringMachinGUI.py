# TuringMachinGUI.py
"""
Графический интерфейс для машины Тьюринга.

Предоставляет визуальный редактор таблицы переходов, 
визуализацию ленты и управления выполнением программы.
"""

import tkinter as tk
import os
from tkinter import ttk, messagebox, simpledialog, filedialog
from TuringMachine import *


class TransitionTableEditor:
    """Редактор таблицы переходов машины Тьюринга.

    Позволяет визуально редактировать состояния, символы и переходы.
    """

    def __init__(self, parent, machine: TuringMachine):
        self.machine = machine
        self.frame = ttk.LabelFrame(parent, text="Таблица переходов", padding="5")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Панель управления таблицей
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, pady=5)

        ttk.Button(control_frame, text="Add state",
                   command=self.add_state).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Add symbol",
                   command=self.add_symbol).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Apply table",
                   command=self.apply_transitions).pack(side=tk.LEFT, padx=30)

        # Контейнер для таблицы с прокруткой
        table_container = ttk.Frame(self.frame)
        table_container.pack(fill=tk.BOTH, expand=True)

        # Настройка canvas и скроллбаров
        self.canvas = tk.Canvas(table_container, bg='white')

        # Вертикальный скроллбар
        self.v_scrollbar = ttk.Scrollbar(table_container, orient="vertical",
                                         command=self.canvas.yview)
        # Горизонтальный скроллбар
        self.h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal",
                                         command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set,
                              xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Фрейм таблицы внутри canvas
        self.table_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Привязка событий для корректной работы прокрутки
        self.table_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Поддержка прокрутки колесиком мыши
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)
        self.canvas.bind("<Button-5>", self.on_mousewheel)
        # Горизонтальная прокрутка с Shift+колесико
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)
        self.canvas.bind("<Shift-Button-4>", self.on_shift_mousewheel)
        self.canvas.bind("<Shift-Button-5>", self.on_shift_mousewheel)

        # Инициализация данных
        self.states = machine.get_states()
        self.symbols = machine.get_symbols()
        self.cells = {}

        self.root = parent
        self.root.after(100, self.create_table)

    def on_frame_configure(self, event):
        """Обновляет область прокрутки при изменении размера фрейма."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Обновляет размер окна canvas при изменении размера виджета."""
        # Обновляем ширину внутреннего фрейма под размер canvas
        pass
        # Не устанавливаем высоту, чтобы фрейм мог быть выше canvas (для вертикальной прокрутки)

    def on_mousewheel(self, event):
        """Обрабатывает прокрутку колесиком мыши (вертикальная)."""
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def on_shift_mousewheel(self, event):
        """Обрабатывает горизонтальную прокрутку с Shift+колесико."""
        if event.delta:
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 4:
                self.canvas.xview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.xview_scroll(1, "units")

    def create_table(self, table=None):
        """Создает или пересоздает таблицу переходов."""
        # Очистка предыдущей таблицы
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.cells = {}

        # Заголовки символов (горизонтальные)
        for col, symbol in enumerate(self.symbols):
            label = ttk.Label(self.table_frame, text=symbol, borderwidth=1, relief="solid",
                              background="lightgray", width=10)
            label.grid(row=0, column=col + 1, sticky="nsew", padx=1, pady=1)

        # Состояния и ячейки переходов
        for row, state in enumerate(self.states):
            # Заголовок состояния
            state_label = ttk.Label(self.table_frame, text=state, borderwidth=1, relief="solid",
                                    background="lightblue", width=8)
            state_label.grid(row=row + 1, column=0, sticky="nsew", padx=1, pady=1)

            # Ячейки для каждого символа
            for col, symbol in enumerate(self.symbols):
                entry = tk.Entry(self.table_frame, width=10, justify='center')
                entry.grid(row=row + 1, column=col + 1, sticky="nsew", padx=1, pady=1)

                # Заполнение существующих переходов
                if state in self.machine.states and symbol in self.machine.states[state]:
                    trans = self.machine.states[state][symbol]
                    entry.insert(0, f"{trans.write_symbol} {trans.next_state} {trans.direction.value}")

                self.cells[(state, symbol)] = entry

        # Настройка весов строк и столбцов для правильного растягивания
        for i in range(len(self.states) + 1):
            self.table_frame.grid_rowconfigure(i, weight=1)
        for i in range(len(self.symbols) + 1):
            self.table_frame.grid_columnconfigure(i, weight=1)

        # Обновление области прокрутки
        self.table_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_state(self):
        """Добавляет новое состояние в таблицу."""
        state_name = simpledialog.askstring("Новое состояние", "Введите название для состояния:")
        if not state_name:
            # Генерация имени состояния по умолчанию (q1, q2, ...)
            max_num = 0
            for state in self.states:
                if state.startswith('q'):
                    try:
                        num = int(state[1:])
                        max_num = max(max_num, num)
                    except ValueError:
                        pass
            new_state = f'q{max_num + 1}'
        else:
            new_state = state_name

        if new_state not in self.states:
            self.states.append(new_state)
            self.create_table()

    def add_symbol(self):
        """Добавляет новый символ в таблицу."""
        symbol = simpledialog.askstring("Новый символ", "Введите новый символ:")
        if symbol and symbol not in self.symbols:
            self.symbols.append(symbol)
            self.create_table()

    def apply_transitions(self):
        """Применяет изменения из таблицы к машине Тьюринга."""
        try:
            self.machine.states = {}  # Очистка текущих переходов

            for (state, symbol), entry in self.cells.items():
                value = entry.get().strip()
                if value:  # Только для непустых ячеек
                    self.machine.new_transition(state, symbol, value)

            messagebox.showinfo("Успех", "Переходы применены!")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def highlight_active_state(self, active_state):
        """Подсвечивает активное состояние в таблице."""
        for widget in self.table_frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.grid_info()["column"] == 0:
                state_name = widget.cget("text")
                bg_color = "lightgreen" if state_name == active_state else "lightblue"
                widget.configure(background=bg_color)


class TuringMachineGUI:
    """Главный класс графического интерфейса машины Тьюринга.

    Координирует взаимодействие между визуальными компонентами
    и логикой машины Тьюринга.
    """

    def __init__(self):
        self.machine = TuringMachine()
        self.root = tk.Tk()
        self.root.title("Машина Тьюринга - Редактор")
        self.root.geometry("900x700")

        self.setup_ui()
        self.is_running = False
        self.update_display()

    def setup_ui(self):
        """Создает и размещает все элементы интерфейса."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Панель информации о состоянии
        info_frame = ttk.LabelFrame(main_frame, text="Состояние", padding="5")
        info_frame.pack(fill=tk.X, pady=5)

        self.state_label = ttk.Label(info_frame, text="Состояние: q0")
        self.state_label.pack(side=tk.LEFT, padx=5)

        self.step_label = ttk.Label(info_frame, text="Шаг: 0")
        self.step_label.pack(side=tk.LEFT, padx=20)

        # Визуализация ленты с прокруткой
        tape_frame = ttk.LabelFrame(main_frame, text="Лента", padding="10")
        tape_frame.pack(fill=tk.X, pady=5)

        # Контейнер для ленты с прокруткой
        tape_container = ttk.Frame(tape_frame)
        tape_container.pack(fill=tk.BOTH, expand=True)

        # Canvas для ленты с горизонтальным скроллбаром
        self.tape_canvas = tk.Canvas(tape_container, height=80, bg='white')
        self.tape_scrollbar = ttk.Scrollbar(tape_container, orient="horizontal",
                                            command=self.tape_canvas.xview)
        self.tape_canvas.configure(xscrollcommand=self.tape_scrollbar.set)

        self.tape_scrollbar.pack(side="bottom", fill="x")
        self.tape_canvas.pack(side="top", fill="both", expand=True)

        # Панель управления выполнением
        exec_frame = ttk.Frame(main_frame)
        exec_frame.pack(fill=tk.X, pady=10)

        # Кнопки пошагового выполнения
        steps_frame = ttk.Frame(exec_frame)
        steps_frame.pack(side=tk.LEFT, padx=5)
        ttk.Button(steps_frame, text="Step", command=self.step).pack(pady=(0, 2))
        ttk.Button(steps_frame, text="Step Back", command=self.step_back).pack(pady=(2, 0))

        # Основные кнопки управления
        ttk.Button(exec_frame, text="Run/Pause", command=self.toggle_run).pack(side=tk.LEFT, padx=5)
        ttk.Button(exec_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        ttk.Button(exec_frame, text="Set new tape", command=self.create_tape_dialog).pack(side=tk.LEFT, padx=5)

        # Операции с программой
        program_frame = ttk.Frame(exec_frame)
        program_frame.pack(side=tk.LEFT, padx=40)
        ttk.Button(program_frame, text='Save to disk', command=self.save_machine).pack(pady=(0, 2))
        ttk.Button(program_frame, text='Load from disk', command=self.load_machine).pack(pady=(2, 0))

        # Операции с лентой
        tape_ops_frame = ttk.Frame(exec_frame)
        tape_ops_frame.pack(side=tk.LEFT, padx=5)
        ttk.Button(tape_ops_frame, text='Save moment', command=self.save_tape).pack(pady=(0, 2))
        ttk.Button(tape_ops_frame, text='Load moment', command=self.load_tape).pack(pady=(2, 0))

        # Выбор скорости выполнения
        speed_frame = ttk.Frame(exec_frame)
        speed_frame.pack(side=tk.LEFT, padx=20)
        ttk.Label(speed_frame, text='Choose your speed').pack(pady=(0, 2))
        self.speed = ttk.Combobox(speed_frame, values=['1', '2', '3', '4', '5'])
        self.speed.set('3')
        self.speed.pack(pady=(2, 0))

        # Редактор таблицы переходов
        self.table_editor = TransitionTableEditor(main_frame, self.machine)

    def draw_tape(self, tape, head_pos):
        """Отрисовывает текущее состояние ленты на canvas."""
        self.tape_canvas.delete("all")

        cell_width = 50
        start_x = 50
        total_width = max(800, len(tape) * cell_width + 100)  # Минимальная ширина + запас

        # Устанавливаем область прокрутки
        self.tape_canvas.configure(scrollregion=(0, 0, total_width, 80))

        # Отрисовка ячеек ленты
        for i, symbol in enumerate(tape):
            x = start_x + i * cell_width
            if symbol == BLANK_SYMBOL:
                symbol = ''
            # Выделение текущей ячейки под головкой
            if i == head_pos:
                self.tape_canvas.create_rectangle(x, 20, x + cell_width, 50,
                                                  fill='lightblue', outline='black')
            else:
                self.tape_canvas.create_rectangle(x, 20, x + cell_width, 50,
                                                  fill='white', outline='black')

            # Символ в ячейке
            self.tape_canvas.create_text(x + cell_width / 2, 35, text=str(symbol),
                                         font=('Arial', 14))

        # Отрисовка головки машины
        head_x = start_x + head_pos * cell_width + cell_width / 2
        self.tape_canvas.create_polygon(
            head_x - 10, 10, head_x + 10, 10, head_x, 20,
            fill='red', outline='black'
        )

        # Автоматическая прокрутка к текущей позиции головки
        self.scroll_to_head(head_pos, cell_width, start_x)

    def scroll_to_head(self, head_pos, cell_width, start_x):
        """Прокручивает ленту к текущей позиции головки."""
        head_center_x = start_x + head_pos * cell_width + cell_width / 2
        canvas_width = self.tape_canvas.winfo_width()

        # Получаем текущую видимую область
        xview = self.tape_canvas.xview()
        visible_start = xview[0] * self.tape_canvas.bbox("all")[2]  # Начало видимой области
        visible_end = xview[1] * self.tape_canvas.bbox("all")[2]  # Конец видимой области

        # Если головка не в видимой области, прокручиваем к ней
        if head_center_x < visible_start or head_center_x > visible_end:
            # Вычисляем новую позицию прокрутки (центрируем головку)
            new_start = max(0, head_center_x - canvas_width / 2)
            # Нормализуем позицию для xview_moveto
            total_width = self.tape_canvas.bbox("all")[2]
            normalized_pos = new_start / total_width if total_width > 0 else 0
            self.tape_canvas.xview_moveto(normalized_pos)

    def update_display(self):
        """Обновляет все элементы отображения состояния машины."""
        info: StateInfo = self.machine.get_state_info()
        self.state_label.config(text=f"State: {info.current_state}")
        self.step_label.config(text=f"Steps_done: {info.step_count}")
        self.draw_tape(info.tape, info.head_position)
        self.table_editor.highlight_active_state(info.current_state)

    def step(self):
        """Выполняет один шаг машины Тьюринга."""
        try:
            if self.machine.run_transition():
                self.update_display()
            else:
                messagebox.showinfo("Done", "Machine successfully stopped!")
                self.is_running = False
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def step_back(self):
        """Откатывает машину на один шаг назад."""
        self.is_running = False
        try:
            if self.machine.step_back():
                self.update_display()
            else:
                messagebox.showinfo("Невозможно", "Никаких шагов ранее не было!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def toggle_run(self):
        """Включает/выключает автоматическое выполнение машины."""
        if not self.is_running:
            self.is_running = True
            self.auto_run()
        else:
            self.is_running = False

    def auto_run(self):
        """Автоматически выполняет шаги машины с заданной скоростью."""
        if self.is_running:
            try:
                if self.machine.run_transition():
                    self.update_display()
                    speed = int(self.speed.get()) if self.speed.get() else 3
                    self.root.after(2100 - 400 * speed, self.auto_run)
                else:
                    messagebox.showinfo("Done", "Machine successfulle stoped!")
                    self.is_running = False
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.is_running = False

    def reset(self):
        """Сбрасывает машину в начальное состояние, сохраняя таблицу переходов."""
        # Сохранение текущей конфигурации таблицы
        current_states = self.table_editor.states.copy()
        current_symbols = self.table_editor.symbols.copy()

        # Создание новой машины
        self.machine = TuringMachine()

        # Восстановление таблицы
        self.table_editor.states = current_states
        self.table_editor.symbols = current_symbols
        self.table_editor.create_table()

        self.is_running = False
        self.update_display()

    def create_tape_dialog(self):
        """Диалоговое окно для создания новой ленты."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Создать ленту")
        dialog.geometry("300x150")

        ttk.Label(dialog, text="Введите символы ленты:").pack(pady=10)

        tape_entry = ttk.Entry(dialog, width=30)
        tape_entry.pack(pady=5)
        tape_entry.insert(0, "01010")  # Значение по умолчанию

        def apply_tape():
            """Обработчик применения новой ленты."""
            try:
                tape_symbols = list(tape_entry.get())
                self.machine.set_tape(tape_symbols)
                self.update_display()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        ttk.Button(dialog, text="Ok", command=apply_tape).pack(pady=10)

    def save_machine(self):
        """Сохраняет текущую программу машины в файл."""
        filename = filedialog.asksaveasfilename(
            title="Сохранить программу",
            defaultextension=".tur",
            filetypes=[("Turing machine files", "*.tur"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )

        if not filename:
            return

        try:
            self.machine.save_to_file(filename)
            messagebox.showinfo("Success", f"Программа сохранена в файл:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Не удалось сохранить файл:\n{str(e)}")

    def save_tape(self):
        """Сохраняет текущее состояние ленты."""
        self.machine.save_tape()

    def load_machine(self):
        """Загружает программу машины из файла."""
        filename = filedialog.askopenfilename(
            title="Загрузить программу",
            filetypes=[("Turing machine files", "*.tur"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )

        if not filename:
            return

        try:
            self.machine = TuringMachine.load_from_file(filename)

            # Обновление редактора таблицы
            self.table_editor.machine = self.machine
            self.table_editor.states = self.machine.get_states()
            self.table_editor.symbols = self.machine.get_symbols()
            self.table_editor.create_table()

            self.update_display()
            messagebox.showinfo("Success", f"Программа загружена из файла:\n{filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Не удалось загрузить файл:\n{str(e)}")

    def load_tape(self):
        """Загружает ранее сохраненное состояние ленты."""
        self.machine.load_tape()
        self.update_display()