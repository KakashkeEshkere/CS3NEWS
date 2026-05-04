import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- 1. Список предопределённых цитат ---
QUOTES_DATABASE = [
    {"text": "Жизнь — это то, что происходит, пока ты строишь другие планы.", "author": "Джон Леннон", "theme": "жизнь"},
    {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "мотивация"},
    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "theme": "успех"},
    {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "theme": "знания"},
    {"text": "Величайшая слава не в том, чтобы никогда не ошибаться, а в том, чтобы уметь подняться каждый раз, когда падаешь.", "author": "Конфуций", "theme": "мудрость"},
    {"text": "Неудача — это просто возможность начать снова, но уже более мудро.", "author": "Генри Форд", "theme": "мотивация"},
]

# --- 2. Пути к файлам ---
HISTORY_FILE = 'quotes.json'

# --- 3. Загрузка истории из файла ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return []
    return []

# --- 4. Сохранение истории в файл ---
def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- 5. Основная логика приложения ---
class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")
        
        self.history = load_history()

        # Виджеты
        self.quote_label = tk.Label(root, text="Нажмите кнопку для генерации цитаты", wraplength=500, font=('Arial', 12), justify='center')
        self.quote_label.pack(pady=10)

        self.generate_button = tk.Button(root, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_button.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5)
        self.author_entry = tk.Entry(filter_frame)
        self.author_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5)
        self.theme_entry = tk.Entry(filter_frame)
        self.theme_entry.grid(row=0, column=3, padx=5)

        self.filter_button = tk.Button(filter_frame, text="Фильтровать", command=self.filter_quotes)
        self.filter_button.grid(row=0, column=4, padx=5)

        # История
        history_frame = tk.Frame(root)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(history_frame, text="История сгенерированных цитат:").pack()
        
        self.history_listbox = tk.Listbox(history_frame, height=10)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Заполняем историю при запуске
        for quote in self.history:
            self.history_listbox.insert(tk.END, f'"{quote["text"]}" — {quote["author"]}')

    def generate_quote(self):
        """Генерирует случайную цитату и обновляет интерфейс."""
        quote = random.choice(QUOTES_DATABASE)
        
        # Обновление отображения текущей цитаты
        self.quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]}')
        
        # Добавление в историю (в начало списка)
        self.history.insert(0, quote)
        
        # Обновление виджета истории
        self.history_listbox.insert(0, f'"{quote["text"]}" — {quote["author"]}')
        
        # Сохранение истории в файл
        save_history(self.history)

    def filter_quotes(self):
        """Фильтрует цитаты по автору и теме."""
        author_filter = self.author_entry.get().strip().lower()
        theme_filter = self.theme_entry.get().strip().lower()

        if not author_filter and not theme_filter:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите автора или тему для фильтрации.")
            return

        # Фильтрация базы данных
        filtered_quotes = [
            q for q in QUOTES_DATABASE 
            if (not author_filter or q["author"].lower() == author_filter) and 
               (not theme_filter or q["theme"].lower() == theme_filter)
        ]

        if not filtered_quotes:
            messagebox.showinfo("Результат", "Цитаты по заданным критериям не найдены.")
            return

        # Отображение результата в новом окне
        result_window = tk.Toplevel(self.root)
        result_window.title("Результаты фильтрации")
        
        for q in filtered_quotes:
            label_text = f'"{q["text"]}"\n— {q["author"]} (Тема: {q["theme"]})'
            tk.Label(result_window, text=label_text, wraplength=400, justify='left').pack(pady=5)


# --- 6. Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
