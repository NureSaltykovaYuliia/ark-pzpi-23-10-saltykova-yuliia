"""
Simplified version of Dog Tracker IoT Device for Wokwi
Спрощена версія IoT пристрою для Wokwi

This version has all code in a single file for easier deployment
Ця версія має весь код в одному файлі для легшого розгортання
"""
import time
import json

# Configuration
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""
API_BASE_URL = "http://192.168.1.100:5104/api"
DEVICE_GUID = "ESP32-DOG-TRACKER-001"

# GPS settings
GPS_START_LAT = 50.4501
GPS_START_LON = 30.5234
GPS_UPDATE_INTERVAL = 10

# Battery settings
BATTERY_INITIAL_LEVEL = 100.0
BATTERY_DRAIN_RATE = 0.1

# LED pins
LED_WIFI_PIN = 2
LED_GPS_PIN = 4
LED_BATTERY_PIN = 5
LED_API_PIN = 18

DEBUG_MODE = True


class SimpleDogTracker:
    """Simplified Dog Tracker implementation"""

    def __init__(self):
        print("\n" + "="*50)
        print("Dog Tracker IoT Device Starting (Simple Version)")
        print("="*50 + "\n")

        # State variables
        self.wifi_connected = False
        self.device_id = None
        self.current_lat = GPS_START_LAT
        self.current_lon = GPS_START_LON
        self.battery_level = BATTERY_INITIAL_LEVEL
        self.last_gps_update = 0
        self.movement_step = 0

        # Initialize hardware
        self._init_leds()
        self._init_wifi()

        print("[INIT] Initialization complete\n")

    def _init_leds(self):
        """Initialize LED pins"""
        try:
            from machine import Pin
            self.led_wifi = Pin(LED_WIFI_PIN, Pin.OUT)
            self.led_gps = Pin(LED_GPS_PIN, Pin.OUT)
            self.led_battery = Pin(LED_BATTERY_PIN, Pin.OUT)
            self.led_api = Pin(LED_API_PIN, Pin.OUT)

            # Startup sequence
            for led in [self.led_wifi, self.led_gps, self.led_battery, self.led_api]:
                led.value(1)
                time.sleep(0.2)
                led.value(0)

            print("[INFO] LED controller initialized")
        except ImportError:
            print("[WARNING] Running in simulation mode - LEDs not available")
            self.led_wifi = None

    def _init_wifi(self):
        """Initialize WiFi"""
        try:
            import network
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            print("[INFO] WiFi hardware initialized")
        except ImportError:
            print("[WARNING] network module not available")
            self.wlan = None

    def connect_wifi(self):
        """Connect to WiFi"""
        if not self.wlan:
            print("[INFO] WiFi not available (simulation mode)")
            return False

        print(f"[SETUP] Connecting to WiFi: {WIFI_SSID}...")

        if self.led_wifi:
            for _ in range(3):
                self.led_wifi.value(1)
                time.sleep(0.2)
                self.led_wifi.value(0)
                time.sleep(0.2)

        try:
            self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)

            # Wait for connection
            timeout = 30
            start = time.time()
            while not self.wlan.isconnected():
                if time.time() - start > timeout:
                    print("[ERROR] WiFi connection timeout")
                    return False
                print(".", end="")
                time.sleep(1)

            print("\n[SUCCESS] WiFi connected")
            if self.wlan.isconnected():
                print(f"[INFO] IP Address: {self.wlan.ifconfig()[0]}")

            if self.led_wifi:
                self.led_wifi.value(1)

            self.wifi_connected = True
            return True

        except Exception as e:
            print(f"\n[ERROR] WiFi connection failed: {e}")
            return False

    def update_gps(self):
        """Simulate GPS update"""
        import math

        # Simulate circular movement
        angle = (self.movement_step * math.pi / 4)
        self.current_lat += 0.0001 * math.cos(angle)
        self.current_lon += 0.0001 * math.sin(angle)
        self.movement_step = (self.movement_step + 1) % 8

        if self.led_gps:
            self.led_gps.value(1)

        if DEBUG_MODE:
            print(f"[GPS] Lat: {self.current_lat:.6f}, Lon: {self.current_lon:.6f}")

    def update_battery(self):
        """Simulate battery drain"""
        # Drain battery slightly
        elapsed_minutes = 0.5  # Assume 30 seconds between calls
        self.battery_level = max(0.0, self.battery_level - self.BATTERY_DRAIN_RATE * elapsed_minutes)

        # LED warning
        if self.battery_level < 20 and self.led_battery:
            self.led_battery.value(1)
            time.sleep(0.3)
            self.led_battery.value(0)

        if DEBUG_MODE:
            print(f"[BATTERY] Level: {self.battery_level:.1f}%")

    def send_data(self):
        """Send data to API (simulated)"""
        if not self.wifi_connected:
            print("[INFO] No WiFi - data buffered (simulated)")
            return

        if self.led_api:
            self.led_api.value(1)
            time.sleep(0.1)
            self.led_api.value(0)

        # In real implementation, this would make HTTP request
        payload = {
            'lastLatitude': self.current_lat,
            'lastLongitude': self.current_lon,
            'batteryLevel': self.battery_level
        }

        print(f"[API] Sending data: {payload}")

        # Simulate success
        if self.led_api:
            time.sleep(0.1)
            self.led_api.value(1)
            time.sleep(0.1)
            self.led_api.value(0)

        print("[SUCCESS] Data sent")

    def loop(self):
        """Main loop"""
        current_time = time.time()

        # Update GPS every 10 seconds
        if current_time - self.last_gps_update >= GPS_UPDATE_INTERVAL:
            self.update_gps()
            self.update_battery()
            self.send_data()
            self.last_gps_update = current_time

        time.sleep(1)

    def run(self):
        """Main run method"""
        # Setup
        self.connect_wifi()

        print("\n[INFO] Entering main loop...\n")
        print("Press Ctrl+C to stop\n")

        # Main loop
        loop_count = 0
        try:
            while True:
                self.loop()
                loop_count += 1

                # Status every 30 seconds
                if loop_count % 30 == 0:
                    print(f"\n[STATUS] Running for {loop_count} seconds")
                    print(f"  WiFi: {'Connected' if self.wifi_connected else 'Disconnected'}")
                    print(f"  GPS: {self.current_lat:.6f}, {self.current_lon:.6f}")
                    print(f"  Battery: {self.battery_level:.1f}%\n")

        except KeyboardInterrupt:
            print("\n\n[INFO] Shutting down...")
            if self.led_wifi:
                for led in [self.led_wifi, self.led_gps, self.led_battery, self.led_api]:
                    led.value(0)
            print("[INFO] Shutdown complete")


def main():
    """Main entry point"""
    tracker = SimpleDogTracker()
    tracker.run()


if __name__ == '__main__':
    main()
