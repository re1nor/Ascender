from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Данные
times = ['12:52:31', '12:53:31', '12:58:31']  # Временные метки
values = [10, 15, 20]  # Соответствующие значения

# Преобразуем строки времени в объекты datetime
formatted_times = [datetime.strptime(t, "%H:%M:%S") for t in times]

# Создаем график
fig, ax = plt.subplots()

# Построение графика
ax.plot(formatted_times, values, marker='o')

# Устанавливаем формат отображения времени на оси X
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

# Автоматическое форматирование для лучшего отображения меток
fig.autofmt_xdate()

# Подписываем оси
ax.set_xlabel("Время")
ax.set_ylabel("Значения")

# Показываем график
plt.show()
