"""
Модуль моніторингу батареї для IoT пристрою
Симулює рівень заряду батареї
"""

import config
import random


class BatteryMonitor:
    """Клас для моніторингу рівня батареї"""

    def __init__(self, initial_level=100):
        self.battery_level = initial_level
        self.is_charging = False
        self.discharge_rate = 0.1  # % за вимір

    def read_battery_level(self):
        """
        Зчитування рівня заряду батареї
        У реальному пристрої - читання з ADC
        У симуляції - поступове зменшення рівня

        Returns:
            float: Рівень заряду батареї (0-100%)
        """
        if self.is_charging:
            # Якщо заряджається - повільно збільшуємо
            self.battery_level = min(100, self.battery_level + 0.5)
        else:
            # Якщо розряджається - повільно зменшуємо з невеликою випадковістю
            discharge = self.discharge_rate + random.uniform(-0.05, 0.05)
            self.battery_level = max(0, self.battery_level - discharge)

        if config.DEBUG:
            print(f"[BATTERY] Рівень заряду: {self.battery_level:.1f}%")

        # Попередження про низький заряд
        if self.battery_level < config.BATTERY_LOW_THRESHOLD and not self.is_charging:
            print(f"[BATTERY] ⚠ УВАГА! Низький заряд батареї: {self.battery_level:.1f}%")

        return self.battery_level

    def get_battery_level(self):
        """
        Отримання поточного рівня батареї без зміни стану

        Returns:
            float: Поточний рівень заряду
        """
        return self.battery_level

    def set_charging(self, charging):
        """
        Встановлення стану зарядки

        Args:
            charging: True якщо пристрій заряджається
        """
        self.is_charging = charging
        status = "заряджається" if charging else "розряджається"
        print(f"[BATTERY] Статус: {status}")

    def set_battery_level(self, level):
        """
        Встановлення рівня батареї (для тестування)

        Args:
            level: Рівень заряду (0-100)
        """
        self.battery_level = max(0, min(100, level))
        print(f"[BATTERY] Рівень батареї встановлено: {self.battery_level:.1f}%")

    def is_low_battery(self):
        """
        Перевірка чи батарея розряджена

        Returns:
            bool: True якщо батарея нижче порогу
        """
        return self.battery_level < config.BATTERY_LOW_THRESHOLD


# Глобальний екземпляр моніторингу батареї
battery_monitor = BatteryMonitor()
