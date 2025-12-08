"""
Use Cases (Business Logic) for IoT Device
Бізнес-логіка для IoT пристрою
"""
from core.entities import DeviceStatus, DataRecord, GPSData, BatteryData


class DataCollectionUseCase:
    """
    Use case for collecting sensor data
    Сценарій збору даних з сенсорів
    """
    def __init__(self, gps_sensor, battery_monitor):
        self.gps_sensor = gps_sensor
        self.battery_monitor = battery_monitor

    def collect_data(self) -> DataRecord:
        """
        Collect GPS and battery data
        Зібрати дані GPS і батареї
        """
        gps_data = self.gps_sensor.read()
        battery_data = self.battery_monitor.read()
        return DataRecord(gps_data, battery_data)

    def is_data_valid(self, record: DataRecord) -> bool:
        """
        Validate collected data
        Перевірити коректність зібраних даних
        """
        if not record.gps_data or not record.battery_data:
            return False

        # Check GPS coordinates are valid
        if not (-90 <= record.gps_data.latitude <= 90):
            return False
        if not (-180 <= record.gps_data.longitude <= 180):
            return False

        # Check battery level is valid
        if not (0 <= record.battery_data.level <= 100):
            return False

        return True


class DataTransmissionUseCase:
    """
    Use case for transmitting data to API
    Сценарій передачі даних на API
    """
    def __init__(self, api_client, data_buffer, led_controller):
        self.api_client = api_client
        self.data_buffer = data_buffer
        self.led_controller = led_controller

    def send_data(self, device_id: int, record: DataRecord) -> bool:
        """
        Send single data record to API
        Відправити один запис даних на API
        """
        try:
            self.led_controller.blink_api_led()
            payload = record.to_api_payload()
            success = self.api_client.update_device(device_id, payload)

            if success:
                record.mark_sent()
                self.led_controller.api_success()
                print(f"[SUCCESS] Data sent: {record}")
                return True
            else:
                record.increment_attempts()
                self.led_controller.api_error()
                print(f"[ERROR] Failed to send data: {record}")
                return False

        except Exception as e:
            record.increment_attempts()
            self.led_controller.api_error()
            print(f"[EXCEPTION] Error sending data: {e}")
            return False

    def send_buffered_data(self, device_id: int) -> int:
        """
        Send all buffered data records
        Відправити всі буферизовані записи даних
        """
        sent_count = 0
        records = self.data_buffer.get_unsent_records()

        for record in records:
            if self.send_data(device_id, record):
                sent_count += 1
            else:
                break  # Stop on first failure to preserve order

        # Clean up sent records
        self.data_buffer.remove_sent_records()
        return sent_count


class DeviceRegistrationUseCase:
    """
    Use case for device registration with API
    Сценарій реєстрації пристрою на API
    """
    def __init__(self, api_client, led_controller):
        self.api_client = api_client
        self.led_controller = led_controller

    def register_device(self, device_guid: str, dog_id: int) -> int:
        """
        Register device with API and return device ID
        Зареєструвати пристрій на API і повернути ID пристрою
        """
        try:
            self.led_controller.blink_api_led()
            device_id = self.api_client.register_device(device_guid, dog_id)

            if device_id:
                self.led_controller.api_success()
                print(f"[SUCCESS] Device registered with ID: {device_id}")
                return device_id
            else:
                self.led_controller.api_error()
                print(f"[ERROR] Failed to register device")
                return None

        except Exception as e:
            self.led_controller.api_error()
            print(f"[EXCEPTION] Error registering device: {e}")
            return None


class WiFiConnectionUseCase:
    """
    Use case for WiFi connection management
    Сценарій управління WiFi з'єднанням
    """
    def __init__(self, wifi_manager, led_controller):
        self.wifi_manager = wifi_manager
        self.led_controller = led_controller

    def connect_wifi(self, ssid: str, password: str) -> bool:
        """
        Connect to WiFi network
        Підключитися до WiFi мережі
        """
        try:
            self.led_controller.wifi_connecting()
            success = self.wifi_manager.connect(ssid, password)

            if success:
                self.led_controller.wifi_connected()
                print(f"[SUCCESS] Connected to WiFi: {ssid}")
                return True
            else:
                self.led_controller.wifi_disconnected()
                print(f"[ERROR] Failed to connect to WiFi: {ssid}")
                return False

        except Exception as e:
            self.led_controller.wifi_disconnected()
            print(f"[EXCEPTION] WiFi connection error: {e}")
            return False

    def check_connection(self) -> bool:
        """
        Check if WiFi is still connected
        Перевірити, чи є з'єднання з WiFi
        """
        is_connected = self.wifi_manager.is_connected()

        if is_connected:
            self.led_controller.wifi_connected()
        else:
            self.led_controller.wifi_disconnected()

        return is_connected


class BatteryMonitoringUseCase:
    """
    Use case for battery monitoring and alerts
    Сценарій моніторингу батареї та сповіщень
    """
    def __init__(self, battery_monitor, led_controller):
        self.battery_monitor = battery_monitor
        self.led_controller = led_controller

    def check_battery_status(self) -> BatteryData:
        """
        Check battery status and trigger alerts if needed
        Перевірити стан батареї та викликати сповіщення при необхідності
        """
        battery_data = self.battery_monitor.read()

        if battery_data.is_critical:
            self.led_controller.battery_critical()
            print(f"[CRITICAL] Battery level critical: {battery_data.level:.1f}%")
        elif battery_data.is_low:
            self.led_controller.battery_low()
            print(f"[WARNING] Battery level low: {battery_data.level:.1f}%")
        else:
            self.led_controller.battery_normal()

        return battery_data
