from tkinter import *
import wikipedia
from tkinter import messagebox

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
        title.place(x=0, y=0, relwidth=1)

        # Основной фрейм
        frame1 = Frame(self.root, bd=2, relief=RIDGE)
        frame1.place(x=20, y=130, width=1330, height=550)

        # Строка поиска
        self.var_search = StringVar()
        entry_word = Entry(self.root, textvariable=self.var_search, font=("times new roman", 20))
        entry_word.place(x=100, y=82, width=500)

        # Кнопки
        btn_search = Button(self.root, text="Искать", command=self.search_word, font=("times new roman", 15, "bold"), bg="#262626", fg="white")
        btn_search.place(x=620, y=80, height=40, width=120)

        btn_clear = Button(self.root, text="Очистить", command=self.clear, font=("times new roman", 15, "bold"), bg="#262626", fg="white")
        btn_clear.place(x=750, y=80, height=40, width=120)

        btn_enable = Button(self.root, text="Разрешить редактирование", command=self.enable_editing, font=("times new roman", 15, "bold"), bg="#262626", fg="white")
        btn_enable.place(x=880, y=80, height=40, width=220)

        btn_disable = Button(self.root, text="Запретить редактирование", command=self.disable_editing, font=("times new roman", 15, "bold"), bg="#262626", fg="white")
        btn_disable.place(x=1100, y=80, height=40, width=220)

        # Прокручиваемое поле для вывода
        scroll_y = Scrollbar(frame1, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill="y")

        self.text_area = Text(frame1, font=("times new roman", 15), yscrollcommand=scroll_y.set)
        self.text_area.pack(fill=BOTH, expand=1)
        scroll_y.config(command=self.text_area.yview)

    # Включить режим редактирования
    def enable_editing(self):
        self.text_area.config(state=NORMAL)

    # Отключить режим редактирования
    def disable_editing(self):
        self.text_area.config(state=DISABLED)

    # Очистить поле ввода и область вывода
    def clear(self):
        self.var_search.set("")     # Очистить строку поиска
        self.text_area.delete('1.0', END)  # Очистить область вывода

    # Выполнить поиск по запросу
    def search_word(self):
        word = self.var_search.get().strip()
        if not word:
            messagebox.showerror("Ошибка", "Введите слово для поиска.")
        else:
            try:
                result = wikipedia.summary(word)
                self.text_area.insert('1.0', result)
            except wikipedia.exceptions.PageError:
                messagebox.showerror("Ошибка", f"В статье '{word}' отказано!")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

# Создаем главное окно Tkinter
root = Tk()
app = SearchWiki(root)  # Передаем экземпляр корня в класс
root.mainloop()