import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
import tkinter.colorchooser as colorchooser

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Блокнот")
        self.root.geometry("700x500")

        self.current_font_size_en = 12
        self.current_font_size_cyr = 12

        self.text_area = tk.Text(self.root, undo=True, font=("Arial", self.current_font_size_en))
        self.text_area.pack(fill=tk.BOTH, expand=1)

        # Контекстне меню для текстового поля
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Вирізати", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Копіювати", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Вставити", command=lambda: self.text_area.event_generate("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Змінити колір", command=self.context_change_color)
        self.context_menu.add_command(label="Змінити стиль шрифту", command=self.context_change_font_style)
        self.context_menu.add_command(label="Змінити розмір шрифту", command=self.context_change_font_size)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Виділити все", command=lambda: self.text_area.event_generate("<<SelectAll>>"))
        self.context_menu.add_command(label="Очистити", command=self.clear_text)

        self.text_area.bind("<Button-3>", self.show_context_menu)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Меню "Файл"
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Відкрити", command=self.open_file)
        file_menu.add_command(label="Зберегти", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)

        # Меню "Редагувати"
        edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Редагувати", menu=edit_menu)
        edit_menu.add_command(label="Відмінити", command=self.undo)
        edit_menu.add_command(label="Повторити", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Вирізати", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Копіювати", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Вставити", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Вирівняти ліворуч", command=self.align_left)
        edit_menu.add_command(label="По центру", command=self.align_center)
        edit_menu.add_command(label="Вирівняти праворуч", command=self.align_right)
        edit_menu.add_separator()
        edit_menu.add_command(label="Очистити", command=self.clear_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Змінити розмір шрифту (EN)", command=self.change_font_size_en)
        edit_menu.add_command(label="Змінити розмір шрифту (Кирилиця)", command=self.change_font_size_cyr)
        edit_menu.add_command(label="Змінити стиль шрифту (EN)", command=self.change_font_style_en)
        edit_menu.add_command(label="Змінити стиль шрифту (Кирилиця)", command=self.change_font_style_cyr)
        edit_menu.add_command(label="Змінити колір тексту (EN)", command=self.change_color_en)
        edit_menu.add_command(label="Змінити колір тексту (Кирилиця)", command=self.change_color_cyr)

        # Теги для вирівнювання
        self.text_area.tag_configure("left", justify="left")
        self.text_area.tag_configure("center", justify="center")
        self.text_area.tag_configure("right", justify="right")

        # Теги для шрифтів
        self.font_en = font.Font(family="Arial", size=self.current_font_size_en)
        self.font_cyr = font.Font(family="Arial", size=self.current_font_size_cyr)
        self.text_area.tag_configure("en_font", font=self.font_en)
        self.text_area.tag_configure("cyr_font", font=self.font_cyr)

        # Додаємо кольори для англійських і кириличних символів
        self.color_en = "#000000"
        self.color_cyr = "#000000"
        self.text_area.tag_configure("en_font", font=self.font_en, foreground=self.color_en)
        self.text_area.tag_configure("cyr_font", font=self.font_cyr, foreground=self.color_cyr)

        # Гарячі клавіші
        self.text_area.bind("<Control-z>", lambda event: (self.undo(), "break"))
        self.text_area.bind("<Control-y>", lambda event: (self.redo(), "break"))
        self.text_area.bind("<Control-x>", lambda event: (self.text_area.event_generate("<<Cut>>"), "break"))
        self.text_area.bind("<Control-c>", lambda event: (self.text_area.event_generate("<<Copy>>"), "break"))
        self.text_area.bind("<Control-v>", lambda event: (self.text_area.event_generate("<<Paste>>"), "break"))

        # Оновлення шрифтів при кожній зміні тексту
        self.text_area.bind("<<Modified>>", self.apply_fonts)

        # Панель для вибору шрифту та розміру як у Word
        font_frame = tk.Frame(self.root)
        font_frame.pack(fill=tk.X, padx=5, pady=2)

        # Список шрифтів
        available_fonts = sorted(list(font.families()))
        self.font_family_var_en = tk.StringVar(value=self.font_en.actual("family"))
        self.font_family_var_cyr = tk.StringVar(value=self.font_cyr.actual("family"))
        self.font_size_var_en = tk.IntVar(value=self.current_font_size_en)
        self.font_size_var_cyr = tk.IntVar(value=self.current_font_size_cyr)

        tk.Label(font_frame, text="EN:").pack(side=tk.LEFT)
        font_menu_en = tk.OptionMenu(font_frame, self.font_family_var_en, *available_fonts, command=self.set_font_family_en)
        font_menu_en.pack(side=tk.LEFT)
        size_menu_en = tk.Spinbox(font_frame, from_=8, to=72, textvariable=self.font_size_var_en, width=4, command=self.set_font_size_en)
        size_menu_en.pack(side=tk.LEFT, padx=(0, 10))

        color_btn_en = tk.Button(font_frame, text="Колір EN", command=self.change_color_en)
        color_btn_en.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(font_frame, text="Кирилиця:").pack(side=tk.LEFT)
        font_menu_cyr = tk.OptionMenu(font_frame, self.font_family_var_cyr, *available_fonts, command=self.set_font_family_cyr)
        font_menu_cyr.pack(side=tk.LEFT)
        size_menu_cyr = tk.Spinbox(font_frame, from_=8, to=72, textvariable=self.font_size_var_cyr, width=4, command=self.set_font_size_cyr)
        size_menu_cyr.pack(side=tk.LEFT)

        color_btn_cyr = tk.Button(font_frame, text="Колір Кирилиця", command=self.change_color_cyr)
        color_btn_cyr.pack(side=tk.LEFT)

        # Панель для вирівнювання тексту
        align_frame = tk.Frame(self.root)
        align_frame.pack(fill=tk.X, padx=5, pady=2)

        align_left_btn = tk.Button(align_frame, text="Вирівняти ліворуч", command=self.align_left)
        align_left_btn.pack(side=tk.LEFT, padx=2)
        align_center_btn = tk.Button(align_frame, text="По центру", command=self.align_center)
        align_center_btn.pack(side=tk.LEFT, padx=2)
        align_right_btn = tk.Button(align_frame, text="Вирівняти праворуч", command=self.align_right)
        align_right_btn.pack(side=tk.LEFT, padx=2)

        # Теги для вирівнювання
        self.text_area.tag_configure("left", justify="left")
        self.text_area.tag_configure("center", justify="center")
        self.text_area.tag_configure("right", justify="right")

        # Теги для шрифтів
        self.font_en = font.Font(family="Arial", size=self.current_font_size_en)
        self.font_cyr = font.Font(family="Arial", size=self.current_font_size_cyr)
        self.text_area.tag_configure("en_font", font=self.font_en)
        self.text_area.tag_configure("cyr_font", font=self.font_cyr)

        # Гарячі клавіші
        self.text_area.bind("<Control-z>", lambda event: (self.undo(), "break"))
        self.text_area.bind("<Control-y>", lambda event: (self.redo(), "break"))
        self.text_area.bind("<Control-x>", lambda event: (self.text_area.event_generate("<<Cut>>"), "break"))
        self.text_area.bind("<Control-c>", lambda event: (self.text_area.event_generate("<<Copy>>"), "break"))
        self.text_area.bind("<Control-v>", lambda event: (self.text_area.event_generate("<<Paste>>"), "break"))

        # Оновлення шрифтів при кожній зміні тексту
        self.text_area.bind("<<Modified>>", self.apply_fonts)

    def apply_fonts(self, event=None):
        # Застосовує різні розміри шрифту для англійських і кириличних символів
        self.text_area.tag_remove("en_font", "1.0", tk.END)
        self.text_area.tag_remove("cyr_font", "1.0", tk.END)
        text = self.text_area.get("1.0", tk.END)
        idx = "1.0"
        for char in text:
            next_idx = self.text_area.index(f"{idx} +1c")
            if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
                self.text_area.tag_add("en_font", idx, next_idx)
            elif '\u0400' <= char <= '\u04FF' or '\u0500' <= char <= '\u052F':  # Кирилиця
                self.text_area.tag_add("cyr_font", idx, next_idx)
            idx = next_idx
            if char == '\n':
                continue
        self.text_area.edit_modified(False)

    def change_font_size_en(self):
        size = simpledialog.askinteger("Розмір шрифту (EN)", "Введіть розмір шрифту для англійських букв:", initialvalue=self.current_font_size_en)
        if size:
            self.current_font_size_en = size
            self.font_en.configure(size=size)
            self.apply_fonts()

    def change_font_size_cyr(self):
        size = simpledialog.askinteger("Розмір шрифту (Кирилиця)", "Введіть розмір шрифту для кирилиці:", initialvalue=self.current_font_size_cyr)
        if size:
            self.current_font_size_cyr = size
            self.font_cyr.configure(size=size)
            self.apply_fonts()

    def change_font_style_en(self):
        styles = ["Arial", "Times New Roman", "Courier New", "Calibri", "Comic Sans MS"]

        # Створюємо нове вікно для вибору стилю з прикладами
        style_win = tk.Toplevel(self.root)
        style_win.title("Стиль шрифту (EN)")
        style_win.resizable(False, False)

        tk.Label(style_win, text="Оберіть стиль шрифту для англійських букв:").pack(padx=10, pady=5)

        selected = tk.StringVar(value=self.font_en.actual("family"))

        def set_style():
            self.font_en.configure(family=selected.get())
            self.apply_fonts()
            style_win.destroy()

        for s in styles:
            example = tk.Radiobutton(
                style_win,
                text=f"{s} (Example: ABC abc)",
                variable=selected,
                value=s,
                font=(s, 12)
            )
            example.pack(anchor="w", padx=15)

        tk.Button(style_win, text="OK", command=set_style).pack(pady=10)

    def change_font_style_cyr(self):
        styles = ["Arial", "Times New Roman", "Courier New", "Calibri", "Comic Sans MS"]

        style_win = tk.Toplevel(self.root)
        style_win.title("Стиль шрифту (Кирилиця)")
        style_win.resizable(False, False)

        tk.Label(style_win, text="Оберіть стиль шрифту для кирилиці:").pack(padx=10, pady=5)

        selected = tk.StringVar(value=self.font_cyr.actual("family"))

        def set_style():
            self.font_cyr.configure(family=selected.get())
            self.apply_fonts()
            style_win.destroy()

        for s in styles:
            example = tk.Radiobutton(
                style_win,
                text=f"{s} (Приклад: АБВ абв)",
                variable=selected,
                value=s,
                font=(s, 12)
            )
            example.pack(anchor="w", padx=15)

        tk.Button(style_win, text="OK", command=set_style).pack(pady=10)

    def set_font_family_en(self, family):
        self.font_en.configure(family=family)
        self.apply_fonts()

    def set_font_family_cyr(self, family):
        self.font_cyr.configure(family=family)
        self.apply_fonts()

    def set_font_size_en(self):
        size = self.font_size_var_en.get()
        self.current_font_size_en = int(size)
        self.font_en.configure(size=int(size))
        self.apply_fonts()

    def set_font_size_cyr(self):
        size = self.font_size_var_cyr.get()
        self.current_font_size_cyr = int(size)
        self.font_cyr.configure(size=int(size))
        self.apply_fonts()

    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass

    def align_left(self):
        self.text_area.tag_remove("center", "1.0", tk.END)
        self.text_area.tag_remove("right", "1.0", tk.END)
        self.text_area.tag_add("left", "1.0", tk.END)

    def align_center(self):
        self.text_area.tag_remove("left", "1.0", tk.END)
        self.text_area.tag_remove("right", "1.0", tk.END)
        self.text_area.tag_add("center", "1.0", tk.END)

    def align_right(self):
        self.text_area.tag_remove("left", "1.0", tk.END)
        self.text_area.tag_remove("center", "1.0", tk.END)
        self.text_area.tag_add("right", "1.0", tk.END)

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.apply_fonts()
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

    def change_color_en(self):
        colors = [
            ("Чорний", "#000000"), ("Червоний", "#FF0000"), ("Зелений", "#008000"),
            ("Синій", "#0000FF"), ("Жовтий", "#FFFF00"), ("Оранжевий", "#FFA500"),
            ("Фіолетовий", "#800080"), ("Бірюзовий", "#00CED1"), ("Сірий", "#808080"),
            ("Білий", "#FFFFFF"), ("Вибрати...", None)
        ]

        color_win = tk.Toplevel(self.root)
        color_win.title("Колір тексту (EN)")
        color_win.resizable(False, False)
        tk.Label(color_win, text="Оберіть колір для англійських букв:").pack(padx=10, pady=5)

        selected = tk.StringVar(value=self.color_en)

        def set_color():
            val = selected.get()
            if val == "Вибрати...":
                color = colorchooser.askcolor(title="Виберіть колір", initialcolor=self.color_en)[1]
            else:
                color = val

            try:
                start = self.text_area.index(tk.SEL_FIRST)
                end = self.text_area.index(tk.SEL_LAST)
                tag_name = f"en_color_{color}"
                if not tag_name in self.text_area.tag_names():
                    self.text_area.tag_configure(tag_name, foreground=color)
                self.text_area.tag_add(tag_name, start, end)
            except tk.TclError:
                # Якщо немає виділення — змінюємо глобальний колір
                self.color_en = color
                self.text_area.tag_configure("en_font", foreground=self.color_en)
                self.apply_fonts()
            color_win.destroy()

        for name, hexcode in colors:
            if hexcode:
                example = tk.Radiobutton(
                    color_win,
                    text=name,
                    variable=selected,
                    value=hexcode,
                    indicatoron=0,
                    width=15,
                    background=hexcode,
                    fg="black" if hexcode not in ["#000000", "#800080"] else "white",
                    font=("Arial", 11)
                )
            else:
                example = tk.Radiobutton(
                    color_win,
                    text=name,
                    variable=selected,
                    value="Вибрати...",
                    indicatoron=0,
                    width=15,
                    font=("Arial", 11)
                )
            example.pack(anchor="w", padx=15, pady=2)

        tk.Button(color_win, text="OK", command=set_color).pack(pady=10)

    def change_color_cyr(self):
        colors = [
            ("Чорний", "#000000"), ("Червоний", "#FF0000"), ("Зелений", "#008000"),
            ("Синій", "#0000FF"), ("Жовтий", "#FFFF00"), ("Оранжевий", "#FFA500"),
            ("Фіолетовий", "#800080"), ("Бірюзовий", "#00CED1"), ("Сірий", "#808080"),
            ("Білий", "#FFFFFF"), ("Вибрати...", None)
        ]

        color_win = tk.Toplevel(self.root)
        color_win.title("Колір тексту (Кирилиця)")
        color_win.resizable(False, False)
        tk.Label(color_win, text="Оберіть колір для кирилиці:").pack(padx=10, pady=5)

        selected = tk.StringVar(value=self.color_cyr)

        def set_color():
            val = selected.get()
            if val == "Вибрати...":
                color = colorchooser.askcolor(title="Виберіть колір", initialcolor=self.color_cyr)[1]
            else:
                color = val

            try:
                start = self.text_area.index(tk.SEL_FIRST)
                end = self.text_area.index(tk.SEL_LAST)
                tag_name = f"cyr_color_{color}"
                if not tag_name in self.text_area.tag_names():
                    self.text_area.tag_configure(tag_name, foreground=color)
                self.text_area.tag_add(tag_name, start, end)
            except tk.TclError:
                # Якщо немає виділення — змінюємо глобальний колір
                self.color_cyr = color
                self.text_area.tag_configure("cyr_font", foreground=self.color_cyr)
                self.apply_fonts()
            color_win.destroy()

        for name, hexcode in colors:
            if hexcode:
                example = tk.Radiobutton(
                    color_win,
                    text=name,
                    variable=selected,
                    value=hexcode,
                    indicatoron=0,
                    width=15,
                    background=hexcode,
                    fg="black" if hexcode not in ["#000000", "#800080"] else "white",
                    font=("Arial", 11)
                )
            else:
                example = tk.Radiobutton(
                    color_win,
                    text=name,
                    variable=selected,
                    value="Вибрати...",
                    indicatoron=0,
                    width=15,
                    font=("Arial", 11)
                )
            example.pack(anchor="w", padx=15, pady=2)

        tk.Button(color_win, text="OK", command=set_color).pack(pady=10)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def context_change_color(self):
        try:
            start = self.text_area.index(tk.SEL_FIRST)
            end = self.text_area.index(tk.SEL_LAST)
        except tk.TclError:
            return  # Нічого не виділено
        color = colorchooser.askcolor(title="Оберіть колір тексту")[1]
        if color:
            tag_name = f"context_color_{color}"
            if not tag_name in self.text_area.tag_names():
                self.text_area.tag_configure(tag_name, foreground=color)
            self.text_area.tag_add(tag_name, start, end)

    def context_change_font_style(self):
        try:
            start = self.text_area.index(tk.SEL_FIRST)
            end = self.text_area.index(tk.SEL_LAST)
        except tk.TclError:
            return  # Нічого не виділено
        styles = [
            "Arial", "Times New Roman", "Courier New", "Calibri", "Comic Sans MS",
            "Verdana", "Tahoma", "Georgia", "Impact", "Lucida Console",
            "Segoe UI", "Trebuchet MS", "Garamond", "Bookman Old Style", "Consolas"
        ]
        style_win = tk.Toplevel(self.root)
        style_win.title("Стиль шрифту для виділеного")
        style_win.resizable(False, False)
        tk.Label(style_win, text="Оберіть стиль шрифту:").pack(padx=10, pady=5)
        selected = tk.StringVar(value="Arial")
        def set_style():
            font_family = selected.get()
            tag_name = f"context_font_{font_family}"
            if not tag_name in self.text_area.tag_names():
                self.text_area.tag_configure(tag_name, font=(font_family, 12))
            self.text_area.tag_add(tag_name, start, end)
            style_win.destroy()
        for s in styles:
            example = tk.Radiobutton(
                style_win,
                text=f"{s} (Приклад: АБВ абв ABC abc)",
                variable=selected,
                value=s,
                font=(s, 12)
            )
            example.pack(anchor="w", padx=15)
        tk.Button(style_win, text="OK", command=set_style).pack(pady=10)

    def context_change_font_size(self):
        try:
            start = self.text_area.index(tk.SEL_FIRST)
            end = self.text_area.index(tk.SEL_LAST)
        except tk.TclError:
            return  # Нічого не виділено
        size = simpledialog.askinteger("Розмір шрифту", "Введіть розмір шрифту для виділеного тексту:", initialvalue=12)
        if size:
            tag_name = f"context_size_{size}"
            # Визначаємо поточний шрифт виділеного тексту (або беремо Arial)
            try:
                current_tags = self.text_area.tag_names(start)
                font_family = "Arial"
                for tag in current_tags:
                    font_conf = self.text_area.tag_cget(tag, "font")
                    if font_conf:
                        font_family = font_conf.split()[0]
                        break
            except Exception:
                font_family = "Arial"
            if not tag_name in self.text_area.tag_names():
                self.text_area.tag_configure(tag_name, font=(font_family, size))
            self.text_area.tag_add(tag_name, start, end)

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()