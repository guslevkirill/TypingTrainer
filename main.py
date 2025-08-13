import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from words import words
from punctuation import punctuation


class TypingTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренажёр печати v.1.0 (test)")
        self.root.geometry("800x600")

        # Настройки
        self.test_duration = 0
        self.time_left = 0
        self.start_time = 0
        self.mode = None
        self.word_count = 30
        self.current_text = ""
        self.user_input = ""
        self.words_typed = 0
        self.test_active = False

        # Слова для тренировки
        self.words = words
        self.punctuation = punctuation

        # Настройка стилей
        self.setup_styles()
        self.setup_selection_screen()

    def setup_styles(self):
        """Настройка стилей для виджетов ttk"""
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12), padding=10)
        style.configure("TRadiobutton", font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))

    def setup_selection_screen(self):
        """Параметры"""
        self.clear_screen()
        self.test_active = False

        # Выбор времени
        time_label = ttk.Label(self.root, text="Выберите время (секунды):")
        time_label.pack(pady=5)

        self.time_var = tk.IntVar(value=30)
        time_combobox = ttk.Combobox(
            self.root,
            textvariable=self.time_var,
            values=[10, 30, 60, 120],
            state="readonly"
        )
        time_combobox.pack(pady=5)

        # Выбор количества слов
        word_count_label = ttk.Label(self.root, text="Выберите количество слов:")
        word_count_label.pack(pady=5)

        self.word_count_var = tk.IntVar(value=30)
        word_count_combobox = ttk.Combobox(
            self.root,
            textvariable=self.word_count_var,
            values=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            state="readonly"
        )
        word_count_combobox.pack(pady=5)

        # Выбор режима
        mode_label = ttk.Label(self.root, text="Выберите режим печати:")
        mode_label.pack(pady=10)

        self.mode_var = tk.StringVar(value="words")
        words_radio = ttk.Radiobutton(
            self.root,
            text="Только слова",
            variable=self.mode_var,
            value="words"
        )
        words_radio.pack()

        punctuation_radio = ttk.Radiobutton(
            self.root,
            text="Слова и знаки препинания",
            variable=self.mode_var,
            value="punctuation"
        )
        punctuation_radio.pack()

        # Кнопка старта
        start_button = ttk.Button(
            self.root,
            text="Начать",
            command=self.start_typing_test,
            style="Accent.TButton"
        )
        start_button.pack(pady=20)

    def start_typing_test(self):
        """Запускает тест на печать"""
        self.test_duration = self.time_var.get()
        self.time_left = self.test_duration
        self.word_count = self.word_count_var.get()
        self.mode = self.mode_var.get()
        self.current_text = self.generate_text()
        self.user_input = ""
        self.words_typed = 0
        self.test_active = True
        self.clear_screen()
        self.setup_typing_screen()

        # Запуск таймера
        self.start_time = time.time()
        self.update_timer()

    def generate_text(self):
        """Генерируем текст для печати"""
        selected_words = random.choices(self.words, k=self.word_count)

        if self.mode == "punctuation":
            for i in range(len(selected_words)):
                if random.random() > 0.7:
                    selected_words[i] += random.choice(self.punctuation)

        return " ".join(selected_words)

    def setup_typing_screen(self):
        """Экран печати"""
        # Таймер
        self.timer_label = ttk.Label(
            self.root,
            text=f"Осталось: {self.time_left} сек",
            font=("Arial", 14)
        )
        self.timer_label.pack(pady=10)

        # Поле с текстом для ввода и подсветкой
        self.text_display = tk.Text(
            self.root,
            height=10,
            wrap=tk.WORD,
            font=("Courier New", 16),
            bg="#f5f5f5",
            padx=15,
            pady=15,
            spacing2=5  # Межстрочный интервал
        )
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Вставляем текст для ввода
        self.text_display.insert(tk.END, self.current_text)

        # Настройка цветов
        self.text_display.tag_config("correct", foreground="green")
        self.text_display.tag_config("wrong", foreground="red")
        self.text_display.tag_config("remaining", foreground="#555555")

        # Запрет редактирования
        self.text_display.config(state="disabled")

        # Поле ввода
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(
            self.root,
            textvariable=self.entry_var,
            font=("Courier New", 16),
            width=50
        )
        self.entry.pack(pady=10, padx=20)
        self.entry.focus()

        # Отслеживание ввода
        self.entry_var.trace_add("write", self.update_text_display)

    def update_timer(self):
        """Обновляет таймер"""
        if self.test_active:
            elapsed = time.time() - self.start_time
            self.time_left = max(0, self.test_duration - int(elapsed))
            self.timer_label.config(text=f"Осталось: {self.time_left} сек")

            # Проверяем условия завершения
            if self.time_left <= 0 or self.words_typed >= self.word_count:
                self.finish_typing_test()
            else:
                self.root.after(200, self.update_timer)

    def update_text_display(self, *args):
        """Обновляет текст с подсветкой"""
        if not self.test_active:
            return

        input_text = self.entry_var.get()
        self.words_typed = len(input_text.split())

        # Очищаем текст с подсветкой
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, tk.END)

        # Сравниваем введённый текст с образцом
        for i in range(max(len(self.current_text), len(input_text))):
            if i < len(input_text):
                if i < len(self.current_text) and input_text[i] == self.current_text[i]:
                    # Правильный символ
                    self.text_display.insert(tk.END, input_text[i], "correct")
                else:
                    # Ошибочный символ
                    self.text_display.insert(tk.END, input_text[i], "wrong")
            elif i < len(self.current_text):
                # Оставшиеся символы
                self.text_display.insert(tk.END, self.current_text[i], "remaining")

        self.text_display.config(state="disabled")
        self.text_display.see(tk.END)  # Автопрокрутка

    def finish_typing_test(self):
        """Завершаем тест и показываем статистику"""
        self.test_active = False
        elapsed_time = time.time() - self.start_time
        typed_text = self.entry_var.get()

        # Подсчёт правильных символов
        correct_chars = 0
        min_length = min(len(self.current_text), len(typed_text))
        for i in range(min_length):
            if self.current_text[i] == typed_text[i]:
                correct_chars += 1

        # Рассчёт статистики
        total_chars = len(self.current_text)
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0
        wpm = (len(typed_text.split()) / elapsed_time) * 60 if elapsed_time > 0 else 0

        # Показываем статистику
        messagebox.showinfo(
            "Результат",
            f"Тест завершен!\n\n"
            f"Слов в минуту: {wpm:.1f}\n"
            f"Точность: {accuracy:.1f}%\n"
            f"Введено слов: {self.words_typed}/{self.word_count}\n"
            f"Затраченное время: {elapsed_time:.2f} сек"
        )
        self.setup_selection_screen()

    def clear_screen(self):
        """Очищает все виджеты"""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTrainer(root)
    root.mainloop()