"""
Модуль управління Smart Device для IoT пристрою
Відповідає за реєстрацію пристрою та відправку даних на сервер
"""

import urequests
import ujson
import config
from auth import auth_manager
from gps_sensor import gps_sensor
from battery_monitor import battery_monitor


class DeviceManager:
    """Клас для управління розумним пристроєм"""

    def __init__(self):
        self.device_id = None
        self.device_guid = config.DEVICE_GUID
        self.dog_id = config.DOG_ID
        self.is_registered = False

    def register_device(self, dog_id):
        """
        Реєстрація пристрою на сервері через CreateDevice endpoint
        POST /api/smartdevices
        Використовує CreateSmartDeviceDto: {deviceGuid, dogId}

        Args:
            dog_id: ID собаки, до якої прив'язується пристрій

        Returns:
            bool: True якщо реєстрація успішна
        """
        if not auth_manager.is_authenticated():
            print("[DEVICE] ✗ Неможливо зареєструвати пристрій: користувач не авторизований")
            return False

        url = config.API_BASE_URL + config.API_SMART_DEVICES

        payload = {
            "deviceGuid": self.device_guid,
            "dogId": dog_id
        }

        try:
            if config.DEBUG:
                print(f"[DEVICE] Реєстрація пристрою: {self.device_guid}")
                print(f"[DEVICE] Dog ID: {dog_id}")
                print(f"[DEVICE] URL: {url}")

            response = urequests.post(
                url,
                headers=auth_manager.get_auth_header(),
                data=ujson.dumps(payload)
            )

            if config.DEBUG:
                print(f"[DEVICE] Статус відповіді: {response.status_code}")

            if response.status_code == 201:
                data = response.json()
                self.device_id = data.get("id")
                self.dog_id = dog_id
                self.is_registered = True
                print(f"[DEVICE] ✓ Пристрій успішно зареєстровано (ID: {self.device_id})")
                response.close()
                return True
            else:
                try:
                    error_data = response.json()
                    print(f"[DEVICE] ✗ Помилка реєстрації: {error_data.get('message', 'Невідома помилка')}")
                except:
                    print(f"[DEVICE] ✗ Помилка реєстрації: статус {response.status_code}")
                response.close()
                return False

        except Exception as e:
            print(f"[DEVICE] ✗ Виняток при реєстрації: {e}")
            return False

    def send_telemetry(self):
        """
        Відправка телеметричних даних на сервер
        (GPS координати та рівень батареї)

        Returns:
            bool: True якщо дані успішно відправлені
        """
        if not self.is_registered:
            print("[DEVICE] ✗ Пристрій не зареєстровано")
            return False

        if not auth_manager.is_authenticated():
            print("[DEVICE] ✗ Користувач не авторизований")
            return False

        # Отримання даних з сенсорів
        latitude, longitude = gps_sensor.read_coordinates()
        battery_level = battery_monitor.read_battery_level()

        if latitude is None or longitude is None:
            print("[DEVICE] ✗ GPS координати недоступні")
            return False

        url = f"{config.API_BASE_URL}{config.API_SMART_DEVICES}/{self.device_id}"

        payload = {
            "lastLatitude": latitude,
            "lastLongitude": longitude,
            "batteryLevel": battery_level
        }

        try:
            if config.DEBUG:
                print(f"[DEVICE] Відправка телеметрії:")
                print(f"  GPS: {latitude:.6f}, {longitude:.6f}")
                print(f"  Батарея: {battery_level:.1f}%")
                print(f"[DEVICE] URL: {url}")

            response = urequests.put(
                url,
                headers=auth_manager.get_auth_header(),
                data=ujson.dumps(payload)
            )

            if config.DEBUG:
                print(f"[DEVICE] Статус відповіді: {response.status_code}")

            if response.status_code == 204:
                print(f"[DEVICE] ✓ Телеметрія відправлена успішно")
                response.close()
                return True
            else:
                try:
                    error_data = response.json()
                    print(f"[DEVICE] ✗ Помилка відправки: {error_data.get('message', 'Невідома помилка')}")
                except:
                    print(f"[DEVICE] ✗ Помилка відправки: статус {response.status_code}")
                response.close()
                return False

        except Exception as e:
            print(f"[DEVICE] ✗ Виняток при відправці телеметрії: {e}")
            return False

    def get_device_info(self):
        """
        Отримання інформації про пристрій з сервера

        Returns:
            dict: Інформація про пристрій або None
        """
        if not self.device_id:
            print("[DEVICE] Пристрій ще не зареєстровано")
            return None

        if not auth_manager.is_authenticated():
            print("[DEVICE] Користувач не авторизований")
            return None

        url = f"{config.API_BASE_URL}{config.API_SMART_DEVICES}/{self.device_id}"

        try:
            response = urequests.get(
                url,
                headers=auth_manager.get_auth_header()
            )

            if response.status_code == 200:
                data = response.json()
                response.close()
                return data
            else:
                print(f"[DEVICE] Помилка отримання інформації: {response.status_code}")
                response.close()
                return None

        except Exception as e:
            print(f"[DEVICE] Виняток при отриманні інформації: {e}")
            return None


# Глобальний екземпляр менеджера пристрою
device_manager = DeviceManager()
