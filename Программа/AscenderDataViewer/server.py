import threading
import time
import random
from datetime import datetime
import re
import socket
import threading
from threading import Thread
import csv
import json
from tkinter import *
from tkinter import ttk


class Server:
    def __init__(self, callback, mainWindow):
        self.is_monitoring = False
        self.tunnel_address = None  # Порт
        self.callback = callback  # Callback для уведомления интерфейса о статусах
        self.data_thread = None  # Поток для генерации данных
        self.data_package = ()  # Стартовое значение пустого пакета данных
        self.SERVER_ADDRESS = ()
        # Список с распаршенными данными
        self.decodedArray = []

    def validate_address(self, address):
        """Проверяет формат адреса сервера."""
        pattern = r"^(http:\/\/|https:\/\/)?[a-zA-Z0-9.-]+(:[0-9]{1,5})?$"
        return re.match(pattern, address) is not None

    def start_monitoring(self, port):
        """Имитирует запуск сервера и настройку соединения."""
        # if not address or not self.validate_address(address):
        #     self.callback("Ошибка: неверный адрес сервера")
        #     return False
        self.SERVER_ADDRESS = ('localhost', int(port))

        self.is_monitoring = True

        # Создаем поток для запуска и настройки сервера
        thread = threading.Thread(target=self.listen_socket, daemon=True)
        thread.start()
        return True, thread

    def exitServer(thread):
        thread.do_run = False
        sys.exit()

    # Записывает decodedArray в
    def writeToCsv():
        keys = self.decodedArray[0].keys()
        with open("people2.csv", 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.decodedArray)

    def parseToDictArray(packet):
        dictSave = {}
        dataInPackets = packet.split(",")

        # Разделение на данные в одном подпакете
        firstData = dataInPackets[0].split(";")

        # Дата
        dictSave["Date"] = dataInPackets[0][0:6]
        dictSave["Date"] = str(dictSave["Date"][0:2]) + "." + str(dictSave["Date"][2:4]) + "." + str(
            dictSave["Date"][4:6])

        # Время
        dictSave["Time"] = dataInPackets[0][7:13]
        dictSave["Time"] = str(dictSave["Time"][0:2]) + ":" + str(dictSave["Time"][2:4]) + ":" + str(
            dictSave["Time"][4:6])

        timeX.append(dictSave["Date"] + " " + dictSave["Time"])

        # Скорость
        dictSave["Speed"] = firstData[10]
        if (dictSave["Speed"] == "NA"):
            speedY.append(0)
        else:
            speedY.append(dictSave["Speed"])

        dictSave["Course"] = firstData[7]
        # Высота
        dictSave["Altitude"] = firstData[8]
        if (dictSave["Altitude"] == "NA"):
            altitudeY.append(None)
        else:
            altitudeY.append(dictSave["Altitude"])

        # Долгота
        dictSave["Longitude"] = firstData[4]

        if (dictSave["Longitude"] == "NA"):

            longitudeX.append(None)
        else:
            # Минуты и секунды в доли
            minutes = float(dictSave["Longitude"][3:]) / 60
            dictSave["Longitude"] = int(dictSave["Longitude"][1:3]) + minutes
            longitudeX.append(dictSave["Longitude"])

        # Широта
        dictSave["Latitude"] = firstData[2]

        if (dictSave["Latitude"] == "NA"):

            latitudeY.append(None)
        else:
            # Минуты и секунды в доли
            minutes = float(dictSave["Latitude"][2:]) / 60
            dictSave["Latitude"] = int(dictSave["Latitude"][:2]) + minutes
            latitudeY.append(dictSave["Latitude"])

        # Тепература
        dictSave["Temperature"] = dataInPackets[2][16:]
        # Вольтаж
        dictSave["Voltage"] = firstData[15].split(":")[2]

        # Вывод в JSON для удобного просмотра
        print(json.dumps(dictSave, sort_keys=True, indent=4))

        # Добавление в массив
        self.decodedArray.append(dictSave)

        # Обновление графиков
        # updatePlot()

        writeToCsv()

    def listen_socket(self):
        t = threading.current_thread()

        # Настраиваем сокет
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.SERVER_ADDRESS)
        server_socket.listen(10)
        self.callback("Сервер запущен, ождание подключения...")
        print('server is running, please, press ctrl+c to stop', flush=True)

        while getattr(t, "do_run", True):
            # Получаем соединение

            connection, address = server_socket.accept()
            self.callback("Новое соединение: {address}".format(address=address))
            print("new connection from {address}".format(address=address))

            # Получаем данные

            while getattr(t, "do_run", True):
                # Получаем пакет
                self.callback("Ожидание пакета")
                print("Waiting for packet...")
                data = connection.recv(1024)
                print("Got packet: ", str(data)[2:5])

                # Если запрос на регистрацию
                if (str(data)[2:5] == "#L#"):
                    self.callback("Получен пакет на регистрацию")
                    # Возвращаем согласием на регистрацию терминала
                    authSecces = bytes("#AL#1\r\n", encoding='UTF-8')
                    connection.send(authSecces)
                    print(str(authSecces))

                # Если запрос на передачу данных
                elif (str(data)[2:5] == "#B#"):

                    self.callback("Получен пакет c данными")
                    # Разделить пакет на подпакеты
                    splitted = str(data)[5:].split("|")
                    print(splitted)

                    numOfPackets = len(splitted)

                    # Для каждого подпакета
                    for i in range(len(splitted) - 1):
                        parseToDictArray(splitted[i])

                    answer = bytes("#AB#" + str(numOfPackets) + "\r\n", encoding='UTF-8')
                    connection.send(answer)
                    print(answer)
                    break

                else:
                    print("Unknown packet:", str(data))
                    break

            connection.close()

    def stop_monitoring(self, thread):
        """Остановка сервера."""
        thread.do_run = False
        self.is_monitoring = False
        self.data_package = ()  # Очищаем данные
        self.callback("Сервер остановлен")

    def _simulate_startup_process(self):
        """Имитация этапов запуска сервера и настройки."""
        self.callback("Ожидайте. Запуск сервера...")
        time.sleep(2)  # Задержка для имитации запуска
        self.callback("Сервер запущен. Настраиваем соединение с терминалом...")
        time.sleep(2)  # Задержка для имитации настройки соединения
        self.callback("Соединение с терминалом настроено")

        # Начинаем посылать данные после настройки
        self.start_data_stream()

    def start_data_stream(self):
        """Запуск потока генерации данных."""
        self.data_thread = threading.Thread(target=self._simulate_data_stream, daemon=True)
        self.data_thread.start()

    def _simulate_data_stream(self):
        """Имитация потока данных."""
        while self.is_monitoring:
            data = self.generate_data()
            self.data_package = data  # Обновление данных пакета
            print(data)
            time.sleep(1)  # Задержка между отправками данных

    def generate_data(self):
        """Генерация случайных данных и возврат их в виде кортежа."""
        timestamp = datetime.now().strftime("%H%M%S")
        datestamp = datetime.now().strftime("%Y%m%d")
        gps_lat = round(random.uniform(-90, 90), 6)
        gps_lon = round(random.uniform(-180, 180), 6)
        gps_alt = round(random.uniform(0, 5000), 2)
        speed = round(random.uniform(0, 120), 2)
        course = round(random.uniform(0, 360), 2)

        # Возвращаем данные в виде кортежа
        return (timestamp, datestamp, gps_lat, gps_lon, gps_alt, speed, course)

