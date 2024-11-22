import tkinter as tk


class MonitoringWindow:
    def __init__(self, master, parent_window, data_package):
        self.master = master
        self.parent_window = parent_window
        self.data_package = data_package

    @classmethod
    def create_window(cls, parent_window, data_package):
        new_root = tk.Tk()
        monitoring_window = cls(new_root, parent_window, data_package)
        monitoring_window.setup_window()

    def setup_window(self):
        self.master.title("Мониторинг")
        self.master.geometry("800x600")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        label = tk.Label(self.master, text="Окно мониторинга")
        label.pack(pady=10)

        # Добавьте логику мониторинга здесь

    def on_close(self):
        """Возвращаемся к главному окну при закрытии."""
        self.master.destroy()
        self.parent_window.deiconify()
