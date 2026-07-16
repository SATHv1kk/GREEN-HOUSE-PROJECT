"""
pH Sensor Module for Smart Greenhouse
"""
import random
from datetime import datetime

class PHSensor:
    def __init__(self, sensor_id="ph_001", initial_ph=6.5):
        self.sensor_id = sensor_id
        self.current_ph = initial_ph
        self.is_active = True
        self.ph_range = (5.5, 7.5)  # pH scale
        self.last_update = datetime.now()
        
    def read_ph(self):
        """Read current pH level with realistic fluctuations"""
        if not self.is_active:
            return None
            
        # Add random fluctuation
        fluctuation = random.uniform(-0.05, 0.05)
        
        # Update pH with bounds checking
        self.current_ph += fluctuation
        self.current_ph = max(self.ph_range[0], min(self.ph_range[1], self.current_ph))
        
        self.last_update = datetime.now()
        return round(self.current_ph, 2)
    
    def calibrate(self, reference_ph):
        """Calibrate sensor with reference pH level"""
        self.current_ph = reference_ph
        return True
    
    def get_status(self):
        """Get sensor status"""
        return {
            "sensor_id": self.sensor_id,
            "is_active": self.is_active,
            "current_ph": self.current_ph,
            "last_update": self.last_update.isoformat()
        }
    
    def activate(self):
        """Activate the sensor"""
        self.is_active = True
        
    def deactivate(self):
        """Deactivate the sensor"""
        self.is_active = False

if __name__ == "__main__":
    # Test the pH sensor
    ph_sensor = PHSensor()
    print(f"Initial pH level: {ph_sensor.read_ph()}")
    
    # Simulate readings over time
    for i in range(10):
        ph_value = ph_sensor.read_ph()
        print(f"pH reading {i+1}: {ph_value}")
