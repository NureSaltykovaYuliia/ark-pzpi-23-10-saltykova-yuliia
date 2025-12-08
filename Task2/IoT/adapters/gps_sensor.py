"""
GPS Sensor Adapter (Infrastructure Layer)
Адаптер GPS сенсора (Інфраструктурний шар)
"""
import time
import math
from core.entities import GPSData


class GPSSensor:
    """
    GPS Sensor adapter for reading location data
    Адаптер GPS сенсора для читання даних про місцезнаходження

    In real hardware, this would interface with a GPS module (e.g., NEO-6M)
    На реальному обладнанні це працювало б з GPS модулем (наприклад, NEO-6M)
    """

    def __init__(self, simulation_enabled=True, start_lat=50.4501, start_lon=30.5234,
                 movement_speed=0.0001):
        """
        Initialize GPS sensor

        Args:
            simulation_enabled: Whether to use simulated GPS data
            start_lat: Starting latitude for simulation
            start_lon: Starting longitude for simulation
            movement_speed: Speed of simulated movement (degrees per read)
        """
        self.simulation_enabled = simulation_enabled
        self.current_lat = start_lat
        self.current_lon = start_lon
        self.movement_speed = movement_speed
        self.time_offset = 0
        self.movement_pattern = 0  # 0-7 for 8 directions

    def read(self) -> GPSData:
        """
        Read current GPS coordinates
        Прочитати поточні GPS координати
        """
        if self.simulation_enabled:
            return self._read_simulated()
        else:
            return self._read_hardware()

    def _read_simulated(self) -> GPSData:
        """
        Simulate GPS reading with realistic movement pattern
        Симулювати читання GPS з реалістичним патерном руху
        """
        # Simulate circular/random walk pattern
        angle = (self.movement_pattern * math.pi / 4)  # 45 degree increments

        # Add some randomness to movement
        self.current_lat += self.movement_speed * math.cos(angle)
        self.current_lon += self.movement_speed * math.sin(angle)

        # Change direction periodically
        if self.time_offset % 5 == 0:
            self.movement_pattern = (self.movement_pattern + 1) % 8

        self.time_offset += 1

        # Add slight random variation
        lat_variation = (hash(str(time.time())) % 100 - 50) * 0.000001
        lon_variation = (hash(str(time.time() + 1)) % 100 - 50) * 0.000001

        final_lat = self.current_lat + lat_variation
        final_lon = self.current_lon + lon_variation

        return GPSData(
            latitude=round(final_lat, 6),
            longitude=round(final_lon, 6),
            timestamp=int(time.time())
        )

    def _read_hardware(self) -> GPSData:
        """
        Read GPS data from actual hardware module
        Прочитати GPS дані з реального апаратного модуля

        This would interface with UART/I2C GPS module
        Це працювало б через UART/I2C з GPS модулем
        """
        # TODO: Implement actual GPS module reading
        # Example for NEO-6M:
        # - Read NMEA sentences from UART
        # - Parse GPGGA or GPRMC sentences
        # - Extract latitude and longitude

        raise NotImplementedError("Hardware GPS reading not implemented yet")

    def is_valid_fix(self) -> bool:
        """
        Check if GPS has a valid position fix
        Перевірити, чи є у GPS валідний фікс позиції
        """
        if self.simulation_enabled:
            return True  # Simulation always has fix
        else:
            # TODO: Check GPS fix status from hardware
            return False

    def get_satellite_count(self) -> int:
        """
        Get number of satellites in view
        Отримати кількість видимих супутників
        """
        if self.simulation_enabled:
            return 8  # Simulated satellite count
        else:
            # TODO: Get actual satellite count from GPS module
            return 0

    def reset_position(self, lat: float, lon: float):
        """
        Reset GPS position (for simulation)
        Скинути позицію GPS (для симуляції)
        """
        self.current_lat = lat
        self.current_lon = lon
        self.time_offset = 0

    def __repr__(self):
        return (f"GPSSensor(lat={self.current_lat:.6f}, lon={self.current_lon:.6f}, "
                f"simulated={self.simulation_enabled})")


class GPSSensorMock:
    """
    Mock GPS sensor for testing without hardware
    Макет GPS сенсора для тестування без обладнання
    """

    def __init__(self, fixed_lat=50.4501, fixed_lon=30.5234):
        self.fixed_lat = fixed_lat
        self.fixed_lon = fixed_lon

    def read(self) -> GPSData:
        """Return fixed GPS coordinates"""
        return GPSData(
            latitude=self.fixed_lat,
            longitude=self.fixed_lon,
            timestamp=int(time.time())
        )

    def is_valid_fix(self) -> bool:
        return True

    def get_satellite_count(self) -> int:
        return 5
