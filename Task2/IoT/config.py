"""
Configuration file for ESP32 IoT Device
Конфігураційний файл для IoT пристрою ESP32
"""

# WiFi Configuration
WIFI_SSID = "Wokwi-GUEST"  # Default Wokwi WiFi
WIFI_PASSWORD = ""

# API Configuration
API_BASE_URL = "http://192.168.1.100:5104/api"  # Change to your API server IP
API_SMARTDEVICES_ENDPOINT = "/smartdevices"

# Device Configuration
DEVICE_GUID = "ESP32-DOG-TRACKER-001"  # Unique device identifier
DEVICE_ID = None  # Will be set after registration

# GPS Simulation Configuration
GPS_UPDATE_INTERVAL = 10  # seconds
GPS_SIMULATION_ENABLED = True
GPS_START_LAT = 50.4501  # Kyiv coordinates
GPS_START_LON = 30.5234
GPS_MOVEMENT_SPEED = 0.0001  # degrees per update (simulated movement)

# Battery Configuration
BATTERY_UPDATE_INTERVAL = 30  # seconds
BATTERY_SIMULATION_ENABLED = True
BATTERY_INITIAL_LEVEL = 100.0
BATTERY_DRAIN_RATE = 0.1  # percent per minute

# Data Buffering Configuration
MAX_BUFFER_SIZE = 50  # Maximum number of records to buffer
SEND_INTERVAL = 15  # seconds between send attempts

# LED Pins Configuration
LED_WIFI_PIN = 2      # Blue LED - WiFi status
LED_GPS_PIN = 4       # Green LED - GPS status
LED_BATTERY_PIN = 5   # Yellow LED - Battery warning (<20%)
LED_API_PIN = 18      # Red LED - API communication

# Button Configuration
BUTTON_MANUAL_SEND_PIN = 15  # Button for manual data send

# Debug Configuration
DEBUG_MODE = True
SERIAL_BAUD_RATE = 115200
