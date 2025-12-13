import requests
import time
import uuid
import sys

class IoTDeviceSimulator:
    def __init__(self, api_url, device_guid=None):
        self.api_url = api_url.rstrip('/')
        self.device_guid = device_guid or str(uuid.uuid4())
        self.dog_id = None

    def register_device(self):
        """Регистрация устройства в базе данных"""
        print(f"[INFO] Регистрация устройства с GUID: {self.device_guid}")

        try:
            response = requests.post(
                f"{self.api_url}/api/smartdevices/register-device",
                json={"deviceGuid": self.device_guid},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] Устройство успешно зарегистрировано!")
                print(f"[INFO] ID устройства в БД: {data.get('id')}")
                return True
            else:
                print(f"[ERROR] Ошибка регистрации: {response.status_code}")
                print(f"[ERROR] {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] Ошибка при регистрации: {e}")
            return False

    def check_dog_assignment(self):
        """Проверка, назначена ли собака этому устройству"""
        try:
            response = requests.get(
                f"{self.api_url}/api/smartdevices/device/{self.device_guid}/dog"
            )

            if response.status_code == 200:
                data = response.json()
                return data.get('dogId')
            else:
                print(f"[ERROR] Ошибка проверки собаки: {response.status_code}")
                return None
        except Exception as e:
            print(f"[ERROR] Ошибка при проверке собаки: {e}")
            return None

    def wait_for_dog_assignment(self, check_interval=5):
        """Ожидание назначения собаки устройству"""
        print("[INFO] Сканирование сервера на наличие собаки...")

        while True:
            dog_id = self.check_dog_assignment()

            if dog_id is not None:
                self.dog_id = dog_id
                print(f"\n{'='*50}")
                print(f"[SUCCESS] Собака найдена!")
                print(f"[INFO] ID собаки: {dog_id}")
                print(f"{'='*50}\n")
                return dog_id
            else:
                print(f"[INFO] Собака ещё не назначена. Ожидание {check_interval} секунд...")
                time.sleep(check_interval)

    def run(self):
        """Основной цикл работы устройства"""
        print("="*50)
        print("IoT Device Simulator - MyDogSpace")
        print("="*50)

        # Шаг 1: Регистрация устройства
        if not self.register_device():
            print("[ERROR] Не удалось зарегистрировать устройство. Завершение работы.")
            return

        print()

        # Шаг 2: Ожидание назначения собаки
        self.wait_for_dog_assignment()

        # Устройство готово к работе
        print("[INFO] Устройство готово к работе!")
        print(f"[INFO] Устройство привязано к собаке с ID: {self.dog_id}")

def main():
    # Параметры подключения
    API_URL = "http://localhost:5104"  # Измените на ваш URL сервера

    # Можно указать свой GUID или он будет сгенерирован автоматически
    DEVICE_GUID = None  # Например: "DEVICE-ABC-123"

    if len(sys.argv) > 1:
        DEVICE_GUID = sys.argv[1]
        print(f"[INFO] Используется указанный GUID: {DEVICE_GUID}")

    if len(sys.argv) > 2:
        API_URL = sys.argv[2]
        print(f"[INFO] Используется указанный URL API: {API_URL}")

    # Создание и запуск симулятора
    simulator = IoTDeviceSimulator(API_URL, DEVICE_GUID)

    try:
        simulator.run()
    except KeyboardInterrupt:
        print("\n[INFO] Устройство остановлено пользователем.")
    except Exception as e:
        print(f"\n[ERROR] Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
