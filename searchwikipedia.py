from tkinter import *
import wikipedia
from tkinter import messagebox
import requests
import json
import time

# Русская версия запросов
wikipedia.set_lang("ru")

class SearchWiki:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для поиска и редактирования")
        self.root.geometry("1360x740+0+0")
        self.root.config(bg="#262626")

        # Название окна
        title = Label(self.root, text="Поиск и Редактор", font=("times new roman", 35, "bold"), bg="white", fg="black")
        title.place(x=0, y=0, relwidth=1, height=70)

        # Основной фрейм
        frame1 = Frame(self.root, bd=2, relief=RIDGE)
        frame1.place(x=20, y=130, width=1320, height=550)

        # Строка поиска
        self.var_search = StringVar()
        entry_word = Entry(self.root, textvariable=self.var_search, font=("times new roman", 20))
        entry_word.place(x=100, y=85, width=500, height=40)
        entry_word.bind('<Return>', lambda event: self.search_word())  # Поиск по Enter

        # Кнопки - изменены размеры и расположение
        btn_search = Button(self.root, text="Искать", command=self.search_word, 
                           font=("times new roman", 14, "bold"), bg="#404040", fg="white", relief=RAISED)
        btn_search.place(x=620, y=85, height=40, width=100)

        btn_clear = Button(self.root, text="Очистить", command=self.clear, 
                          font=("times new roman", 14, "bold"), bg="#404040", fg="white", relief=RAISED)
        btn_clear.place(x=730, y=85, height=40, width=100)

        btn_enable = Button(self.root, text="Разрешить\nредактирование", command=self.enable_editing, 
                           font=("times new roman", 12, "bold"), bg="#2E7D32", fg="white", relief=RAISED)
        btn_enable.place(x=850, y=85, height=40, width=130)

        btn_disable = Button(self.root, text="Запретить\nредактирование", command=self.disable_editing, 
                            font=("times new roman", 12, "bold"), bg="#C62828", fg="white", relief=RAISED)
        btn_disable.place(x=995, y=85, height=40, width=130)

        # Статус режима редактирования
        self.status_label = Label(self.root, text="Режим: редактирование разрешено", 
                                  font=("times new roman", 11), bg="#262626", fg="white")
        self.status_label.place(x=1140, y=92)

        # Прокручиваемое поле для вывода
        scroll_y = Scrollbar(frame1, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill="y")

        self.text_area = Text(frame1, font=("times new roman", 15), yscrollcommand=scroll_y.set, wrap=WORD)
        self.text_area.pack(fill=BOTH, expand=1)
        scroll_y.config(command=self.text_area.yview)
        
        # По умолчанию редактирование разрешено
        self.text_area.config(state=NORMAL)

    # Включить режим редактирования
    def enable_editing(self):
        self.text_area.config(state=NORMAL)
        self.status_label.config(text="Режим: редактирование разрешено", fg="#4CAF50")

    # Отключить режим редактирования
    def disable_editing(self):
        self.text_area.config(state=DISABLED)
        self.status_label.config(text="Режим: редактирование запрещено", fg="#EF5350")

    # Очистить поле ввода и область вывода
    def clear(self):
        self.var_search.set("")     # Очистить строку поиска
        self.text_area.delete('1.0', END)  # Очистить область вывода

    # Выполнить поиск по запросу с альтернативными методами
    def search_word(self):
        word = self.var_search.get().strip()
        if not word:
            messagebox.showerror("Ошибка", "Введите слово для поиска.")
            return

        # Показываем индикатор загрузки
        current_state = self.text_area.cget("state")
        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', END)
        self.text_area.insert('1.0', "Поиск... Пожалуйста, подождите.")
        if current_state == DISABLED:
            self.text_area.config(state=DISABLED)
        self.root.update()

        try:
            # Пробуем получить страницу через Wikipedia API напрямую
            result = self.get_wikipedia_page(word)
            if result:
                self.text_area.config(state=NORMAL)
                self.text_area.delete('1.0', END)
                self.text_area.insert('1.0', result)
                # Возвращаем исходное состояние редактирования
                if current_state == DISABLED:
                    self.text_area.config(state=DISABLED)
            else:
                self.text_area.config(state=NORMAL)
                self.text_area.delete('1.0', END)
                if current_state == DISABLED:
                    self.text_area.config(state=DISABLED)
                messagebox.showerror("Ошибка", f"Не удалось получить статью '{word}'. Проверьте подключение к интернету.")
                
        except Exception as e:
            self.text_area.config(state=NORMAL)
            self.text_area.delete('1.0', END)
            if current_state == DISABLED:
                self.text_area.config(state=DISABLED)
            error_msg = str(e)
            if "Expecting value" in error_msg or "char 0" in error_msg:
                messagebox.showerror("Ошибка подключения", 
                                    "Проблема с подключением к Wikipedia.\n\n"
                                    "Возможные решения:\n"
                                    "1. Проверьте подключение к интернету\n"
                                    "2. Попробуйте использовать VPN\n"
                                    "3. Повторите попытку через несколько секунд\n"
                                    "4. Проверьте, открывается ли Wikipedia в браузере")
            else:
                messagebox.showerror("Ошибка", f"Произошла ошибка:\n{error_msg}")

    def get_wikipedia_page(self, title):
        """Альтернативный метод получения страницы Wikipedia через REST API"""
        try:
            # Используем прямой API запрос
            session = requests.Session()
            
            # URL для API Wikipedia
            url = "https://ru.wikipedia.org/api/rest_v1/page/summary/" + title.replace(" ", "_")
            
            # Добавляем заголовки для имитации браузера
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8'
            }
            
            response = session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data:
                    return data['extract']
                elif 'description' in data:
                    return data['description']
                else:
                    # Если не получили через REST API, пробуем через библиотеку wikipedia
                    return self.get_via_wikipedia_lib(title)
            elif response.status_code == 404:
                # Страница не найдена, ищем похожие
                return self.search_similar_pages(title)
            else:
                return self.get_via_wikipedia_lib(title)
                
        except requests.exceptions.RequestException as e:
            # Если прямая ошибка, пробуем через библиотеку
            return self.get_via_wikipedia_lib(title)
        except json.JSONDecodeError:
            return self.get_via_wikipedia_lib(title)

    def get_via_wikipedia_lib(self, title):
        """Получение через библиотеку wikipedia с обработкой ошибок"""
        try:
            # Пробуем получить страницу
            result = wikipedia.summary(title)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            # Несколько вариантов
            options = e.options[:15]
            selected = self.show_selection_dialog(options)
            if selected:
                return wikipedia.summary(selected)
            return None
        except wikipedia.exceptions.PageError:
            # Страница не найдена - ищем похожие
            return self.search_similar_pages(title)
        except Exception as e:
            raise e

    def search_similar_pages(self, query):
        """Поиск похожих страниц"""
        try:
            suggestions = wikipedia.search(query, results=10)
            if suggestions:
                selected = self.show_selection_dialog(suggestions, "Статья не найдена. Возможно, вы имели в виду:")
                if selected:
                    return wikipedia.summary(selected)
            return None
        except:
            return None

    def show_selection_dialog(self, options, title="Выберите статью"):
        """Показывает диалог выбора статьи из списка"""
        if not options:
            return None
            
        # Создаем диалоговое окно для выбора
        dialog = Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Центрируем окно
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        Label(dialog, text="Найдено несколько вариантов. Выберите один:", 
              font=("times new roman", 12), pady=10).pack()
        
        # Список для выбора
        frame = Frame(dialog)
        frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        listbox = Listbox(frame, font=("times new roman", 11), 
                          yscrollcommand=scrollbar.set)
        listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for option in options:
            listbox.insert(END, option)
        
        result = [None]
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                result[0] = listbox.get(selection[0])
                dialog.destroy()
        
        def on_double_click(event):
            on_select()
        
        listbox.bind('<Double-Button-1>', on_double_click)
        
        Button(dialog, text="Выбрать", command=on_select, 
               font=("times new roman", 11), padx=20, pady=5).pack(pady=10)
        
        Button(dialog, text="Отмена", command=dialog.destroy, 
               font=("times new roman", 11), padx=20, pady=5).pack()
        
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.bind('<Return>', lambda e: on_select())
        
        # Ждем закрытия окна
        self.root.wait_window(dialog)
        
        return result[0]

# Создаем главное окно Tkinter
if __name__ == "__main__":
    root = Tk()
    app = SearchWiki(root)
    root.mainloop()
