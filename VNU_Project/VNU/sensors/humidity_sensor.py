"""
Humidity Sensor Module for Smart Greenhouse
"""
import random
from datetime import datetime

class HumiditySensor:
    def __init__(self, sensor_id="humid_001", initial_humidity=65.0):
        self.sensor_id = sensor_id
        self.current_humidity = initial_humidity
        self.is_active = True
        self.day_humidity_range = (60, 80)  # Percentage
        self.night_humidity_range = (65, 85)  # Percentage
        self.last_update = datetime.now()
        
    def read_humidity(self, is_day=True):
        """Read current humidity with realistic fluctuations"""
        if not self.is_active:
            return None
            
        # Base humidity range based on day/night
        if is_day:
            min_humid, max_humid = self.day_humidity_range
        else:
            min_humid, max_humid = self.night_humidity_range
            
        # Add random fluctuation
        fluctuation = random.uniform(-1.0, 1.0)
        
        # Update humidity with bounds checking
        self.current_humidity += fluctuation
        self.current_humidity = max(min_humid, min(max_humid, self.current_humidity))
        
        self.last_update = datetime.now()
        return round(self.current_humidity, 1)
    
    def calibrate(self, reference_humidity):
        """Calibrate sensor with reference humidity"""
        self.current_humidity = reference_humidity
        return True
    
    def get_status(self):
        """Get sensor status"""
        return {
            "sensor_id": self.sensor_id,
            "is_active": self.is_active,
            "current_humidity": self.current_humidity,
            "last_update": self.last_update.isoformat()
        }
    
    def activate(self):
        """Activate the sensor"""
        self.is_active = True
        
    def deactivate(self):
        """Deactivate the sensor"""
        self.is_active = False

if __name__ == "__main__":
    # Test the humidity sensor
    humid_sensor = HumiditySensor()
    print(f"Initial humidity: {humid_sensor.read_humidity()}%")
    
    # Simulate readings over time
    for i in range(10):
        humidity = humid_sensor.read_humidity(is_day=True)
        print(f"Humidity reading {i+1}: {humidity}%")
