"""
CO2 Sensor Module for Smart Greenhouse
"""
import random
from datetime import datetime

class CO2Sensor:
    def __init__(self, sensor_id="co2_001", initial_ppm=400.0):
        self.sensor_id = sensor_id
        self.current_ppm = initial_ppm
        self.is_active = True
        self.day_co2_range = (350, 800)  # PPM
        self.night_co2_range = (300, 500)  # PPM
        self.last_update = datetime.now()
        
    def read_co2(self, is_day=True):
        """Read current CO2 level with realistic fluctuations"""
        if not self.is_active:
            return None
            
        # Base CO2 range based on day/night
        if is_day:
            min_co2, max_co2 = self.day_co2_range
        else:
            min_co2, max_co2 = self.night_co2_range
            
        # Add random fluctuation
        fluctuation = random.uniform(-10, 10)
        
        # Update CO2 with bounds checking
        self.current_ppm += fluctuation
        self.current_ppm = max(min_co2, min(max_co2, self.current_ppm))
        
        self.last_update = datetime.now()
        return round(self.current_ppm, 1)
    
    def calibrate(self, reference_ppm):
        """Calibrate sensor with reference CO2 level"""
        self.current_ppm = reference_ppm
        return True
    
    def get_status(self):
        """Get sensor status"""
        return {
            "sensor_id": self.sensor_id,
            "is_active": self.is_active,
            "current_ppm": self.current_ppm,
            "last_update": self.last_update.isoformat()
        }
    
    def activate(self):
        """Activate the sensor"""
        self.is_active = True
        
    def deactivate(self):
        """Deactivate the sensor"""
        self.is_active = False

if __name__ == "__main__":
    # Test the CO2 sensor
    co2_sensor = CO2Sensor()
    print(f"Initial CO2 level: {co2_sensor.read_co2()} ppm")
    
    # Simulate readings over time
    for i in range(10):
        ppm = co2_sensor.read_co2(is_day=True)
        print(f"CO2 reading {i+1}: {ppm} ppm")
