import sqlite3
import sys
from pathlib import Path

db_path = Path(__file__).parent / "Infrastructure" / "DB_Storage" / "MyDogSpace.db"

if not db_path.exists():
    print(f"❌ База данных не найдена: {db_path}")
    sys.exit(1)

print(f"✅ База данных найдена: {db_path}")
print(f"📊 Размер: {db_path.stat().st_size / 1024:.2f} KB\n")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получаем список таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print("📋 Таблицы в базе данных:")
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  - {table_name}: {count} записей")

# Проверяем пользователей
print("\n👥 Пользователи:")
cursor.execute("SELECT Id, Username, Email, Role FROM Users LIMIT 5")
users = cursor.fetchall()
for user in users:
    print(f"  ID {user[0]}: {user[1]} ({user[2]}) - {user[3]}")

# Проверяем собак
print("\n🐕 Собаки:")
cursor.execute("SELECT Id, Name, Breed, OwnerId FROM Dogs LIMIT 5")
dogs = cursor.fetchall()
for dog in dogs:
    print(f"  ID {dog[0]}: {dog[1]} ({dog[2]}) - Owner: {dog[3]}")

# Проверяем события
print("\n📅 События:")
cursor.execute("SELECT Id, Name, StartTime, OrganizerId FROM Events LIMIT 5")
events = cursor.fetchall()
for event in events:
    print(f"  ID {event[0]}: {event[1]} - {event[2]} - Organizer: {event[3]}")

# Проверяем устройства
print("\n📱 Smart Devices:")
cursor.execute("SELECT Id, DeviceGuid, DogId, BatteryLevel FROM SmartDevices LIMIT 5")
devices = cursor.fetchall()
for device in devices:
    print(f"  ID {device[0]}: {device[1]} - Dog: {device[2]} - Battery: {device[3]}%")

conn.close()

print("\n✅ Проверка завершена!")
