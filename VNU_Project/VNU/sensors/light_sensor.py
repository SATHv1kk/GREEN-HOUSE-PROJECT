"""
Light Sensor Module for Smart Greenhouse
"""
import random
from datetime import datetime

class LightSensor:
    def __init__(self, sensor_id="light_001", initial_lux=25000.0):
        self.sensor_id = sensor_id
        self.current_lux = initial_lux
        self.is_active = True
        self.day_lux_range = (20000, 50000)  # Lux
        self.night_lux_range = (10, 50)  # Lux
        self.last_update = datetime.now()
        
    def read_lux(self, is_day=True):
        """Read current light intensity with realistic fluctuations"""
        if not self.is_active:
            return None
            
        # Base light range based on day/night
        if is_day:
            min_lux, max_lux = self.day_lux_range
        else:
            min_lux, max_lux = self.night_lux_range
            
        # Add random fluctuation
        fluctuation = random.uniform(-20, 20)
        
        # Update lux with bounds checking
        self.current_lux += fluctuation
        self.current_lux = max(min_lux, min(max_lux, self.current_lux))
        
        self.last_update = datetime.now()
        return round(self.current_lux, 1)
    
    def calibrate(self, reference_lux):
        """Calibrate sensor with reference lux"""
        self.current_lux = reference_lux
        return True
    
    def get_status(self):
        """Get sensor status"""
        return {
            "sensor_id": self.sensor_id,
            "is_active": self.is_active,
            "current_lux": self.current_lux,
            "last_update": self.last_update.isoformat()
        }
    
    def activate(self):
        """Activate the sensor"""
        self.is_active = True
        
    def deactivate(self):
        """Deactivate the sensor"""
        self.is_active = False

if __name__ == "__main__":
    # Test the light sensor
    light_sensor = LightSensor()
    print(f"Initial light level: {light_sensor.read_lux()} lux")
    
    # Simulate readings over time
    for i in range(10):
        lux = light_sensor.read_lux(is_day=True)
        print(f"Light reading {i+1}: {lux} lux")
