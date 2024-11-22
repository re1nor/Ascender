import numpy as np
from geopy.distance import geodesic
from datetime import datetime


class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.speeds = np.array(self.data.get('speed', [])) / 3.6
        self.courses = np.array(self.data.get('course', []))
        self.altitudes = np.array(self.data.get('altitude', []))
        self.latitudes = np.array(self.data.get('latitude', []))
        self.longitudes = np.array(self.data.get('longitude', []))
        # timestamps <-> '21.11.24 06:13:01'
        self.date_time = [datetime.strptime(ts, "%d.%m.%y %H:%M:%S") for ts in self.data.get('timestamp')]
        self.time = np.array([(d_t - self.date_time[0]).total_seconds() for d_t in self.date_time])  # 0,1,2... (c)

    def calc_lin_acc(self):
        speed_diff = np.diff(self.speeds)
        time_diff = np.diff(self.time)
        accel = np.divide(speed_diff, time_diff, where=time_diff != 0)
        accel = np.insert(accel, 0, accel[0])  # добавляем начальное ускорение для соотв размерности
        accel = np.nan_to_num(accel, nan=0.0)
        return accel.tolist()

    def calc_course_rate(self):
        course_diff = np.diff(self.courses)
        time_diff = np.diff(self.time)
        course_rate = np.divide(course_diff, time_diff, where=time_diff != 0)
        course_rate = np.insert(course_rate, 0, course_rate[0])
        course_rate = np.nan_to_num(course_rate, nan=0.0)
        return course_rate.tolist()

    def calc_height_rate(self):
        height_diff = np.diff(self.altitudes)
        time_diff = np.diff(self.time)
        height_rate = np.divide(height_diff, time_diff, where=time_diff != 0)
        height_rate = np.insert(height_rate, 0, height_rate[0])
        height_rate = np.nan_to_num(height_rate, nan=0.0)
        return height_rate.tolist()

    def calc_max_distance(self):
        """Удаленность от начальной точки записи"""
        max_distance = 0
        mask_latitudes = ~np.isnan(self.latitudes)
        mask_longitudes = ~np.isnan(self.longitudes)
        latitudes = self.latitudes[mask_latitudes]
        longitudes = self.longitudes[mask_longitudes]
        start_point = (latitudes[0], longitudes[0])

        for i in range(len(longitudes)):
            current_point = (latitudes[i], longitudes[i])
            distance = geodesic(start_point, current_point).kilometers
            if distance > max_distance:
                max_distance = distance
        return max_distance

    def calc_total_dist_len(self):
        """Пробег"""
        total_length = 0.0
        mask_latitudes = ~np.isnan(self.latitudes)
        mask_longitudes = ~np.isnan(self.longitudes)
        latitudes = self.latitudes[mask_latitudes]
        longitudes = self.longitudes[mask_longitudes]
        for i in range(1, len(latitudes)):
            point1 = (latitudes[i - 1], longitudes[i - 1])
            point2 = (latitudes[i], longitudes[i])
            total_length += geodesic(point1, point2).kilometers
        return total_length

    def calc_start_height(self):
        return self.altitudes[~np.isnan(self.altitudes)][0]

    def process_data(self):
        return {
            'timestamp': self.date_time,
            'time': self.time.tolist(),
            'speed': np.nan_to_num(self.speeds, nan=0.0).tolist(),
            'altitude': np.nan_to_num(self.altitudes, nan=0.0).tolist(),
            'lin_acc': self.calc_lin_acc(),
            'course_rate': self.calc_course_rate(),
            'height_rate': self.calc_height_rate(),
        }
