import tkinter as tk
import csv

import numpy as np

from graph_window import GraphWindow


class LogWindow:
    def __init__(self, master, parent_window, file_path):
        self.master = master
        self.parent_window = parent_window
        self.file_path = file_path
        self.data = {}
        self.processed_data = {}

    @classmethod
    def create_window(cls, parent_window, file_path):
        new_root = tk.Tk()
        new_root.resizable(False, False)  # Отключает изменение размера по горизонтали и вертикали
        log_window = cls(new_root, parent_window, file_path)
        log_window.setup_window()

    def setup_window(self):
        """Настройка окна."""
        self.master.title(f"Просмотр лога {self.file_path}")
        self.master.geometry("490x720")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Загрузка и обработка данных
        self.data = self.load_csv_to_dict(self.file_path)
        self.process_data()

        # Основной фрейм
        main_frame = tk.Frame(self.master, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        label_width = 20
        entry_width = 20

        # Поля для отображения начала и конца записи
        date_frame = tk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=10)

        tk.Label(date_frame, text="Начало записи", font=("Arial", 12), width=12,
                 anchor="e").grid(row=0, column=0, sticky="w")
        self.start_time = tk.Entry(date_frame, font=("Arial", 12), width=17)
        self.start_time.grid(row=0, column=1, padx=10)

        tk.Label(date_frame, text="Конец записи", font=("Arial", 12), width=12, anchor="e").grid(
            row=1, column=0, sticky="w")
        self.end_time = tk.Entry(date_frame, font=("Arial", 12), width=17)
        self.end_time.grid(row=1, column=1, padx=10)

        # Фрейм для "Скорость"
        speed_frame = tk.LabelFrame(main_frame, text="Скорость, (м/c)", font=("Arial", 12), padx=10, pady=10)
        speed_frame.pack(fill=tk.X, pady=10)

        tk.Label(speed_frame, text="Макс:", font=("Arial", 10), width=label_width, anchor="e").grid(row=0, column=0,
                                                                                                    sticky="w")
        self.speed_max = tk.Entry(speed_frame, font=("Arial", 10), width=entry_width)
        self.speed_max.grid(row=0, column=1, padx=10)

        show_button_speed = tk.Button(speed_frame, text="Показать",
                                      command=lambda: self.show_graph("speed"), font=("Arial", 10))
        show_button_speed.grid(row=0, column=2, padx=10)

        # Фрейм для "Линейное ускорение"
        acceleration_frame = tk.LabelFrame(main_frame, text="Линейное ускорение, (м/с^2)", font=("Arial", 12), padx=10, pady=10)
        acceleration_frame.pack(fill=tk.X, pady=10)

        tk.Label(acceleration_frame, text="Макс:", font=("Arial", 10), width=label_width, anchor="e").grid(row=0,
                                                                                                           column=0,
                                                                                                           sticky="w")
        self.acceleration_max = tk.Entry(acceleration_frame, font=("Arial", 10), width=entry_width)
        self.acceleration_max.grid(row=0, column=1, padx=10)

        show_button_acceleration = tk.Button(acceleration_frame, text="Показать",
                                             command=lambda: self.show_graph("lin_acc"), font=("Arial", 10))
        show_button_acceleration.grid(row=0, column=2, padx=10)

        # Фрейм для "Скорость смены курса"
        course_rate_frame = tk.LabelFrame(main_frame, text="Скорость смены курса, (град/с)", font=("Arial", 12), padx=10, pady=10)
        course_rate_frame.pack(fill=tk.X, pady=10)

        tk.Label(course_rate_frame, text="Макс:", font=("Arial", 10), width=label_width, anchor="e").grid(row=0,
                                                                                                          column=0,
                                                                                                          sticky="w")
        self.course_rate_max = tk.Entry(course_rate_frame, font=("Arial", 10), width=entry_width)
        self.course_rate_max.grid(row=0, column=1, padx=10)

        show_button_course_rate = tk.Button(course_rate_frame, text="Показать",
                                            command=lambda: self.show_graph("course_rate"), font=("Arial", 10))
        show_button_course_rate.grid(row=0, column=2, padx=10)

        # Фрейм для "Скороподъёмность"
        climb_rate_frame = tk.LabelFrame(main_frame, text="Скороподъёмность, (м/с)", font=("Arial", 12), padx=10, pady=10)
        climb_rate_frame.pack(fill=tk.X, pady=10)

        tk.Label(climb_rate_frame, text="Макс:", font=("Arial", 10), width=label_width, anchor="e").grid(row=0,
                                                                                                         column=0,
                                                                                                         sticky="w")
        self.height_rate_max = tk.Entry(climb_rate_frame, font=("Arial", 10), width=entry_width)
        self.height_rate_max.grid(row=0, column=1, padx=10)

        show_button_height_rate = tk.Button(climb_rate_frame, text="Показать",
                                            command=lambda: self.show_graph("height_rate"), font=("Arial", 10))
        show_button_height_rate.grid(row=0, column=2, padx=10)

        # Фрейм для "Высота"
        altitude_frame = tk.LabelFrame(main_frame, text="Высота, (м)", font=("Arial", 12), padx=10, pady=10)
        altitude_frame.pack(fill=tk.X, pady=10)

        tk.Label(altitude_frame, text="Макс:", font=("Arial", 10), width=label_width, anchor="e").grid(row=0, column=0,
                                                                                                       sticky="w")
        self.altitude_max = tk.Entry(altitude_frame, font=("Arial", 10), width=entry_width)
        self.altitude_max.grid(row=0, column=1, padx=10)

        tk.Label(altitude_frame, text="Стартовая:", font=("Arial", 10), width=label_width, anchor="e").grid(row=1,
                                                                                                            column=0,
                                                                                                            sticky="w")
        self.altitude_start = tk.Entry(altitude_frame, font=("Arial", 10), width=entry_width)
        self.altitude_start.grid(row=1, column=1, padx=10)

        show_button_altitude = tk.Button(altitude_frame, text="Показать",
                                         command=lambda: self.show_graph("altitude"), font=("Arial", 10))
        show_button_altitude.grid(row=0, column=2, padx=10)

        # Фрейм для "Маршрут"
        route_frame = tk.LabelFrame(main_frame, text="Маршрут", font=("Arial", 12), padx=10, pady=10)
        route_frame.pack(fill=tk.X, pady=10)

        tk.Label(route_frame, text="Пробег, (км):", font=("Arial", 10), width=label_width, anchor="e").grid(row=0,
                                                                                                            column=0,
                                                                                                            sticky="w")
        self.route_total = tk.Entry(route_frame, font=("Arial", 10), width=entry_width)
        self.route_total.grid(row=0, column=1, padx=10)

        tk.Label(route_frame, text="Макс. удалённость, (км):", font=("Arial", 10), width=label_width, anchor="e").grid(
            row=1, column=0, sticky="w")
        self.route_max_distance = tk.Entry(route_frame, font=("Arial", 10), width=entry_width)
        self.route_max_distance.grid(row=1, column=1, padx=10)

        tk.Label(route_frame, text="Длительность, (мин):", font=("Arial", 10), width=label_width, anchor="e").grid(row=2,
                                                                                                            column=0,
                                                                                                            sticky="w")
        self.route_duration = tk.Entry(route_frame, font=("Arial", 10), width=entry_width)
        self.route_duration.grid(row=2, column=1, padx=10)

        self.write_res()

    def on_close(self):
        """Возвращаемся к главному окну при закрытии."""
        self.master.destroy()
        self.parent_window.deiconify()

    def load_csv_to_dict(self, file_path):
        """Читает CSV-файл и возвращает словарь списков."""
        data = {
            "timestamp": [],
            "speed": [],
            "course": [],
            "altitude": [],
            "latitude": [],
            "longitude": []
        }
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                data["timestamp"].append(row["Date"] + " " + row["Time"])
                data["speed"].append(np.nan if row["Speed"] == 'NA' else float(row["Speed"]))
                data["course"].append(np.nan if row["Course"] == 'NA' else float(row["Course"]))
                data["altitude"].append(np.nan if row["Altitude"] == 'NA' else float(row["Altitude"]))
                data["latitude"].append(np.nan if row["Latitude"] == 'NA' else float(row["Latitude"]))
                data["longitude"].append(np.nan if row["Longitude"] == 'NA' else float(row["Longitude"]))
        return data

    def process_data(self):
        """Обрабатывает данные с использованием DataProcessor."""
        from data_processor import DataProcessor  # Импортируем ваш класс DataProcessor
        processor = DataProcessor(self.data)
        self.processed_data = processor.process_data()
        self.total_dist = processor.calc_total_dist_len()
        self.max_distance = processor.calc_max_distance()
        self.start_height = processor.calc_start_height()

    def write_res(self):
        """Заполняет поля Entry обработанными данными."""
        self.start_time.insert(0, self.processed_data.get("timestamp", "N/A")[0])
        self.end_time.insert(0, self.processed_data.get("timestamp", "N/A")[-1])
        self.route_duration.insert(0, self.processed_data.get("time")[-1] / 60)

        self.speed_max.insert(0, max(self.processed_data.get("speed", []), default="N/A"))
        self.acceleration_max.insert(0, max(self.processed_data.get("lin_acc", []), default="N/A"))
        self.course_rate_max.insert(0, max(self.processed_data.get("course_rate", []), default="N/A"))
        self.height_rate_max.insert(0, max(self.processed_data.get("height_rate", []), default="N/A"))

        self.route_total.insert(0, self.total_dist)
        self.route_max_distance.insert(0, self.max_distance)

        altitude_data = self.processed_data.get("altitude")
        self.altitude_max.insert(0, max(altitude_data))
        self.altitude_start.insert(0, self.start_height)

    def show_graph(self, title):
        x_data = self.processed_data.get("timestamp")
        if title == 'speed':
            y_data = self.processed_data.get("speed")
            GraphWindow(title, "Время, (c)", "Скорость, (м/с)", x_data, y_data)
        elif title == 'lin_acc':
            y_data = self.processed_data.get("lin_acc")
            GraphWindow(title, "Время, (c)", "Линейное ускорение, (м/c^2)", x_data, y_data)
        elif title == 'course_rate':
            y_data = self.processed_data.get("course_rate")
            GraphWindow(title, "Время, (c)", "Скр. изм. курса, (м/c)", x_data, y_data)
        elif title == 'height_rate':
            y_data = self.processed_data.get("height_rate")
            GraphWindow(title, "Время, (c)", "Скороподъемность, (м/c)", x_data, y_data)
        elif title == 'altitude':
            y_data = self.processed_data.get("altitude")
            GraphWindow(title, "Время, (c)", "Абс. высота, (м)", x_data, y_data)


