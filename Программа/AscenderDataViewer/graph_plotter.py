# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


class GraphPlotter:
    def __init__(self, title, x_label, y_label, unit_name):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.unit_name = unit_name
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

    def plot_graph(self, x_data, y_data):
        """Построение графика."""
        self.ax.plot(x_data, y_data, label=self.title)
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(f"{self.y_label} ({self.unit_name})")

        # Настройка делений на осях
        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True, numticks=20))  # Ось X
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True, numticks=20))  # Ось Y

        # Отображение сетки и легенды
        self.ax.grid(True)
        self.ax.legend()

        plt.show()



