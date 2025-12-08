"""
Data Buffer Service (Application Layer)
Сервіс буферизації даних (Прикладний шар)
"""
from core.entities import DataRecord


class DataBuffer:
    """
    Circular buffer for storing sensor data when offline
    Циклічний буфер для зберігання даних сенсорів при відсутності з'єднання
    """

    def __init__(self, max_size=50):
        """
        Initialize data buffer

        Args:
            max_size: Maximum number of records to store
        """
        self.max_size = max_size
        self.records = []
        self.total_added = 0
        self.total_sent = 0

    def add(self, record: DataRecord):
        """
        Add data record to buffer
        Додати запис даних до буферу

        Args:
            record: DataRecord to add
        """
        # If buffer is full, remove oldest unsent record
        if len(self.records) >= self.max_size:
            # Try to remove oldest sent record first
            for i, rec in enumerate(self.records):
                if rec.sent:
                    self.records.pop(i)
                    break
            else:
                # No sent records found, remove oldest unsent record
                self.records.pop(0)
                print(f"[WARNING] Buffer full, removed oldest record")

        self.records.append(record)
        self.total_added += 1
        print(f"[BUFFER] Added record (total: {len(self.records)}/{self.max_size})")

    def get_unsent_records(self) -> list:
        """
        Get all unsent records from buffer
        Отримати всі невідправлені записи з буферу

        Returns:
            List of unsent DataRecord objects
        """
        return [rec for rec in self.records if not rec.sent]

    def get_all_records(self) -> list:
        """
        Get all records from buffer
        Отримати всі записи з буферу

        Returns:
            List of all DataRecord objects
        """
        return self.records.copy()

    def remove_sent_records(self):
        """
        Remove all successfully sent records from buffer
        Видалити всі успішно відправлені записи з буферу
        """
        before_count = len(self.records)
        self.records = [rec for rec in self.records if not rec.sent]
        removed_count = before_count - len(self.records)

        if removed_count > 0:
            self.total_sent += removed_count
            print(f"[BUFFER] Removed {removed_count} sent records (remaining: {len(self.records)})")

    def clear(self):
        """
        Clear all records from buffer
        Очистити всі записи з буферу
        """
        cleared_count = len(self.records)
        self.records.clear()
        print(f"[BUFFER] Cleared {cleared_count} records")

    def is_full(self) -> bool:
        """
        Check if buffer is full
        Перевірити, чи буфер заповнений

        Returns:
            True if buffer is full, False otherwise
        """
        return len(self.records) >= self.max_size

    def is_empty(self) -> bool:
        """
        Check if buffer is empty
        Перевірити, чи буфер порожній

        Returns:
            True if buffer is empty, False otherwise
        """
        return len(self.records) == 0

    def get_unsent_count(self) -> int:
        """
        Get number of unsent records
        Отримати кількість невідправлених записів

        Returns:
            Number of unsent records
        """
        return len([rec for rec in self.records if not rec.sent])

    def get_oldest_unsent_record(self) -> DataRecord:
        """
        Get oldest unsent record
        Отримати найстаріший невідправлений запис

        Returns:
            Oldest unsent DataRecord, or None if no unsent records
        """
        unsent = self.get_unsent_records()
        return unsent[0] if unsent else None

    def get_statistics(self) -> dict:
        """
        Get buffer statistics
        Отримати статистику буферу

        Returns:
            Dictionary with buffer statistics
        """
        unsent_count = self.get_unsent_count()
        sent_count = len(self.records) - unsent_count

        return {
            'total_records': len(self.records),
            'unsent_records': unsent_count,
            'sent_records': sent_count,
            'max_size': self.max_size,
            'total_added': self.total_added,
            'total_sent': self.total_sent,
            'buffer_usage_percent': (len(self.records) / self.max_size) * 100
        }

    def print_statistics(self):
        """
        Print buffer statistics to console
        Вивести статистику буферу в консоль
        """
        stats = self.get_statistics()
        print("\n[BUFFER STATISTICS]")
        print(f"  Current records: {stats['total_records']}/{stats['max_size']}")
        print(f"  Unsent records: {stats['unsent_records']}")
        print(f"  Sent records: {stats['sent_records']}")
        print(f"  Total added: {stats['total_added']}")
        print(f"  Total sent: {stats['total_sent']}")
        print(f"  Buffer usage: {stats['buffer_usage_percent']:.1f}%")

    def __repr__(self):
        return (f"DataBuffer(size={len(self.records)}/{self.max_size}, "
                f"unsent={self.get_unsent_count()})")


class DataBufferPersistent(DataBuffer):
    """
    Persistent data buffer that saves to file system
    Постійний буфер даних, що зберігається у файловій системі

    TODO: Implement file system persistence for ESP32
    """

    def __init__(self, max_size=50, filename='buffer.json'):
        super().__init__(max_size)
        self.filename = filename
        # TODO: Load from file on initialization

    def save_to_file(self):
        """
        Save buffer to file
        Зберегти буфер у файл
        """
        # TODO: Implement JSON serialization to file
        pass

    def load_from_file(self):
        """
        Load buffer from file
        Завантажити буфер з файлу
        """
        # TODO: Implement JSON deserialization from file
        pass
