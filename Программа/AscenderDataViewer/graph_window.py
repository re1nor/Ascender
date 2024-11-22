import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates

class GraphWindow:
    def __init__(self, title, x_label, y_label, x_data, y_data, mode='dot'):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.x_data = x_data
        self.y_data = y_data
        self.mode = mode

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)

        # Форматирование оси X для отображения времени
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        # Initial plot
        if self.mode == 'step':
            self.plot, = self.ax.step(self.x_data, self.y_data)
        elif self.mode == 'dot':
            self.plot, = self.ax.plot(self.x_data, self.y_data)

        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))

        # Определение размера окна (количество точек на графике)
        self.window_size = 50  # Число точек, которые отображаются в одно время

        # Создание горизонтального ползунка для перемещения графика по оси X
        self.ax_slider = self.fig.add_axes([0.1, 0.01, 0.8, 0.01], facecolor='lightgoldenrodyellow')
        self.slider = Slider(self.ax_slider, None, 0, len(self.x_data) - self.window_size, valinit=0, valstep=1)

        self.slider.on_changed(self.update_graph)

        # Устанавливаем начальные пределы для оси X, чтобы показывался только фрагмент
        self.ax.set_xlim(self.x_data[0], self.x_data[self.window_size - 1])

        # Показать график
        plt.show()

    def update_graph(self, val):
        # Получение текущей позиции ползунка
        start_idx = int(self.slider.val)
        end_idx = start_idx + self.window_size  # Показать фиксированное число точек

        # Обновление данных на графике
        self.plot.set_data(self.x_data[start_idx:end_idx], self.y_data[start_idx:end_idx])

        # Перерасчет диапазона оси X для отображения новой области данных
        self.ax.set_xlim(self.x_data[start_idx], self.x_data[end_idx - 1])

        # Перерисовка графика
        self.fig.canvas.draw()