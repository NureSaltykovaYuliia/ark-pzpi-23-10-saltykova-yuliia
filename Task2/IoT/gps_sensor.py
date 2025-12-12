"""
Модуль GPS сенсора для IoT пристрою
Симулює GPS координати для тестування в Wokwi з реалістичною симуляцією ходьби
"""

import config
import random
import math


class GPSSensor:
    """Клас для роботи з GPS сенсором (симуляція з реалістичною ходьбою)"""

    def __init__(self):
        self.latitude = config.DEFAULT_LATITUDE
        self.longitude = config.DEFAULT_LONGITUDE
        self.is_active = True

        # Параметри для симуляції ходьби
        self.angle = random.uniform(0, 360)  # Початковий кут напрямку руху
        self.distance_from_center = 0.0  # Відстань від базової точки (в градусах)
        self.step_size = 0.0002  # Розмір кроку (~20 метрів)
        self.max_distance = 0.002  # Максимальна відстань від центру (~200 метрів)

    def read_coordinates(self):
        """
        Зчитування GPS координат з симуляцією реалістичної ходьби
        Собака рухається випадково, іноді заходячи за межі безпечної зони

        Returns:
            tuple: (latitude, longitude)
        """
        if not self.is_active:
            return (None, None)

        # Симуляція випадкової ходьби (Random Walk)
        # Собака змінює напрямок руху з певною ймовірністю
        if random.random() < 0.3:  # 30% шанс змінити напрямок
            self.angle += random.uniform(-45, 45)  # Повертаємо на ±45 градусів

        # Конвертуємо кут в радіани
        angle_rad = math.radians(self.angle)

        # Обчислюємо нові координати
        lat_change = self.step_size * math.cos(angle_rad)
        lon_change = self.step_size * math.sin(angle_rad)

        # Оновлюємо позицію
        self.latitude += lat_change
        self.longitude += lon_change

        # Обчислюємо відстань від базової точки
        self.distance_from_center = math.sqrt(
            (self.latitude - config.DEFAULT_LATITUDE)**2 +
            (self.longitude - config.DEFAULT_LONGITUDE)**2
        )

        # Якщо собака зайшла надто далеко - повертаємо її назад
        if self.distance_from_center > self.max_distance:
            # Повертаємо напрямок до центру
            self.angle = math.degrees(math.atan2(
                config.DEFAULT_LONGITUDE - self.longitude,
                config.DEFAULT_LATITUDE - self.latitude
            ))
            if config.DEBUG:
                print(f"[GPS] Собака занадто далеко ({self.distance_from_center*111000:.0f}м), повертаємо назад")

        if config.DEBUG:
            distance_meters = self.distance_from_center * 111000  # конверсія градусів в метри
            print(f"[GPS] Координати: {self.latitude:.6f}, {self.longitude:.6f}")
            print(f"[GPS] Відстань від дому: {distance_meters:.0f} м")

        return (self.latitude, self.longitude)

    def get_last_position(self):
        """
        Отримання останньої відомої позиції

        Returns:
            tuple: (latitude, longitude)
        """
        return (self.latitude, self.longitude)

    def set_position(self, latitude, longitude):
        """
        Встановлення позиції (для тестування)

        Args:
            latitude: Широта
            longitude: Довгота
        """
        self.latitude = latitude
        self.longitude = longitude
        print(f"[GPS] Позиція встановлена: {latitude}, {longitude}")

    def activate(self):
        """Активація GPS сенсора"""
        self.is_active = True
        print("[GPS] Сенсор активовано")

    def deactivate(self):
        """Деактивація GPS сенсора"""
        self.is_active = False
        print("[GPS] Сенсор деактивовано")


# Глобальний екземпляр GPS сенсора
gps_sensor = GPSSensor()
