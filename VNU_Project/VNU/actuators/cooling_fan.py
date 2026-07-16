"""
Cooling Fan Actuator Module for Smart Greenhouse
"""
from datetime import datetime

class CoolingFan:
    def __init__(self, actuator_id="fan_001"):
        self.actuator_id = actuator_id
        self.is_on = False
        self.speed_level = 0  # 0-100%
        self.last_activation = None
        self.last_deactivation = None
        
    def turn_on(self, speed_level=100):
        """Turn on the cooling fan with specified speed level"""
        self.is_on = True
        self.speed_level = max(0, min(100, speed_level))  # Clamp between 0-100
        self.last_activation = datetime.now()
        return True
    
    def turn_off(self):
        """Turn off the cooling fan"""
        self.is_on = False
        self.speed_level = 0
        self.last_deactivation = datetime.now()
        return True
    
    def set_speed_level(self, speed_level):
        """Set the fan speed level"""
        if self.is_on:
            self.speed_level = max(0, min(100, speed_level))
            return True
        return False
    
    def get_status(self):
        """Get fan status"""
        return {
            "actuator_id": self.actuator_id,
            "is_on": self.is_on,
            "speed_level": self.speed_level,
            "last_activation": self.last_activation.isoformat() if self.last_activation else None,
            "last_deactivation": self.last_deactivation.isoformat() if self.last_deactivation else None
        }

if __name__ == "__main__":
    # Test the cooling fan
    fan = CoolingFan()
    print("Fan initial status:", fan.get_status())
    
    # Turn on fan
    fan.turn_on(75)
    print("Fan turned on:", fan.get_status())
    
    # Turn off fan
    fan.turn_off()
    print("Fan turned off:", fan.get_status())
