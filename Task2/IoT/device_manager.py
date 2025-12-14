"""
Модуль управління Smart Device для IoT пристрою
Відповідає за реєстрацію пристрою та відправку даних на сервер
БЕЗ АВТОРИЗАЦІЇ! Повністю автономний режим
"""

import urequests
import ujson
import config
from gps_sensor import gps_sensor
from battery_monitor import battery_monitor


class DeviceManager:
    """Клас для управління розумним пристроєм"""

    def __init__(self):
        self.device_id = None
        self.device_guid = config.DEVICE_GUID
        self.dog_id = None  # Буде отримано з сервера автоматично
        self.is_registered = False
        self.dog_assigned = False

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
                # Якщо пристрій вже зареєстровано, спробуємо отримати його дані
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', '')
                    print(f"[DEVICE] ⚠ Помилка реєстрації: {error_msg}")

                    # Якщо пристрій вже існує, спробуємо його знайти
                    if "вже" in error_msg.lower() or response.status_code == 400:
                        print(f"[DEVICE] Пристрій можливо вже зареєстровано, пошук...")
                        response.close()

                        # Спроба отримати існуючий пристрій
                        if self._try_get_existing_device(dog_id):
                            return True

                except:
                    print(f"[DEVICE] ✗ Помилка реєстрації: статус {response.status_code}")

                response.close()
                return False

        except Exception as e:
            print(f"[DEVICE] ✗ Виняток при реєстрації: {e}")
            return False

    def _try_get_existing_device(self, dog_id):
        """
        Спроба отримати дані існуючого пристрою

        Args:
            dog_id: ID собаки

        Returns:
            bool: True якщо пристрій знайдено
        """
        try:
            # Спробуємо отримати пристрій за dog_id
            url = f"{config.API_BASE_URL}{config.API_SMART_DEVICES}/dog/{dog_id}"
            response = urequests.get(
                url,
                headers=auth_manager.get_auth_header()
            )

            if response.status_code == 200:
                data = response.json()
                device_guid = data.get("deviceGuid")

                # Перевіряємо, чи це той самий пристрій
                if device_guid == self.device_guid:
                    self.device_id = data.get("id")
                    self.dog_id = dog_id
                    self.is_registered = True
                    print(f"[DEVICE] ✓ Пристрій вже зареєстровано (ID: {self.device_id})")
                    response.close()
                    return True
                else:
                    print(f"[DEVICE] ✗ До цієї собаки прикріплений інший пристрій: {device_guid}")
                    response.close()
                    return False

            response.close()
            return False

        except Exception as e:
            print(f"[DEVICE] ✗ Помилка при пошуку існуючого пристрою: {e}")
            return False

    def send_telemetry(self):
        """
        Відправка телеметричних даних на сервер БЕЗ авторизації
        (GPS координати та рівень батареї)
        PUT /api/smartdevices/device/{id}/telemetry

        Returns:
            bool: True якщо дані успішно відправлені
        """
        if not self.is_registered:
            print("[DEVICE] ✗ Пристрій не зареєстровано")
            return False

        # Отримання даних з сенсорів
        latitude, longitude = gps_sensor.read_coordinates()
        battery_level = battery_monitor.read_battery_level()

        if latitude is None or longitude is None:
            print("[DEVICE] ✗ GPS координати недоступні")
            return False

        # Новий endpoint БЕЗ авторизації!
        url = f"{config.API_BASE_URL}{config.API_SMART_DEVICES}/device/{self.device_id}/telemetry"

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

            # Правильно серіалізуємо JSON для MicroPython
            json_data = ujson.dumps(payload)
            
            response = urequests.put(
                url,
                headers={"Content-Type": "application/json"},
                data=json_data
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


    def register_device_without_dog(self):
        """
        Реєстрація пристрою БЕЗ прив'язки до собаки
        POST /api/smartdevices/register-device
        Не потребує авторизації!

        Returns:
            bool: True якщо реєстрація успішна
        """
        url = f"{config.API_BASE_URL}{config.API_SMART_DEVICES}/register-device"

        payload = {
            "deviceGuid": self.device_guid
        }

        try:
            if config.DEBUG:
                print(f"[DEVICE] Реєстрація пристрою без собаки: {self.device_guid}")
                print(f"[DEVICE] URL: {url}")

            response = urequests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=ujson.dumps(payload)
            )

            if config.DEBUG:
                print(f"[DEVICE] Статус відповіді: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                self.device_id = data.get("id")
                self.dog_id = data.get("dogId")  # Може бути None
                self.is_registered = True
                self.dog_assigned = (self.dog_id is not None and self.dog_id != 0)

                print(f"[DEVICE] ✓ Пристрій зареєстровано (ID: {self.device_id})")
                if self.dog_assigned:
                    print(f"[DEVICE] ✓ Собака вже призначена (Dog ID: {self.dog_id})")
                else:
                    print(f"[DEVICE] ⚠ Собака ще не призначена")

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

    def check_dog_assignment(self):
        """
        Перевірка чи призначена собака до пристрою
        GET /api/smartdevices/device/{deviceGuid}/dog
        Не потребує авторизації!

        Returns:
            int|None: ID собаки або None якщо не призначена
        """
        url = f"{config.API_BASE_URL}{config.API_SMART_DEVICES}/device/{self.device_guid}/dog"

        try:
            response = urequests.get(url)

            if response.status_code == 200:
                data = response.json()
                dog_id = data.get("dogId")

                if dog_id is not None and dog_id != 0:
                    # Собака призначена!
                    if not self.dog_assigned:
                        print(f"[DEVICE] ✓ Собака призначена! Dog ID: {dog_id}")

                    self.dog_id = dog_id
                    self.dog_assigned = True
                    response.close()
                    return dog_id
                else:
                    # Собака ще не призначена
                    if self.dog_assigned:
                        print(f"[DEVICE] ⚠ Собаку відкріплено від пристрою")

                    self.dog_id = None
                    self.dog_assigned = False
                    response.close()
                    return None
            else:
                if config.DEBUG:
                    print(f"[DEVICE] Помилка перевірки призначення: {response.status_code}")
                response.close()
                return None

        except Exception as e:
            if config.DEBUG:
                print(f"[DEVICE] Виняток при перевірці призначення: {e}")
            return None

    def send_notification(self, title, message, notification_type, related_entity_id=None):
        """
        Відправка уведомлення на сервер БЕЗ авторизації
        POST /api/notifications
        Не потребує авторизації!

        Args:
            title: Заголовок уведомлення
            message: Текст уведомлення
            notification_type: Тип уведомлення (наприклад: "danger_zone", "low_battery", "device_alert")
            related_entity_id: Опціональний ID пов'язаної сутності (наприклад, ID собаки)

        Returns:
            bool: True якщо уведомлення успішно відправлено
        """
        if not self.dog_id:
            if config.DEBUG:
                print("[DEVICE] ⚠ Собака не призначена, уведомлення не буде відправлено")
            return False

        url = f"{config.API_BASE_URL}{config.API_NOTIFICATIONS}/iot-alert"

        # Для IoT сервер очікує: title, message, notificationType, dogId
        payload = {
            "title": title,
            "message": message,
            "notificationType": notification_type,
            "dogId": self.dog_id  # Використовуємо dogId замість relatedEntityId
        }

        try:
            if config.DEBUG:
                print(f"[DEVICE] Відправка уведомлення:")
                print(f"  Заголовок: {title}")
                print(f"  Текст: {message}")
                print(f"  Тип: {notification_type}")
                print(f"  DogId: {self.dog_id}")
                print(f"[DEVICE] URL: {url}")
                print(f"[DEVICE] Payload: {ujson.dumps(payload)}")

            # Правильно серіалізуємо JSON для MicroPython
            json_data = ujson.dumps(payload)
            
            # Відправляємо POST запит з явними headers
            response = urequests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json_data
            )

            if config.DEBUG:
                print(f"[DEVICE] Статус відповіді: {response.status_code}")

            if response.status_code == 201:
                print(f"[DEVICE] ✓ Уведомлення відправлено успішно")
                response.close()
                return True
            else:
                # Спробуємо отримати детальну помилку
                try:
                    response_text = response.text if hasattr(response, 'text') else response.content
                    if config.DEBUG:
                        print(f"[DEVICE] Відповідь сервера: {response_text}")
                    
                    error_data = response.json()
                    print(f"[DEVICE] ✗ Помилка відправки: {error_data.get('message', 'Невідома помилка')}")
                except Exception as parse_error:
                    print(f"[DEVICE] ✗ Помилка відправки: статус {response.status_code}")
                    if config.DEBUG:
                        print(f"[DEVICE] Помилка при розпарсюванні: {parse_error}")
                
                response.close()
                return False

        except Exception as e:
            print(f"[DEVICE] ✗ Виняток при відправці уведомлення: {e}")
            if config.DEBUG:
                import traceback
                traceback.print_exc()
            return False


# Глобальний екземпляр менеджера пристрою
device_manager = DeviceManager()
