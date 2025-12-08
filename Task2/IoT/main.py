"""
Main application for ESP32 Dog Tracker IoT Device
Головна програма для IoT пристрою ESP32 Dog Tracker

Clean Architecture Implementation:
- Domain Layer: core/entities.py, core/use_cases.py
- Application Layer: services/
- Infrastructure Layer: adapters/
- Presentation Layer: main.py (this file)
"""
import time
import config

# Core layer
from core.entities import DeviceStatus, DataRecord
from core.use_cases import (
    DataCollectionUseCase,
    DataTransmissionUseCase,
    DeviceRegistrationUseCase,
    WiFiConnectionUseCase,
    BatteryMonitoringUseCase
)

# Infrastructure layer (adapters)
from adapters.gps_sensor import GPSSensor
from adapters.battery_monitor import BatteryMonitor
from adapters.wifi_manager import WiFiManager
from adapters.api_client import APIClient

# Application layer (services)
from services.data_buffer import DataBuffer
from services.led_controller import LEDController


class DogTrackerDevice:
    """
    Main IoT Device Application
    Головна програма IoT пристрою
    """

    def __init__(self):
        """Initialize device and all components"""
        print("\n" + "="*50)
        print("Dog Tracker IoT Device Starting...")
        print("="*50 + "\n")

        # Initialize device status
        self.device_status = DeviceStatus(
            device_guid=config.DEVICE_GUID,
            device_id=config.DEVICE_ID
        )

        # Initialize infrastructure adapters
        self.led_controller = LEDController(
            wifi_pin=config.LED_WIFI_PIN,
            gps_pin=config.LED_GPS_PIN,
            battery_pin=config.LED_BATTERY_PIN,
            api_pin=config.LED_API_PIN
        )

        self.led_controller.startup_sequence()

        self.gps_sensor = GPSSensor(
            simulation_enabled=config.GPS_SIMULATION_ENABLED,
            start_lat=config.GPS_START_LAT,
            start_lon=config.GPS_START_LON,
            movement_speed=config.GPS_MOVEMENT_SPEED
        )

        self.battery_monitor = BatteryMonitor(
            simulation_enabled=config.BATTERY_SIMULATION_ENABLED,
            initial_level=config.BATTERY_INITIAL_LEVEL,
            drain_rate=config.BATTERY_DRAIN_RATE
        )

        self.wifi_manager = WiFiManager(timeout=30)

        self.api_client = APIClient(
            base_url=config.API_BASE_URL,
            timeout=10
        )

        # Initialize application services
        self.data_buffer = DataBuffer(max_size=config.MAX_BUFFER_SIZE)

        # Initialize use cases
        self.data_collection_uc = DataCollectionUseCase(
            self.gps_sensor,
            self.battery_monitor
        )

        self.data_transmission_uc = DataTransmissionUseCase(
            self.api_client,
            self.data_buffer,
            self.led_controller
        )

        self.device_registration_uc = DeviceRegistrationUseCase(
            self.api_client,
            self.led_controller
        )

        self.wifi_connection_uc = WiFiConnectionUseCase(
            self.wifi_manager,
            self.led_controller
        )

        self.battery_monitoring_uc = BatteryMonitoringUseCase(
            self.battery_monitor,
            self.led_controller
        )

        # Timing variables
        self.last_gps_update = 0
        self.last_battery_update = 0
        self.last_send_attempt = 0

        print("[INIT] Device initialization complete\n")

    def setup(self):
        """
        Setup phase: Connect WiFi and register device
        Фаза налаштування: підключення до WiFi та реєстрація пристрою
        """
        print("\n[SETUP] Starting setup phase...\n")

        # Connect to WiFi
        print("[SETUP] Connecting to WiFi...")
        wifi_connected = self.wifi_connection_uc.connect_wifi(
            config.WIFI_SSID,
            config.WIFI_PASSWORD
        )

        if not wifi_connected:
            print("[ERROR] Failed to connect to WiFi")
            self.led_controller.error_pattern()
            return False

        self.device_status.wifi_connected = True

        # Get authentication token (if required)
        # For now, we assume device can access API without user login
        # In production, you might need device-specific credentials

        # Register device (if not already registered)
        if not self.device_status.device_id:
            print("[SETUP] Registering device with API...")
            # TODO: Get DOG_ID from configuration or user input
            # For now, using a placeholder dog_id
            dog_id = 1  # This should be configured or obtained somehow

            device_id = self.device_registration_uc.register_device(
                config.DEVICE_GUID,
                dog_id
            )

            if device_id:
                self.device_status.device_id = device_id
                config.DEVICE_ID = device_id
                print(f"[SUCCESS] Device registered with ID: {device_id}")
            else:
                print("[WARNING] Failed to register device, will retry later")

        self.led_controller.success_pattern()
        print("\n[SETUP] Setup complete!\n")
        return True

    def loop(self):
        """
        Main loop: Collect, buffer, and transmit data
        Головний цикл: збирати, буферизувати та передавати дані
        """
        current_time = time.time()

        # Update GPS data periodically
        if current_time - self.last_gps_update >= config.GPS_UPDATE_INTERVAL:
            self._update_gps()
            self.last_gps_update = current_time

        # Update battery data periodically
        if current_time - self.last_battery_update >= config.BATTERY_UPDATE_INTERVAL:
            self._update_battery()
            self.last_battery_update = current_time

        # Send data periodically
        if current_time - self.last_send_attempt >= config.SEND_INTERVAL:
            self._send_data()
            self.last_send_attempt = current_time

        # Check WiFi connection
        self._check_wifi_connection()

        # Small delay to prevent busy loop
        time.sleep(1)

    def _update_gps(self):
        """Update GPS data"""
        self.led_controller.gps_acquiring()
        gps_data = self.gps_sensor.read()
        self.device_status.update_gps(gps_data)
        self.led_controller.gps_active()

        if config.DEBUG_MODE:
            print(f"[GPS] {gps_data}")

    def _update_battery(self):
        """Update battery data"""
        battery_data = self.battery_monitoring_uc.check_battery_status()
        self.device_status.update_battery(battery_data)

        if config.DEBUG_MODE:
            print(f"[BATTERY] {battery_data}")

    def _send_data(self):
        """Collect and send data to API"""
        # Collect current sensor data
        record = self.data_collection_uc.collect_data()

        # Validate data
        if not self.data_collection_uc.is_data_valid(record):
            print("[ERROR] Invalid sensor data, skipping...")
            return

        # Add to buffer
        self.data_buffer.add(record)

        # Check if we have WiFi and device is registered
        if not self.device_status.wifi_connected:
            print("[INFO] No WiFi connection, data buffered")
            return

        if not self.device_status.device_id:
            print("[INFO] Device not registered, data buffered")
            return

        # Send buffered data
        sent_count = self.data_transmission_uc.send_buffered_data(
            self.device_status.device_id
        )

        if sent_count > 0:
            print(f"[SUCCESS] Sent {sent_count} record(s)")
            self.device_status.api_available = True
        else:
            print(f"[INFO] No records sent (buffer: {self.data_buffer.get_unsent_count()})")

    def _check_wifi_connection(self):
        """Check and maintain WiFi connection"""
        was_connected = self.device_status.wifi_connected
        is_connected = self.wifi_connection_uc.check_connection()

        if was_connected and not is_connected:
            print("[WARNING] WiFi connection lost, attempting reconnect...")
            self.wifi_connection_uc.connect_wifi(
                config.WIFI_SSID,
                config.WIFI_PASSWORD
            )

        self.device_status.wifi_connected = is_connected

    def print_status(self):
        """Print device status"""
        print("\n" + "="*50)
        print("DEVICE STATUS")
        print("="*50)
        print(f"Device GUID: {self.device_status.device_guid}")
        print(f"Device ID: {self.device_status.device_id or 'Not registered'}")
        print(f"WiFi: {'Connected' if self.device_status.wifi_connected else 'Disconnected'}")
        print(f"GPS: {'Active' if self.device_status.gps_active else 'Inactive'}")
        print(f"API: {'Available' if self.device_status.api_available else 'Unavailable'}")

        if self.device_status.gps_data:
            print(f"\nGPS: {self.device_status.gps_data}")

        if self.device_status.battery_data:
            print(f"Battery: {self.device_status.battery_data}")

        self.data_buffer.print_statistics()
        print("="*50 + "\n")

    def run(self):
        """Main run method"""
        # Setup phase
        if not self.setup():
            print("[ERROR] Setup failed, entering offline mode")
            # Continue in offline mode (buffer data only)

        # Main loop
        print("\n[INFO] Entering main loop...\n")
        loop_count = 0

        try:
            while True:
                self.loop()
                loop_count += 1

                # Print status every 30 iterations
                if loop_count % 30 == 0:
                    self.print_status()

        except KeyboardInterrupt:
            print("\n\n[INFO] Shutting down...")
            self.shutdown()

    def shutdown(self):
        """Cleanup before shutdown"""
        print("[INFO] Performing cleanup...")
        self.print_status()
        self.led_controller.all_off()
        self.wifi_manager.disconnect()
        print("[INFO] Shutdown complete")


def main():
    """Main entry point"""
    # Create and run device
    device = DogTrackerDevice()
    device.run()


if __name__ == '__main__':
    main()
