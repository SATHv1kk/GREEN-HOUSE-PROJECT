"""
Temperature Sensor Module for Smart Greenhouse
"""
import random
import time
from datetime import datetime

class TemperatureSensor:
    def __init__(self, sensor_id="temp_001", initial_temp=25.0):
        self.sensor_id = sensor_id
        self.current_temperature = initial_temp
        self.is_active = True
        self.day_temp_range = (22, 28)  # Celsius
        self.night_temp_range = (16, 20)  # Celsius
        self.last_update = datetime.now()
        
    def read_temperature(self, is_day=True):
        """Read current temperature with realistic fluctuations"""
        if not self.is_active:
            return None
            
        # Base temperature range based on day/night
        if is_day:
            min_temp, max_temp = self.day_temp_range
        else:
            min_temp, max_temp = self.night_temp_range
            
        # Add random fluctuation
        fluctuation = random.uniform(-0.5, 0.5)
        
        # Update temperature with bounds checking
        self.current_temperature += fluctuation
        self.current_temperature = max(min_temp, min(max_temp, self.current_temperature))
        
        self.last_update = datetime.now()
        return round(self.current_temperature, 1)
    
    def calibrate(self, reference_temp):
        """Calibrate sensor with reference temperature"""
        self.current_temperature = reference_temp
        return True
    
    def get_status(self):
        """Get sensor status"""
        return {
            "sensor_id": self.sensor_id,
            "is_active": self.is_active,
            "current_temperature": self.current_temperature,
            "last_update": self.last_update.isoformat()
        }
    
    def activate(self):
        """Activate the sensor"""
        self.is_active = True
        
    def deactivate(self):
        """Deactivate the sensor"""
        self.is_active = False

if __name__ == "__main__":
    # Test the temperature sensor
    temp_sensor = TemperatureSensor()
    print(f"Initial temperature: {temp_sensor.read_temperature()}°C")
    
    # Simulate readings over time
    for i in range(10):
        temp = temp_sensor.read_temperature(is_day=True)
        print(f"Temperature reading {i+1}: {temp}°C")
        time.sleep(0.1)
