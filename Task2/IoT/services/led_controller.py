"""
LED Controller Service (Application Layer)
Сервіс контролера LED (Прикладний шар)
"""
import time


class LEDController:
    """
    Controller for status LEDs
    Контролер для статусних LED
    """

    def __init__(self, wifi_pin=2, gps_pin=4, battery_pin=5, api_pin=18):
        """
        Initialize LED controller

        Args:
            wifi_pin: GPIO pin for WiFi status LED (blue)
            gps_pin: GPIO pin for GPS status LED (green)
            battery_pin: GPIO pin for battery warning LED (yellow)
            api_pin: GPIO pin for API communication LED (red)
        """
        self.wifi_pin = wifi_pin
        self.gps_pin = gps_pin
        self.battery_pin = battery_pin
        self.api_pin = api_pin

        self.leds = {}
        self._init_hardware()

    def _init_hardware(self):
        """
        Initialize LED GPIO pins
        Ініціалізувати GPIO піни для LED
        """
        try:
            from machine import Pin
            self.leds = {
                'wifi': Pin(self.wifi_pin, Pin.OUT),
                'gps': Pin(self.gps_pin, Pin.OUT),
                'battery': Pin(self.battery_pin, Pin.OUT),
                'api': Pin(self.api_pin, Pin.OUT)
            }
            # Turn off all LEDs initially
            self.all_off()
            print("[INFO] LED controller initialized")
        except ImportError:
            print("[WARNING] machine module not available, LED control disabled")

    def _set_led(self, led_name: str, state: bool):
        """
        Set LED state
        Встановити стан LED

        Args:
            led_name: Name of LED (wifi, gps, battery, api)
            state: True for ON, False for OFF
        """
        if led_name in self.leds:
            self.leds[led_name].value(1 if state else 0)

    def _blink_led(self, led_name: str, times=1, delay=0.1):
        """
        Blink LED
        Блимнути LED

        Args:
            led_name: Name of LED
            times: Number of blinks
            delay: Delay between blinks in seconds
        """
        for _ in range(times):
            self._set_led(led_name, True)
            time.sleep(delay)
            self._set_led(led_name, False)
            time.sleep(delay)

    # WiFi Status LEDs
    def wifi_connected(self):
        """WiFi connected - blue LED solid ON"""
        self._set_led('wifi', True)

    def wifi_disconnected(self):
        """WiFi disconnected - blue LED OFF"""
        self._set_led('wifi', False)

    def wifi_connecting(self):
        """WiFi connecting - blue LED blinking"""
        self._blink_led('wifi', times=3, delay=0.2)

    # GPS Status LEDs
    def gps_active(self):
        """GPS active - green LED solid ON"""
        self._set_led('gps', True)

    def gps_inactive(self):
        """GPS inactive - green LED OFF"""
        self._set_led('gps', False)

    def gps_acquiring(self):
        """GPS acquiring fix - green LED blinking"""
        self._blink_led('gps', times=2, delay=0.3)

    # Battery Status LEDs
    def battery_normal(self):
        """Battery normal - yellow LED OFF"""
        self._set_led('battery', False)

    def battery_low(self):
        """Battery low (<20%) - yellow LED slow blink"""
        self._set_led('battery', True)
        time.sleep(0.5)
        self._set_led('battery', False)

    def battery_critical(self):
        """Battery critical (<10%) - yellow LED rapid blink"""
        self._blink_led('battery', times=5, delay=0.1)

    # API Communication LEDs
    def blink_api_led(self):
        """API request in progress - red LED quick blink"""
        self._blink_led('api', times=1, delay=0.1)

    def api_success(self):
        """API request successful - red LED quick double blink"""
        self._blink_led('api', times=2, delay=0.1)

    def api_error(self):
        """API request failed - red LED long blink"""
        self._set_led('api', True)
        time.sleep(0.5)
        self._set_led('api', False)

    # Combined Status Patterns
    def startup_sequence(self):
        """
        Startup LED sequence
        Послідовність LED при запуску
        """
        print("[LED] Startup sequence")
        leds_order = ['wifi', 'gps', 'battery', 'api']

        for led in leds_order:
            self._set_led(led, True)
            time.sleep(0.2)

        time.sleep(0.3)

        for led in reversed(leds_order):
            self._set_led(led, False)
            time.sleep(0.2)

    def error_pattern(self):
        """
        Error LED pattern - all LEDs blink
        Патерн помилки - всі LED блимають
        """
        print("[LED] Error pattern")
        for _ in range(3):
            self.all_on()
            time.sleep(0.2)
            self.all_off()
            time.sleep(0.2)

    def success_pattern(self):
        """
        Success LED pattern
        Патерн успіху
        """
        print("[LED] Success pattern")
        self.all_on()
        time.sleep(0.5)
        self.all_off()

    def all_on(self):
        """Turn all LEDs ON"""
        for led_name in self.leds:
            self._set_led(led_name, True)

    def all_off(self):
        """Turn all LEDs OFF"""
        for led_name in self.leds:
            self._set_led(led_name, False)

    def test_pattern(self):
        """
        Test all LEDs sequentially
        Протестувати всі LED послідовно
        """
        print("[LED] Testing all LEDs...")
        led_names = ['wifi', 'gps', 'battery', 'api']
        colors = ['Blue (WiFi)', 'Green (GPS)', 'Yellow (Battery)', 'Red (API)']

        for led, color in zip(led_names, colors):
            print(f"  Testing {color}")
            self._set_led(led, True)
            time.sleep(1)
            self._set_led(led, False)
            time.sleep(0.3)

        print("[LED] Test complete")

    def __repr__(self):
        return (f"LEDController(wifi={self.wifi_pin}, gps={self.gps_pin}, "
                f"battery={self.battery_pin}, api={self.api_pin})")


class LEDControllerMock:
    """
    Mock LED controller for testing without hardware
    Макет LED контролера для тестування без обладнання
    """

    def __init__(self):
        self.states = {
            'wifi': False,
            'gps': False,
            'battery': False,
            'api': False
        }

    def _set_led(self, led_name: str, state: bool):
        """Mock LED state change"""
        self.states[led_name] = state
        state_str = "ON" if state else "OFF"
        print(f"[MOCK LED] {led_name.upper()}: {state_str}")

    def wifi_connected(self):
        self._set_led('wifi', True)

    def wifi_disconnected(self):
        self._set_led('wifi', False)

    def wifi_connecting(self):
        print("[MOCK LED] WiFi: BLINKING")

    def gps_active(self):
        self._set_led('gps', True)

    def gps_inactive(self):
        self._set_led('gps', False)

    def battery_normal(self):
        self._set_led('battery', False)

    def battery_low(self):
        print("[MOCK LED] Battery: LOW (BLINKING)")

    def battery_critical(self):
        print("[MOCK LED] Battery: CRITICAL (RAPID BLINK)")

    def blink_api_led(self):
        print("[MOCK LED] API: BLINK")

    def api_success(self):
        print("[MOCK LED] API: SUCCESS")

    def api_error(self):
        print("[MOCK LED] API: ERROR")

    def startup_sequence(self):
        print("[MOCK LED] Startup sequence")

    def all_off(self):
        for led in self.states:
            self._set_led(led, False)
