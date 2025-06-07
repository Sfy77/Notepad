import tkinter as tk
from tkinter import ttk, messagebox

class AntivirusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Антивірус")
        self.root.geometry("500x370")

        # Верхній напис
        title = tk.Label(root, text="Антивірус", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Кнопки для сканування
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.quick_btn = tk.Button(btn_frame, text="Швидке сканування", width=20, command=self.quick_scan)
        self.quick_btn.grid(row=0, column=0, padx=5, pady=5)

        self.full_btn = tk.Button(btn_frame, text="Повне сканування", width=20, command=self.full_scan)
        self.full_btn.grid(row=0, column=1, padx=5, pady=5)

        self.custom_btn = tk.Button(btn_frame, text="Вибіркова перевірка", width=20, command=self.custom_scan)
        self.custom_btn.grid(row=1, column=0, padx=5, pady=5)

        self.update_btn = tk.Button(btn_frame, text="Оновити базу", width=20, command=self.update_db)
        self.update_btn.grid(row=1, column=1, padx=5, pady=5)

        # Прогресбар
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", maximum=100)
        self.progress.pack(pady=5)

        # Відсотки прогресу
        self.progress_label = tk.Label(root, text="0%")
        self.progress_label.pack()

        # Відсоток безпеки комп'ютера
        self.security_label = tk.Label(root, text="Безпека комп'ютера: 100%", font=("Arial", 12, "bold"), fg="green")
        self.security_label.pack(pady=5)
        self.security_percent = 100  # Початково 100%

        # Лог/статус
        self.status = tk.Label(root, text="Готово до роботи", anchor="w", font=("Arial", 11))
        self.status.pack(fill=tk.X, padx=10, pady=5)

        # Вихід
        exit_btn = tk.Button(root, text="Вихід", command=root.quit)
        exit_btn.pack(pady=10)

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
            else:
                # Якщо вірусів не знайдено, підвищуємо безпеку (але не більше 100)
                self.security_percent = min(100, self.security_percent + 2)
            color = "green" if self.security_percent >= 80 else "orange" if self.security_percent >= 50 else "red"
            self.security_label.config(text=f"Безпека комп'ютера: {self.security_percent}%", fg=color)
        messagebox.showinfo("Антивірус", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = AntivirusApp(root)
    root.mainloop()