"""
Nutrient Sensor Module for Smart Greenhouse
"""
import random
from datetime import datetime

class NutrientSensor:
    def __init__(self, sensor_id="nutrient_001", initial_level=75.0):
        self.sensor_id = sensor_id
        self.current_level = initial_level
        self.is_active = True
        self.level_range = (0, 100)  # Percentage
        self.last_update = datetime.now()
        
    def read_nutrient_level(self, is_optimal=False):
        """Read current nutrient level with realistic fluctuations"""
        if not self.is_active:
            return None
            
        # Add random fluctuation (natural nutrient consumption)
        fluctuation = random.uniform(-0.3, 0.1)
        
        # If in optimal mode, keep within 70-90% range
        if is_optimal:
            optimal_min, optimal_max = (70, 90)
            self.current_level = max(optimal_min, min(optimal_max, self.current_level + fluctuation))
        else:
            # Update nutrient level with bounds checking, but never let it reach zero
            self.current_level += fluctuation
            self.current_level = max(1, min(self.level_range[1], self.current_level))  # Minimum 1%
        
        self.last_update = datetime.now()
        return round(self.current_level, 1)
    
    def calibrate(self, reference_level):
        """Calibrate sensor with reference nutrient level"""
        self.current_level = reference_level
        return True
    
    def get_status(self):
        """Get sensor status"""
        return {
            "sensor_id": self.sensor_id,
            "is_active": self.is_active,
            "current_level": self.current_level,
            "last_update": self.last_update.isoformat()
        }
    
    def activate(self):
        """Activate the sensor"""
        self.is_active = True
        
    def deactivate(self):
        """Deactivate the sensor"""
        self.is_active = False

if __name__ == "__main__":
    # Test the nutrient sensor
    nutrient_sensor = NutrientSensor()
    print(f"Initial nutrient level: {nutrient_sensor.read_nutrient_level()}%")
    
    # Simulate readings over time
    for i in range(10):
        level = nutrient_sensor.read_nutrient_level()
        print(f"Nutrient level reading {i+1}: {level}%")
