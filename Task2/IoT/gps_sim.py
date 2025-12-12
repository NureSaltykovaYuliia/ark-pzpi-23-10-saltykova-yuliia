# adapters/gps_sim.py
import random

class GPSSimulator:
    def __init__(self, start_lat, start_lon):
        self.lat = start_lat
        self.lon = start_lon
    
    def get_location(self):
        # Імітуємо рух собаки на південь (до центру зони)
        # Кожен виклик собака наближається на ~11 метрів
        self.lat -= 0.0001 
        
        # Додаємо трохи "шуму" (ніби реальний GPS)
        jitter = random.uniform(-0.00001, 0.00001)
        
        return self.lat + jitter, self.lon + jitter