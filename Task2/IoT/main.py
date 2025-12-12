"""
Головний файл IoT пристрою MyDogSpace для ESP32
Виконує підключення до WiFi, авторизацію та відправку телеметрії
"""

import network
import time
from machine import Pin
import config
from auth import auth_manager
from device_manager import device_manager
from gps_sensor import gps_sensor
from battery_monitor import battery_monitor
from geofence_monitor import geofence_monitor


# LED індикатори
led_wifi = Pin(config.LED_WIFI_PIN, Pin.OUT)
led_status = Pin(config.LED_STATUS_PIN, Pin.OUT)


def connect_wifi():
    """
    Підключення до WiFi мережі

    Returns:
        bool: True якщо підключення успішне
    """
    print("\n" + "="*50)
    print("MyDogSpace IoT Device - ESP32")
    print("="*50)
    print("\n[WiFi] Підключення до WiFi...")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

        # Очікування підключення
        max_wait = 10
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print(f"[WiFi] Очікування... ({max_wait})")
            led_wifi.value(not led_wifi.value())  # Мигання LED
            time.sleep(1)

    if wlan.isconnected():
        led_wifi.value(1)  # Увімкнути LED
        print(f"[WiFi] ✓ Підключено!")
        print(f"[WiFi] IP адреса: {wlan.ifconfig()[0]}")
        return True
    else:
        led_wifi.value(0)
        print("[WiFi] ✗ Помилка підключення")
        return False


def initialize_device():
    """
    Ініціалізація пристрою:
    - Реєстрація користувача (якщо потрібно)
    - Авторизація
    - Реєстрація пристрою

    Returns:
        bool: True якщо ініціалізація успішна
    """
    print("\n" + "="*50)
    print("Ініціалізація пристрою")
    print("="*50 + "\n")

    # Спроба авторизації
    print("[INIT] Спроба входу...")
    if auth_manager.login(config.TEST_USER["email"], config.TEST_USER["password"]):
        led_status.value(1)
    else:
        print("[INIT] Вхід не вдався, спроба реєстрації...")

        # Якщо не вдалось увійти - реєструємо нового користувача
        if auth_manager.register(
            config.TEST_USER["username"],
            config.TEST_USER["email"],
            config.TEST_USER["password"]
        ):
            print("[INIT] Користувач зареєстровано, вхід...")
            time.sleep(1)

            # Повторна спроба входу
            if auth_manager.login(config.TEST_USER["email"], config.TEST_USER["password"]):
                led_status.value(1)
            else:
                print("[INIT] ✗ Не вдалося увійти після реєстрації")
                led_status.value(0)
                return False
        else:
            print("[INIT] ✗ Помилка реєстрації")
            led_status.value(0)
            return False

    # Реєстрація пристрою
    # ВАЖЛИВО: Для реєстрації пристрою потрібен ID собаки
    # У реальному сценарії це значення повинно бути налаштоване
    if config.DOG_ID is None:
        print("[INIT] ⚠ УВАГА: DOG_ID не встановлено в config.py")
        print("[INIT] Пристрій не буде зареєстровано на сервері")
        print("[INIT] Буде працювати тільки збір локальних даних")
        return True

    print(f"[INIT] Реєстрація пристрою для собаки ID: {config.DOG_ID}")
    if device_manager.register_device(config.DOG_ID):
        print("[INIT] ✓ Пристрій успішно зареєстровано")
        return True
    else:
        print("[INIT] ✗ Помилка реєстрації пристрою")
        return False


def main_loop():
    """
    Головний цикл роботи пристрою
    Періодично відправляє телеметрію на сервер
    """
    print("\n" + "="*50)
    print("Запуск головного циклу")
    print("="*50 + "\n")

    iteration = 0

    while True:
        try:
            iteration += 1
            print(f"\n--- Ітерація #{iteration} ---")

            # Мигання статусним LED
            led_status.value(not led_status.value())

            # Читання даних з сенсорів
            latitude, longitude = gps_sensor.read_coordinates()
            battery = battery_monitor.read_battery_level()

            print(f"GPS: {latitude:.6f}, {longitude:.6f}")
            print(f"Battery: {battery:.1f}%")

            # Перевірка геозони
            is_safe, distance = geofence_monitor.check_position(latitude, longitude)

            # Якщо собака в небезпечній зоні - відправляємо сповіщення
            if not is_safe and config.DOG_ID is not None:
                if not geofence_monitor.last_alert_sent:
                    print("⚠ УВАГА: Собака вийшла за межі безпечної зони!")
                    if geofence_monitor.send_danger_alert(latitude, longitude, distance, config.DOG_ID):
                        print("✓ Сповіщення про небезпеку відправлено")
                    else:
                        print("✗ Не вдалося відправити сповіщення")
            elif is_safe:
                # Скидаємо флаг коли собака повернулась в безпечну зону
                if geofence_monitor.last_alert_sent:
                    print("✓ Собака повернулась в безпечну зону")
                    geofence_monitor.last_alert_sent = False

            # Якщо пристрій зареєстровано - відправляємо телеметрію
            if device_manager.is_registered:
                print("Відправка телеметрії на сервер...")
                if device_manager.send_telemetry():
                    led_status.value(1)
                else:
                    print("Помилка відправки телеметрії")
                    led_status.value(0)
            else:
                print("Пристрій не зареєстровано - тільки локальний збір даних")

            # Перевірка низького заряду
            if battery_monitor.is_low_battery():
                print("⚠ УВАГА: Низький заряд батареї!")
                # Тут можна додати сповіщення на сервер

            # Очікування до наступної ітерації
            print(f"Очікування {config.DATA_SEND_INTERVAL} секунд...")
            time.sleep(config.DATA_SEND_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n[MAIN] Отримано сигнал зупинки")
            break
        except Exception as e:
            print(f"\n[MAIN] ✗ Помилка в головному циклі: {e}")
            time.sleep(5)  # Очікування перед повторною спробою


def main():
    """Головна функція запуску"""
    try:
        # Вимкнути LED на початку
        led_wifi.value(0)
        led_status.value(0)

        # Підключення до WiFi
        if not connect_wifi():
            print("[MAIN] ✗ Не вдалося підключитися до WiFi")
            return

        # Ініціалізація пристрою
        if initialize_device():
            print("\n[MAIN] ✓ Ініціалізація завершена успішно")
        else:
            print("\n[MAIN] ⚠ Ініціалізація завершена з помилками")

        # Невелика затримка перед початком головного циклу
        time.sleep(2)

        # Запуск головного циклу
        main_loop()

    except Exception as e:
        print(f"\n[MAIN] ✗ Критична помилка: {e}")
        led_wifi.value(0)
        led_status.value(0)

    finally:
        print("\n" + "="*50)
        print("Пристрій зупинено")
        print("="*50)


# Запуск програми
if __name__ == "__main__":
    main()
