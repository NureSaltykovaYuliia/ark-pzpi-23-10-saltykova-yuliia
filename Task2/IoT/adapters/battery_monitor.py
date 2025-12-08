"""
Battery Monitor Adapter (Infrastructure Layer)
Адаптер моніторингу батареї (Інфраструктурний шар)
"""
import time
from core.entities import BatteryData


class BatteryMonitor:
    """
    Battery monitor adapter for reading battery level
    Адаптер моніторингу батареї для читання рівня заряду

    In real hardware, this would read from ADC pin connected to battery
    На реальному обладнанні це читало б з АЦП підключеного до батареї
    """

    def __init__(self, simulation_enabled=True, initial_level=100.0,
                 drain_rate=0.1, adc_pin=None):
        """
        Initialize battery monitor

        Args:
            simulation_enabled: Whether to use simulated battery data
            initial_level: Starting battery level (0-100)
            drain_rate: Battery drain rate per minute
            adc_pin: ADC pin number for hardware reading
        """
        self.simulation_enabled = simulation_enabled
        self.current_level = initial_level
        self.drain_rate = drain_rate  # percent per minute
        self.last_read_time = time.time()
        self.adc_pin = adc_pin
        self.adc = None

        if not simulation_enabled and adc_pin is not None:
            self._init_hardware()

    def _init_hardware(self):
        """
        Initialize hardware ADC for battery reading
        Ініціалізувати апаратний АЦП для читання батареї
        """
        try:
            from machine import ADC, Pin
            self.adc = ADC(Pin(self.adc_pin))
            self.adc.atten(ADC.ATTN_11DB)  # Full range: 0-3.6V
            self.adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution (0-4095)
        except ImportError:
            print("[WARNING] machine module not available, using simulation")
            self.simulation_enabled = True

    def read(self) -> BatteryData:
        """
        Read current battery level
        Прочитати поточний рівень батареї
        """
        if self.simulation_enabled:
            return self._read_simulated()
        else:
            return self._read_hardware()

    def _read_simulated(self) -> BatteryData:
        """
        Simulate battery reading with gradual drain
        Симулювати читання батареї з поступовим розрядом
        """
        current_time = time.time()
        elapsed_minutes = (current_time - self.last_read_time) / 60.0

        # Calculate battery drain
        drain = self.drain_rate * elapsed_minutes
        self.current_level = max(0.0, self.current_level - drain)

        self.last_read_time = current_time

        return BatteryData(
            level=round(self.current_level, 1),
            timestamp=int(current_time)
        )

    def _read_hardware(self) -> BatteryData:
        """
        Read battery level from actual hardware ADC
        Прочитати рівень батареї з реального апаратного АЦП

        Assumes voltage divider circuit:
        Battery+ -> R1 -> ADC_PIN -> R2 -> GND

        For LiPo battery (3.0V - 4.2V):
        - 4.2V = 100% (fully charged)
        - 3.7V = 50% (nominal)
        - 3.0V = 0% (discharged)
        """
        if self.adc is None:
            return self._read_simulated()

        try:
            # Read ADC value (0-4095 for 12-bit)
            adc_value = self.adc.read()

            # Convert to voltage (0-3.6V range with 11dB attenuation)
            voltage = (adc_value / 4095.0) * 3.6

            # Adjust for voltage divider if used
            # If using 2:1 divider (R1=R2), multiply by 2
            actual_voltage = voltage * 2

            # Convert voltage to battery percentage (for LiPo)
            battery_level = self._voltage_to_percentage(actual_voltage)

            return BatteryData(
                level=round(battery_level, 1),
                timestamp=int(time.time())
            )

        except Exception as e:
            print(f"[ERROR] Hardware battery reading failed: {e}")
            return self._read_simulated()

    def _voltage_to_percentage(self, voltage: float) -> float:
        """
        Convert battery voltage to percentage
        Перетворити напругу батареї в відсотки

        LiPo discharge curve approximation:
        4.2V -> 100%
        4.0V -> 85%
        3.7V -> 50%
        3.5V -> 20%
        3.0V -> 0%
        """
        if voltage >= 4.2:
            return 100.0
        elif voltage <= 3.0:
            return 0.0

        # Piecewise linear approximation
        voltage_map = [
            (3.0, 0.0),
            (3.5, 20.0),
            (3.7, 50.0),
            (4.0, 85.0),
            (4.2, 100.0)
        ]

        # Find the appropriate segment
        for i in range(len(voltage_map) - 1):
            v1, p1 = voltage_map[i]
            v2, p2 = voltage_map[i + 1]

            if v1 <= voltage <= v2:
                # Linear interpolation
                percentage = p1 + (voltage - v1) * (p2 - p1) / (v2 - v1)
                return percentage

        return 0.0

    def set_level(self, level: float):
        """
        Manually set battery level (for simulation/testing)
        Вручну встановити рівень батареї (для симуляції/тестування)
        """
        self.current_level = max(0.0, min(100.0, level))
        self.last_read_time = time.time()

    def reset(self, level: float = 100.0):
        """
        Reset battery to full charge (for simulation)
        Скинути батарею до повного заряду (для симуляції)
        """
        self.current_level = level
        self.last_read_time = time.time()

    def __repr__(self):
        return (f"BatteryMonitor(level={self.current_level:.1f}%, "
                f"simulated={self.simulation_enabled})")


class BatteryMonitorMock:
    """
    Mock battery monitor for testing
    Макет монітора батареї для тестування
    """

    def __init__(self, fixed_level=75.0):
        self.fixed_level = fixed_level

    def read(self) -> BatteryData:
        """Return fixed battery level"""
        return BatteryData(
            level=self.fixed_level,
            timestamp=int(time.time())
        )

    def set_level(self, level: float):
        """Set mock battery level"""
        self.fixed_level = max(0.0, min(100.0, level))
