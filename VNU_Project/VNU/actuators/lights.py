"""
Grow Lights Actuator Module for Smart Greenhouse
"""
from datetime import datetime

class GrowLights:
    def __init__(self, actuator_id="lights_001"):
        self.actuator_id = actuator_id
        self.is_on = False
        self.brightness_level = 0  # 0-100%
        self.last_activation = None
        self.last_deactivation = None
        
    def turn_on(self, brightness_level=100):
        """Turn on the grow lights with specified brightness level"""
        self.is_on = True
        self.brightness_level = max(0, min(100, brightness_level))  # Clamp between 0-100
        self.last_activation = datetime.now()
        return True
    
    def turn_off(self):
        """Turn off the grow lights"""
        self.is_on = False
        self.brightness_level = 0
        self.last_deactivation = datetime.now()
        return True
    
    def set_brightness_level(self, brightness_level):
        """Set the grow lights brightness level"""
        if self.is_on:
            self.brightness_level = max(0, min(100, brightness_level))
            return True
        return False
    
    def get_status(self):
        """Get grow lights status"""
        return {
            "actuator_id": self.actuator_id,
            "is_on": self.is_on,
            "brightness_level": self.brightness_level,
            "last_activation": self.last_activation.isoformat() if self.last_activation else None,
            "last_deactivation": self.last_deactivation.isoformat() if self.last_deactivation else None
        }

if __name__ == "__main__":
    # Test the grow lights
    lights = GrowLights()
    print("Lights initial status:", lights.get_status())
    
    # Turn on lights
    lights.turn_on(75)
    print("Lights turned on:", lights.get_status())
    
    # Turn off lights
    lights.turn_off()
    print("Lights turned off:", lights.get_status())
