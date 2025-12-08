"""
WiFi Manager Adapter (Infrastructure Layer)
Адаптер менеджера WiFi (Інфраструктурний шар)
"""
import time


class WiFiManager:
    """
    WiFi connection manager for ESP32
    Менеджер WiFi з'єднання для ESP32
    """

    def __init__(self, timeout=30):
        """
        Initialize WiFi manager

        Args:
            timeout: Connection timeout in seconds
        """
        self.timeout = timeout
        self.wlan = None
        self.is_initialized = False
        self._init_hardware()

    def _init_hardware(self):
        """
        Initialize WiFi hardware (ESP32 WLAN interface)
        Ініціалізувати WiFi обладнання (WLAN інтерфейс ESP32)
        """
        try:
            import network
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            self.is_initialized = True
            print("[INFO] WiFi hardware initialized")
        except ImportError:
            print("[WARNING] network module not available (running on non-ESP32 platform)")
            self.is_initialized = False

    def connect(self, ssid: str, password: str) -> bool:
        """
        Connect to WiFi network
        Підключитися до WiFi мережі

        Args:
            ssid: WiFi network name
            password: WiFi network password

        Returns:
            True if connected successfully, False otherwise
        """
        if not self.is_initialized:
            print("[ERROR] WiFi hardware not initialized")
            return False

        if self.wlan.isconnected():
            print("[INFO] Already connected to WiFi")
            return True

        print(f"[INFO] Connecting to WiFi: {ssid}")

        try:
            self.wlan.connect(ssid, password)

            # Wait for connection with timeout
            start_time = time.time()
            while not self.wlan.isconnected():
                if time.time() - start_time > self.timeout:
                    print(f"[ERROR] WiFi connection timeout after {self.timeout}s")
                    return False

                print(".", end="")
                time.sleep(1)

            print("\n[SUCCESS] WiFi connected")
            self._print_connection_info()
            return True

        except Exception as e:
            print(f"\n[ERROR] WiFi connection failed: {e}")
            return False

    def disconnect(self):
        """
        Disconnect from WiFi network
        Відключитися від WiFi мережі
        """
        if not self.is_initialized:
            return

        if self.wlan.isconnected():
            self.wlan.disconnect()
            print("[INFO] WiFi disconnected")

    def is_connected(self) -> bool:
        """
        Check if WiFi is connected
        Перевірити, чи підключено WiFi

        Returns:
            True if connected, False otherwise
        """
        if not self.is_initialized:
            return False

        return self.wlan.isconnected()

    def get_ip_address(self) -> str:
        """
        Get current IP address
        Отримати поточну IP адресу

        Returns:
            IP address as string, or None if not connected
        """
        if not self.is_initialized or not self.wlan.isconnected():
            return None

        ifconfig = self.wlan.ifconfig()
        return ifconfig[0] if ifconfig else None

    def get_rssi(self) -> int:
        """
        Get WiFi signal strength (RSSI)
        Отримати силу WiFi сигналу (RSSI)

        Returns:
            RSSI value in dBm, or None if not connected
        """
        if not self.is_initialized or not self.wlan.isconnected():
            return None

        try:
            # RSSI is typically negative (-30 to -90 dBm)
            # -30 dBm = excellent, -90 dBm = poor
            return self.wlan.status('rssi')
        except:
            return None

    def _print_connection_info(self):
        """
        Print WiFi connection information
        Вивести інформацію про WiFi з'єднання
        """
        if not self.is_initialized or not self.wlan.isconnected():
            return

        ifconfig = self.wlan.ifconfig()
        print(f"[INFO] IP Address: {ifconfig[0]}")
        print(f"[INFO] Subnet Mask: {ifconfig[1]}")
        print(f"[INFO] Gateway: {ifconfig[2]}")
        print(f"[INFO] DNS: {ifconfig[3]}")

        rssi = self.get_rssi()
        if rssi:
            print(f"[INFO] Signal Strength: {rssi} dBm")

    def scan_networks(self) -> list:
        """
        Scan for available WiFi networks
        Сканувати доступні WiFi мережі

        Returns:
            List of tuples (ssid, bssid, channel, rssi, authmode, hidden)
        """
        if not self.is_initialized:
            return []

        try:
            print("[INFO] Scanning WiFi networks...")
            networks = self.wlan.scan()
            print(f"[INFO] Found {len(networks)} networks")

            for net in networks:
                ssid = net[0].decode('utf-8') if isinstance(net[0], bytes) else net[0]
                rssi = net[3]
                print(f"  - {ssid}: {rssi} dBm")

            return networks

        except Exception as e:
            print(f"[ERROR] WiFi scan failed: {e}")
            return []

    def reconnect(self, ssid: str, password: str) -> bool:
        """
        Reconnect to WiFi if connection is lost
        Перепідключитися до WiFi якщо з'єднання втрачено

        Args:
            ssid: WiFi network name
            password: WiFi network password

        Returns:
            True if reconnected successfully, False otherwise
        """
        if self.is_connected():
            return True

        print("[INFO] WiFi connection lost, attempting to reconnect...")
        self.disconnect()
        time.sleep(2)
        return self.connect(ssid, password)

    def __repr__(self):
        status = "connected" if self.is_connected() else "disconnected"
        ip = self.get_ip_address() or "N/A"
        return f"WiFiManager(status={status}, ip={ip})"


class WiFiManagerMock:
    """
    Mock WiFi manager for testing on non-ESP32 platforms
    Макет WiFi менеджера для тестування на не-ESP32 платформах
    """

    def __init__(self):
        self.connected = False
        self.mock_ip = "192.168.1.100"

    def connect(self, ssid: str, password: str) -> bool:
        """Simulate WiFi connection"""
        print(f"[MOCK] Connecting to WiFi: {ssid}")
        time.sleep(2)
        self.connected = True
        print(f"[MOCK] WiFi connected, IP: {self.mock_ip}")
        return True

    def disconnect(self):
        """Simulate WiFi disconnection"""
        self.connected = False
        print("[MOCK] WiFi disconnected")

    def is_connected(self) -> bool:
        """Check mock connection status"""
        return self.connected

    def get_ip_address(self) -> str:
        """Return mock IP address"""
        return self.mock_ip if self.connected else None

    def get_rssi(self) -> int:
        """Return mock RSSI"""
        return -45 if self.connected else None

    def reconnect(self, ssid: str, password: str) -> bool:
        """Simulate reconnection"""
        return self.connect(ssid, password)
