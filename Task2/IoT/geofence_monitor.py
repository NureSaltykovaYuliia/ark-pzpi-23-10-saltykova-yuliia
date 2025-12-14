"""
Модуль моніторингу геозони для IoT пристрою
Перевіряє чи собака не вийшла за межі безпечної зони
Відправляє уведомлення на сервер БЕЗ авторизації
"""

import config
import geo


class GeofenceMonitor:
    """Клас для моніторингу геозони"""

    def __init__(self):
        self.safe_zone_lat = config.DANGER_ZONE["lat"]
        self.safe_zone_lon = config.DANGER_ZONE["lon"]
        self.safe_zone_radius = config.DANGER_ZONE["radius"]
        self.is_in_danger = False
        self.last_alert_sent = False

    def check_position(self, latitude, longitude):
        """
        Перевірка чи знаходиться собака в безпечній зоні

        Args:
            latitude: Поточна широта
            longitude: Поточна довгота

        Returns:
            tuple: (is_safe, distance) - чи в безпеці, відстань в метрах
        """
        # Обчислюємо відстань від центру безпечної зони
        distance = geo.get_distance_meters(
            self.safe_zone_lat,
            self.safe_zone_lon,
            latitude,
            longitude
        )

        is_safe = distance <= self.safe_zone_radius

        if config.DEBUG:
            status = "БЕЗПЕЧНО" if is_safe else "НЕБЕЗПЕКА!"
            print(f"[GEOFENCE] Відстань від центру: {distance:.0f}м / {self.safe_zone_radius}м [{status}]")

        return (is_safe, distance)

    def send_danger_alert(self, latitude, longitude, distance, dog_id, device_manager):
        """
        Відправка сповіщення про небезпеку на сервер БЕЗ авторизації
        Використовує device_manager для відправки через API

        Args:
            latitude: Координата широти
            longitude: Координата довготи
            distance: Відстань від безпечної зони
            dog_id: ID собаки
            device_manager: Екземпляр DeviceManager для відправки уведомлень

        Returns:
            bool: True якщо сповіщення успішно відправлено
        """
        title = "⚠ Собака вийшла за межи безпечної зони!"
        message = f"Собака знаходиться на відстані {distance:.0f}м від центру безпечної зони. Координати: {latitude:.6f}, {longitude:.6f}"
        notification_type = "danger_zone"

        print("[GEOFENCE] Відправка сповіщення про небезпеку...")

        # Передаємо тільки необхідні параметри - related_entity_id більше не потрібен
        if device_manager.send_notification(title, message, notification_type, dog_id):
            print(f"[GEOFENCE] ✓ Сповіщення про небезпеку відправлено!")
            self.last_alert_sent = True
            return True
        else:
            print(f"[GEOFENCE] ✗ Помилка при відправці сповіщення")
            return False


# Глобальний екземпляр моніторингу геозони
geofence_monitor = GeofenceMonitor()
