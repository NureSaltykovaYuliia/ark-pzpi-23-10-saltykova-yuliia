"""
Модуль моніторингу геозони для IoT пристрою
Перевіряє чи собака не вийшла за межі безпечної зони
"""

import config
import geo
import urequests
import ujson
from auth import auth_manager


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

    def send_danger_alert(self, latitude, longitude, distance, dog_id):
        """
        Відправка сповіщення про небезпеку на сервер

        Args:
            latitude: Координата широти
            longitude: Координата довготи
            distance: Відстань від безпечної зони
            dog_id: ID собаки

        Returns:
            bool: True якщо сповіщення успішно відправлено
        """
        if not auth_manager.is_authenticated():
            print("[GEOFENCE] ✗ Неможливо відправити сповіщення: не авторизовано")
            return False

        url = config.API_BASE_URL + config.API_ALERTS

        payload = {
            "type": 0,  # DangerZone
            "message": f"Собака вийшла за межі безпечної зони! Відстань: {distance:.0f}м",
            "latitude": latitude,
            "longitude": longitude,
            "dogId": dog_id
        }

        try:
            if config.DEBUG:
                print(f"[GEOFENCE] Відправка сповіщення про небезпеку...")
                print(f"[GEOFENCE] URL: {url}")

            response = urequests.post(
                url,
                headers=auth_manager.get_auth_header(),
                data=ujson.dumps(payload)
            )

            if config.DEBUG:
                print(f"[GEOFENCE] Статус відповіді: {response.status_code}")

            if response.status_code == 201:
                print(f"[GEOFENCE] ✓ Сповіщення про небезпеку відправлено!")
                self.last_alert_sent = True
                response.close()
                return True
            else:
                try:
                    error_data = response.json()
                    print(f"[GEOFENCE] ✗ Помилка: {error_data.get('message', 'Невідома помилка')}")
                except:
                    print(f"[GEOFENCE] ✗ Помилка: статус {response.status_code}")
                response.close()
                return False

        except Exception as e:
            print(f"[GEOFENCE] ✗ Виняток при відправці: {e}")
            return False


# Глобальний екземпляр моніторингу геозони
geofence_monitor = GeofenceMonitor()
