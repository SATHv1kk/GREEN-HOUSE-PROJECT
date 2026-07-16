"""
Heater Actuator Module for Smart Greenhouse
"""
from datetime import datetime

class Heater:
    def __init__(self, actuator_id="heater_001"):
        self.actuator_id = actuator_id
        self.is_on = False
        self.power_level = 0  # 0-100%
        self.last_activation = None
        self.last_deactivation = None
        
    def turn_on(self, power_level=100):
        """Turn on the heater with specified power level"""
        self.is_on = True
        self.power_level = max(0, min(100, power_level))  # Clamp between 0-100
        self.last_activation = datetime.now()
        return True
    
    def turn_off(self):
        """Turn off the heater"""
        self.is_on = False
        self.power_level = 0
        self.last_deactivation = datetime.now()
        return True
    
    def set_power_level(self, power_level):
        """Set the heater power level"""
        if self.is_on:
            self.power_level = max(0, min(100, power_level))
            return True
        return False
    
    def get_status(self):
        """Get heater status"""
        return {
            "actuator_id": self.actuator_id,
            "is_on": self.is_on,
            "power_level": self.power_level,
            "last_activation": self.last_activation.isoformat() if self.last_activation else None,
            "last_deactivation": self.last_deactivation.isoformat() if self.last_deactivation else None
        }

if __name__ == "__main__":
    # Test the heater
    heater = Heater()
    print("Heater initial status:", heater.get_status())
    
    # Turn on heater
    heater.turn_on(75)
    print("Heater turned on:", heater.get_status())
    
    # Turn off heater
    heater.turn_off()
    print("Heater turned off:", heater.get_status())
