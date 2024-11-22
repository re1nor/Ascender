import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from log_window import LogWindow
from monitoring_window import MonitoringWindow
from server import Server


class AppWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Ascender Data Viewer")

        # Устанавливаем фиксированный размер окна
        self.master.geometry("280x400")
        # self.master.resizable(False, False)
        self.master.configure(bg="#d3d3d3")

        # Поток открытого сокета сервера
        self.thread = None

        ### Создаем сервер
        self.server = Server(self.update_server_status,master)

        # Основной фрейм
        main_frame = tk.Frame(self.master, padx=10, pady=10, bg="#808080")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Раздел "Онлайн обработка"
        online_frame = tk.LabelFrame(main_frame, text="Мониторинг", padx=10, pady=10, bg="#808080")
        online_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Онлайн раздел будет занимать больше места
        online_frame.grid_propagate(False)

        # Поле для ввода порта (Label и Entry в одной строке)
        self.address_label = tk.Label(online_frame, text="Port:", bg="#808080", width=5)
        self.address_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.address_entry = tk.Entry(online_frame, width=20)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Кнопка "Запуск сервера" (по центру)
        self.server_button = tk.Button(
            online_frame, text="Запуск сервера", command=self.toggle_server, width=25, bg="#C0C0C0"
        )
        self.server_button.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        # Лог событий сервера (по центру)
        self.log_server = tk.scrolledtext.ScrolledText(
            online_frame, wrap="word", height=5, width=25, state='disabled', bg="#DCDCDC"
        )
        self.log_server.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

        # Кнопка "Мониторинг" (по центру)
        self.monitoring_button = tk.Button(
            online_frame, text="Мониторинг", command=self.open_monitoring_window, width=25, state=tk.DISABLED,
            bg="#98FB98"
        )
        self.monitoring_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Раздел "Офлайн обработка"
        offline_frame = tk.LabelFrame(main_frame, text="Просмотр лога", padx=10, pady=10, bg="#808080")
        offline_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

        # Кнопка "Загрузить CSV лог"
        self.load_log_button = tk.Button(
            offline_frame, text="Загрузить CSV лог", command=self.open_log_window, width=30, bg="#C0C0C0"
        )
        self.load_log_button.grid(row=0, column=0, pady=10, sticky="ew")

    def toggle_server(self):
        """Обрабатывает запуск и остановку сервера."""
        if self.server.is_monitoring:
            self.server.stop_monitoring(self.thread)
            self.server_button.config(text="Запуск сервера")
            self.monitoring_button.config(state=tk.DISABLED)
        else:
            address = self.address_entry.get().strip()
            if not address:
                self.update_server_status("Ошибка: адрес сервера не указан")
                return

            success_code, self.thread = self.server.start_monitoring(address)
            self.server_button.config(text="Остановить сервер")

    def update_server_status(self, status_message):
        """Обновляет статус сервера на основе callback от сервера."""
        if status_message == "Соединение с терминалом настроено":
            self.monitoring_button.config(state=tk.NORMAL)

        self.log_server.configure(state='normal')
        self.log_server.insert("end", "\n" + status_message)
        self.log_server.configure(state='disabled')

    def open_monitoring_window(self):
        """Открывает окно мониторинга."""
        self.master.withdraw()  # Скрываем главное окно
        MonitoringWindow.create_window(self.master, self.server.data_package)

    def open_log_window(self):
        """Открывает окно для логов."""
        file_path = filedialog.askopenfilename(
            title="Выберите CSV лог",
            filetypes=(("CSV файлы", "*.csv"), ("Все файлы", "*.*"))
        )
        if file_path:
            self.master.withdraw()  # Скрываем главное окно
            LogWindow.create_window(self.master, file_path)
    # def open_graph_window(self, mode, file_path=None):
    #     """Скрывает текущее окно и открывает GraphWindow."""
    #     self.master.withdraw()
    #     new_root = tk.Tk()
    #     if mode == "monitoring":
    #         graph_window = GraphWindow(new_root, self.reopen_main_window, mode, data_package=self.server.data_package)
    #     elif mode == "log":
    #         graph_window = GraphWindow(new_root, self.reopen_main_window, mode, file_path)
    #     graph_window.create_window()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppWindow(root)
    root.mainloop()
