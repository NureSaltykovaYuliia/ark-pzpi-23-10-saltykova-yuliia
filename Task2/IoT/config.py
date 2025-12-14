# config.py

# === API конфігурація ===
# Віддалений сервер MyDogSpace
API_BASE_URL = "http://35.192.164.131:8080/api"
API_AUTH_REGISTER = "/auth/register"
API_AUTH_LOGIN = "/auth/login"
API_SMART_DEVICES = "/smartdevices"
API_ALERTS = "/alerts"
API_NOTIFICATIONS = "/notifications"  # Эндпоинт для отправки уведомлений (без авторизации)

# === WiFi конфігурація ===
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# === Пристрій конфігурація ===
# Унікальний GUID пристрою
DEVICE_GUID = "ESP32-WOKWI-001"

# ID собаки
# ✅ НЕ ПОТРІБНО встановлювати вручну!
# Пристрій автоматично отримає Dog_ID з сервера після призначення собаки через API
# Призначення: POST /api/smartdevices/device/{deviceGuid}/assign
DOG_ID = None  # Автоматично отримується з сервера!

# === АВТОРИЗАЦІЯ НЕ ПОТРІБНА! ===
# Пристрій працює ПОВНІСТЮ АВТОНОМНО без реєстрації користувача!
# Всі endpoint'и для IoT пристроїв доступні без авторизації:
#   - POST /api/smartdevices/register-device
#   - GET /api/smartdevices/device/{deviceGuid}/dog
#   - PUT /api/smartdevices/device/{id}/telemetry

# === Налаштування сенсорів ===
# GPS симуляція
GPS_UPDATE_INTERVAL = 10  # секунд
DEFAULT_LATITUDE = 50.4501
DEFAULT_LONGITUDE = 30.5234

# === НОВЕ: Налаштування Гео-зон (Geofencing) ===
# Координати "Забороненої зони" (наприклад, дорога або чуже подвір'я)
DANGER_ZONE = {
    "lat": 50.4501,  # Центр зони (співпадає з дефолтним для тесту)
    "lon": 30.5234,
    "radius": 100    # Якщо собака ближче ніж 100м — тривога!
}

# Моніторинг батареї
BATTERY_CHECK_INTERVAL = 30  # секунд
BATTERY_LOW_THRESHOLD = 20   # %

# === Налаштування відправки даних ===
DATA_SEND_INTERVAL = 5  # Зменшив до 5 секунд, щоб ви швидше бачили результат у консолі!
SEND_INTERVAL = 5       # Дублюємо для сумісності з новим кодом

# === LED індикатори ===
LED_WIFI_PIN = 2    # Вбудований LED для WiFi статусу
LED_STATUS_PIN = 4  # LED для статусу підключення до API

# === Режим debug ===
DEBUG = True