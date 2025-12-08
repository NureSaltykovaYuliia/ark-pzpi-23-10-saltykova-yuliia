"""
Domain Entities for IoT Device
Доменні сутності для IoT пристрою
"""
import time


class GPSData:
    """
    Entity representing GPS coordinates
    Сутність для представлення GPS координат
    """
    def __init__(self, latitude: float, longitude: float, timestamp: int = None):
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp or time.time()

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp
        }

    def __repr__(self):
        return f"GPSData(lat={self.latitude:.6f}, lon={self.longitude:.6f})"


class BatteryData:
    """
    Entity representing battery status
    Сутність для представлення стану батареї
    """
    def __init__(self, level: float, timestamp: int = None):
        self.level = max(0.0, min(100.0, level))  # Clamp between 0-100
        self.timestamp = timestamp or time.time()
        self.is_low = self.level < 20.0
        self.is_critical = self.level < 10.0

    def to_dict(self):
        return {
            'level': self.level,
            'timestamp': self.timestamp,
            'is_low': self.is_low,
            'is_critical': self.is_critical
        }

    def __repr__(self):
        return f"BatteryData(level={self.level:.1f}%)"


class DeviceStatus:
    """
    Entity representing overall device status
    Сутність для представлення загального стану пристрою
    """
    def __init__(self, device_guid: str, device_id: int = None):
        self.device_guid = device_guid
        self.device_id = device_id
        self.wifi_connected = False
        self.gps_active = False
        self.api_available = False
        self.last_update_time = None
        self.gps_data = None
        self.battery_data = None

    def update_gps(self, gps_data: GPSData):
        """Update GPS data"""
        self.gps_data = gps_data
        self.gps_active = True

    def update_battery(self, battery_data: BatteryData):
        """Update battery data"""
        self.battery_data = battery_data

    def to_api_payload(self):
        """
        Convert device status to API payload format
        Перетворити статус пристрою в формат для API
        """
        if not self.gps_data or not self.battery_data:
            return None

        return {
            'lastLatitude': self.gps_data.latitude,
            'lastLongitude': self.gps_data.longitude,
            'batteryLevel': self.battery_data.level
        }

    def __repr__(self):
        return (f"DeviceStatus(guid={self.device_guid}, "
                f"wifi={self.wifi_connected}, gps={self.gps_active}, "
                f"api={self.api_available})")


class DataRecord:
    """
    Entity representing a single data record for buffering
    Сутність для представлення одного запису даних для буферизації
    """
    def __init__(self, gps_data: GPSData, battery_data: BatteryData):
        self.gps_data = gps_data
        self.battery_data = battery_data
        self.timestamp = time.time()
        self.attempts = 0
        self.sent = False

    def to_api_payload(self):
        """Convert to API payload format"""
        return {
            'lastLatitude': self.gps_data.latitude,
            'lastLongitude': self.gps_data.longitude,
            'batteryLevel': self.battery_data.level
        }

    def mark_sent(self):
        """Mark record as successfully sent"""
        self.sent = True

    def increment_attempts(self):
        """Increment send attempts counter"""
        self.attempts += 1

    def __repr__(self):
        return (f"DataRecord(gps={self.gps_data}, battery={self.battery_data}, "
                f"attempts={self.attempts}, sent={self.sent})")
