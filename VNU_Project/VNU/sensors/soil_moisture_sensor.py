"""
Soil Moisture Sensor Module for Smart Greenhouse
"""
import random
from datetime import datetime

class SoilMoistureSensor:
    def __init__(self, sensor_id="soil_001", initial_moisture=45.0):
        self.sensor_id = sensor_id
        self.current_moisture = initial_moisture
        self.is_active = True
        self.moisture_range = (0, 100)  # Percentage
        self.last_update = datetime.now()
        
    def read_moisture(self, is_optimal=False, irrigation_active=False):
        """Read current soil moisture with realistic fluctuations"""
        if not self.is_active:
            return None
            
        # Add random fluctuation (natural moisture loss)
        fluctuation = random.uniform(-0.5, 0.2)
        
        # If irrigation is active, keep within optimal range (40-60%)
        if irrigation_active:
            optimal_min, optimal_max = (40, 60)
            self.current_moisture = max(optimal_min, min(optimal_max, self.current_moisture + fluctuation))
        # If in optimal mode, keep within 40-60% range
        elif is_optimal:
            optimal_min, optimal_max = (40, 60)
            self.current_moisture = max(optimal_min, min(optimal_max, self.current_moisture + fluctuation))
        else:
            # Update moisture with bounds checking, but let it go as low as 20%
            self.current_moisture += fluctuation
            self.current_moisture = max(20, min(self.moisture_range[1], self.current_moisture))  # Minimum 20%
        
        self.last_update = datetime.now()
        return round(self.current_moisture, 1)
    
    def calibrate(self, reference_moisture):
        """Calibrate sensor with reference moisture"""
        self.current_moisture = reference_moisture
        return True
    
    def get_status(self):
        """Get sensor status"""
        return {
            "sensor_id": self.sensor_id,
            "is_active": self.is_active,
            "current_moisture": self.current_moisture,
            "last_update": self.last_update.isoformat()
        }
    
    def activate(self):
        """Activate the sensor"""
        self.is_active = True
        
    def deactivate(self):
        """Deactivate the sensor"""
        self.is_active = False

if __name__ == "__main__":
    # Test the soil moisture sensor
    soil_sensor = SoilMoistureSensor()
    print(f"Initial soil moisture: {soil_sensor.read_moisture()}%")
    
    # Simulate readings over time
    for i in range(10):
        moisture = soil_sensor.read_moisture()
        print(f"Soil moisture reading {i+1}: {moisture}%")
