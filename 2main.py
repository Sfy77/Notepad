import tkinter as tk
from tkinter import ttk, messagebox

class AntivirusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Антивірус")
        self.root.geometry("1200x800")

        # Задаємо темно-синій фон і світлий текст
        self.bg_color = "#102040"
        self.fg_color = "#e0e6f0"
        self.root.configure(bg=self.bg_color)

        # Верхня панель з кнопками у правому верхньому кутку
        top_frame = tk.Frame(root, bg=self.bg_color)
        top_frame.pack(fill=tk.X, side=tk.TOP)

        # Spacer для вирівнювання кнопок вправо
        spacer = tk.Label(top_frame, bg=self.bg_color)
        spacer.pack(side=tk.LEFT, expand=True)

        login_btn = tk.Button(
            top_frame, text="Увійти", font=("Arial", 13, "bold"),
            bg="#304080", fg=self.fg_color, activebackground="#4050a0", activeforeground=self.fg_color,
            width=12, height=1, command=self.login
        )
        login_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        register_btn = tk.Button(
            top_frame, text="Зареєструватися", font=("Arial", 13, "bold"),
            bg="#304080", fg=self.fg_color, activebackground="#4050a0", activeforeground=self.fg_color,
            width=15, height=1, command=self.register
        )
        register_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        exit_btn = tk.Button(
            top_frame, text="Вийти", font=("Arial", 13, "bold"),
            bg="#800000", fg="#fff", activebackground="#a00000", activeforeground="#fff",
            width=10, height=1, command=root.quit
        )
        exit_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        # Верхній напис
        title = tk.Label(root, text="Антивірус", font=("Arial", 32, "bold"),
                         bg=self.bg_color, fg=self.fg_color)
        title.pack(pady=20)

        # Кнопки для сканування та сервісу
        btn_frame = tk.Frame(root, bg=self.bg_color)
        btn_frame.pack(pady=30)

        btn_font = ("Arial", 16, "bold")
        btn_width = 18
        btn_height = 2

        self.quick_btn = tk.Button(
            btn_frame, text="Швидке сканування", width=btn_width, height=btn_height, font=btn_font,
            command=self.quick_scan, bg="#203060", fg=self.fg_color,
            activebackground="#304080", activeforeground=self.fg_color
        )
        self.quick_btn.grid(row=0, column=0, padx=20, pady=15)

        self.full_btn = tk.Button(
            btn_frame, text="Повне сканування", width=btn_width, height=btn_height, font=btn_font,
            command=self.full_scan, bg="#203060", fg=self.fg_color,
            activebackground="#304080", activeforeground=self.fg_color
        )
        self.full_btn.grid(row=0, column=1, padx=20, pady=15)

        self.custom_btn = tk.Button(
            btn_frame, text="Вибіркова перевірка", width=btn_width, height=btn_height, font=btn_font,
            command=self.custom_scan, bg="#203060", fg=self.fg_color,
            activebackground="#304080", activeforeground=self.fg_color
        )
        self.custom_btn.grid(row=1, column=0, padx=20, pady=15)

        self.update_btn = tk.Button(
            btn_frame, text="Оновити базу", width=btn_width, height=btn_height, font=btn_font,
            command=self.update_db, bg="#203060", fg=self.fg_color,
            activebackground="#304080", activeforeground=self.fg_color
        )
        self.update_btn.grid(row=1, column=1, padx=20, pady=15)

        # Додаємо кнопки "Очистити" та "Збільшити швидкість" у той самий фрейм
        self.clear_btn = tk.Button(
            btn_frame, text="Очистити", width=btn_width, height=btn_height, font=btn_font,
            command=self.clear_system, bg="#203060", fg=self.fg_color,
            activebackground="#304080", activeforeground=self.fg_color
        )
        self.clear_btn.grid(row=2, column=0, padx=20, pady=15)

        self.boost_btn = tk.Button(
            btn_frame, text="Збільшити швидкість", width=btn_width, height=btn_height, font=btn_font,
            command=self.boost_speed, bg="#203060", fg=self.fg_color,
            activebackground="#304080", activeforeground=self.fg_color
        )
        self.boost_btn.grid(row=2, column=1, padx=20, pady=15)

        # Прогресбар
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "TProgressbar",
            troughcolor="#203060",
            background="#4a90e2",
            bordercolor="#102040",
            lightcolor="#4a90e2",
            darkcolor="#203060"
        )
        self.progress = ttk.Progressbar(root, orient="horizontal", length=800, mode="determinate", maximum=100, style="TProgressbar")
        self.progress.pack(pady=20)

        # Відсотки прогресу
        self.progress_label = tk.Label(root, text="0%", bg=self.bg_color, fg=self.fg_color, font=("Arial", 18, "bold"))
        self.progress_label.pack()

        # Відсоток безпеки комп'ютера
        self.security_label = tk.Label(
            root, text="Безпека комп'ютера: 100%", font=("Arial", 20, "bold"),
            fg="green", bg=self.bg_color
        )
        self.security_label.pack(pady=15)
        self.security_percent = 100  # Початково 100%

        # Лог/статус
        self.status = tk.Label(
            root, text="Готово до роботи", anchor="w", font=("Arial", 16),
            bg=self.bg_color, fg=self.fg_color
        )
        self.status.pack(fill=tk.X, padx=20, pady=10)

        # Додаємо кнопку "Магазин"
        menu_btn = tk.Button(
            root, text="Магазин", font=("Arial", 16, "bold"),
            bg="#304080", fg=self.fg_color, activebackground="#4050a0", activeforeground=self.fg_color,
            command=self.open_store, width=15, height=2
        )
        menu_btn.pack(pady=10)

    def quick_scan(self):
        self.status.config(text="Виконується швидке сканування...")
        self.simulate_progress(duration=2000, step=10, after_func=lambda: self.scan_done("Швидке сканування завершено!", found_viruses=0))

    def full_scan(self):
        self.status.config(text="Виконується повне сканування...")
        self.simulate_progress(duration=4000, step=5, after_func=lambda: self.scan_done("Повне сканування завершено!", found_viruses=1))

    def custom_scan(self):
        self.status.config(text="Виконується вибіркова перевірка...")
        self.simulate_progress(duration=1500, step=15, after_func=lambda: self.scan_done("Вибіркова перевірка завершена!", found_viruses=0))

    def update_db(self):
        self.status.config(text="Оновлення бази...")
        self.simulate_progress(duration=1200, step=20, after_func=lambda: self.scan_done("Базу оновлено!", update_only=True))

    def simulate_progress(self, duration, step, after_func):
        self.progress["value"] = 0
        self.progress_label.config(text="0%")
        self._progress_value = 0
        self._progress_step = step
        self._progress_max = 100
        self._progress_interval = duration // (100 // step)
        self._progress_after_func = after_func
        self._progress_update()

    def _progress_update(self):
        if self._progress_value < self._progress_max:
            self._progress_value += self._progress_step
            if self._progress_value > 100:
                self._progress_value = 100
            self.progress["value"] = self._progress_value
            self.progress_label.config(text=f"{self._progress_value}%")
            self.root.after(self._progress_interval, self._progress_update)
        else:
            self.progress["value"] = 100
            self.progress_label.config(text="100%")
            if self._progress_after_func:
                self._progress_after_func()

    def scan_done(self, msg, found_viruses=0, update_only=False):
        self.progress.stop()
        self.progress["value"] = 100
        self.progress_label.config(text="100%")
        self.status.config(text=msg)
        if not update_only:
            # Зменшуємо відсоток безпеки, якщо знайдено віруси
            if found_viruses > 0:
                self.security_percent = max(0, self.security_percent - found_viruses * 10)
                color = "green" if self.security_percent >= 80 else "orange" if self.security_percent >= 50 else "red"
                self.security_label.config(text=f"Безпека комп'ютера: {self.security_percent}%", fg=color)
                # Діалог для видалення вірусу
                answer = messagebox.askyesno("Загроза виявлена", "Виявлено вірус!\nБажаєте видалити вірус?")
                if answer:
                    self.remove_virus()
            else:
                # Якщо вірусів не знайдено, підвищуємо безпеку (але не більше 100)
                self.security_percent = min(100, self.security_percent + 2)
                color = "green" if self.security_percent >= 80 else "orange" if self.security_percent >= 50 else "red"
                self.security_label.config(text=f"Безпека комп'ютера: {self.security_percent}%", fg=color)
        messagebox.showinfo("Антивірус", msg)

    def remove_virus(self):
        # Тут може бути логіка видалення вірусу, зараз просто повідомлення
        self.status.config(text="Вірус видалено. Система безпечна.")
        self.security_percent = min(100, self.security_percent + 10)
        color = "green" if self.security_percent >= 80 else "orange" if self.security_percent >= 50 else "red"
        self.security_label.config(text=f"Безпека комп'ютера: {self.security_percent}%", fg=color)
        messagebox.showinfo("Антивірус", "Вірус успішно видалено!")

    def open_store(self):
        store_win = tk.Toplevel(self.root)
        store_win.title("Магазин Антивірусів")
        store_win.geometry("900x600")
        store_win.configure(bg=self.bg_color)

        # Додаємо Canvas для скролу
        canvas = tk.Canvas(store_win, bg=self.bg_color, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(store_win, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Фрейм для контенту магазину
        content_frame = tk.Frame(canvas, bg=self.bg_color)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        content_frame.bind("<Configure>", on_configure)

        # Прокрутка колесиком миші
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows

        tk.Label(content_frame, text="Магазин Антивірусів", font=("Arial", 28, "bold"),
                 bg=self.bg_color, fg=self.fg_color).pack(pady=20)

        versions = [
            ("Антивірус Free", "Безкоштовна версія з базовим захистом.", "0 грн",
             "Антивірус Free — це базовий рівень захисту для вашого комп'ютера. Захист від основних загроз, ручне оновлення бази, мінімальний вплив на продуктивність."),
            ("Антивірус Pro", "Розширений захист, автоматичне оновлення, підтримка.", "299 грн/рік",
             "Антивірус Pro — оптимальний вибір для активних користувачів. Включає розширений захист, автоматичне оновлення, технічну підтримку 24/7, захист електронної пошти."),
            ("Антивірус Ultimate", "Максимальний захист, VPN, преміум-підтримка, сімейна ліцензія.", "499 грн/рік",
             "Антивірус Ultimate — максимальний рівень безпеки. Включає всі функції Pro, VPN, захист онлайн-платежів, преміум-підтримку, сімейну ліцензію на 5 пристроїв."),
            ("Антивірус Mobile", "Захист для Android/iOS пристроїв.", "149 грн/рік",
             "Антивірус Mobile — захистіть свій смартфон або планшет. Виявлення мобільних загроз, захист особистих даних, блокування небезпечних додатків."),
            ("Антивірус Business", "Захист для офісу, адміністрування, корпоративна підтримка.", "1999 грн/рік",
             "Антивірус Business — рішення для бізнесу. Централізоване управління, корпоративна підтримка, захист серверів і робочих станцій, аудит безпеки."),
            ("Антивірус Student", "Доступна ціна для студентів, базовий+ захист.", "99 грн/рік",
             "Антивірус Student — спеціальна пропозиція для студентів. Базовий захист, антиреклама, захист браузера, легка вага для старих ПК."),
        ]

        for name, desc, price, details in versions:
            frame = tk.Frame(content_frame, bg="#203060", bd=2, relief="groove")
            frame.pack(fill=tk.X, padx=40, pady=10)
            tk.Label(frame, text=name, font=("Arial", 18, "bold"), bg="#203060", fg="#e0e6f0").pack(anchor="w", padx=10, pady=2)
            tk.Label(frame, text=desc, font=("Arial", 13), bg="#203060", fg="#e0e6f0").pack(anchor="w", padx=10)
            tk.Label(frame, text=price, font=("Arial", 14, "bold"), bg="#203060", fg="#ffd700").pack(anchor="e", padx=10, pady=2)
            tk.Button(
                frame, text="Детальніше / Купити", font=("Arial", 12, "bold"),
                bg="#304080", fg="#e0e6f0", activebackground="#4050a0", activeforeground="#e0e6f0",
                command=lambda n=name, d=desc, p=price, det=details: self.show_product_page(n, d, p, det)
            ).pack(anchor="e", padx=10, pady=5)

    def show_product_page(self, name, desc, price, details):
        prod_win = tk.Toplevel(self.root)
        prod_win.title(name)
        prod_win.geometry("600x400")
        prod_win.configure(bg=self.bg_color)

        tk.Label(prod_win, text=name, font=("Arial", 22, "bold"), bg=self.bg_color, fg="#ffd700").pack(pady=15)
        tk.Label(prod_win, text=desc, font=("Arial", 14, "italic"), bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        tk.Label(prod_win, text=price, font=("Arial", 16, "bold"), bg=self.bg_color, fg="#ffd700").pack(pady=5)
        tk.Label(prod_win, text="Опис:", font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=30, pady=(15, 0))
        tk.Message(prod_win, text=details, font=("Arial", 13), bg=self.bg_color, fg=self.fg_color, width=540).pack(padx=30, pady=5)
        def buy_and_close():
            messagebox.showinfo("Покупка", f"Дякуємо за вибір {name}!\nЗ вами зв'яжеться менеджер.")
            prod_win.destroy()  # Закриває лише вікно покупки, магазин залишається відкритим
        tk.Button(
            prod_win, text="Купити", font=("Arial", 14, "bold"),
            bg="#304080", fg="#e0e6f0", activebackground="#4050a0", activeforeground="#e0e6f0",
            command=buy_and_close
        ).pack(pady=20)

    def login(self):
        login_win = tk.Toplevel(self.root)
        login_win.title("Вхід")
        login_win.geometry("400x270")  # Збільшено розмір вікна
        login_win.configure(bg=self.bg_color)

        tk.Label(login_win, text="Вхід", font=("Arial", 18, "bold"), bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        tk.Label(login_win, text="Логін:", font=("Arial", 13), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=30, pady=(10, 0))
        login_entry = tk.Entry(login_win, font=("Arial", 13))
        login_entry.pack(padx=30, fill=tk.X)

        tk.Label(login_win, text="Пароль:", font=("Arial", 13), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=30, pady=(10, 0))
        password_entry = tk.Entry(login_win, font=("Arial", 13), show="*")
        password_entry.pack(padx=30, fill=tk.X)

        def do_login():
            login = login_entry.get()
            password = password_entry.get()
            if login and password:
                messagebox.showinfo("Вхід", f"Вітаємо, {login}! Вхід виконано.")
                login_win.destroy()
            else:
                messagebox.showwarning("Помилка", "Введіть логін і пароль!")

        tk.Button(
            login_win, text="Увійти", font=("Arial", 15, "bold"),
            bg="#304080", fg=self.fg_color, activebackground="#4050a0", activeforeground=self.fg_color,
            command=do_login, width=15, height=2
        ).pack(pady=20)

    def register(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Реєстрація")
        reg_win.geometry("370x320")
        reg_win.configure(bg=self.bg_color)

        tk.Label(reg_win, text="Реєстрація", font=("Arial", 18, "bold"), bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        tk.Label(reg_win, text="Логін:", font=("Arial", 13), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=30, pady=(10, 0))
        login_entry = tk.Entry(reg_win, font=("Arial", 13))
        login_entry.pack(padx=30, fill=tk.X)

        tk.Label(reg_win, text="Пароль:", font=("Arial", 13), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=30, pady=(10, 0))
        password_entry = tk.Entry(reg_win, font=("Arial", 13), show="*")
        password_entry.pack(padx=30, fill=tk.X)

        tk.Label(reg_win, text="Підтвердіть пароль:", font=("Arial", 13), bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=30, pady=(10, 0))
        confirm_entry = tk.Entry(reg_win, font=("Arial", 13), show="*")
        confirm_entry.pack(padx=30, fill=tk.X)

        def do_register():
            login = login_entry.get()
            password = password_entry.get()
            confirm = confirm_entry.get()
            if not login or not password or not confirm:
                messagebox.showwarning("Помилка", "Заповніть всі поля!")
            elif password != confirm:
                messagebox.showwarning("Помилка", "Паролі не співпадають!")
            else:
                messagebox.showinfo("Реєстрація", f"Користувач {login} зареєстрований!")
                reg_win.destroy()

        tk.Button(reg_win, text="Зареєструватися", font=("Arial", 13, "bold"),
                  bg="#304080", fg=self.fg_color, activebackground="#4050a0", activeforeground=self.fg_color,
                  command=do_register).pack(pady=20)

    def clear_system(self):
        # Імітація очищення системи
        self.status.config(text="Виконується очищення системи...")
        self.progress["value"] = 0
        self.progress_label.config(text="0%")
        self.root.after(1500, self._clear_done)

    def _clear_done(self):
        self.progress["value"] = 100
        self.progress_label.config(text="100%")
        self.status.config(text="Систему очищено від сміття!")
        messagebox.showinfo("Очищення", "Систему очищено від сміття та тимчасових файлів.")

    def boost_speed(self):
        # Імітація прискорення роботи
        self.status.config(text="Оптимізація швидкості роботи...")
        self.progress["value"] = 0
        self.progress_label.config(text="0%")
        self.root.after(1200, self._boost_done)

    def _boost_done(self):
        self.progress["value"] = 100
        self.progress_label.config(text="100%")
        self.status.config(text="Швидкість роботи комп'ютера збільшено!")
        messagebox.showinfo("Оптимізація", "Швидкість роботи комп'ютера збільшено!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AntivirusApp(root)
    root.mainloop()