"""
Dehumidifier Actuator Module for Smart Greenhouse
"""
from datetime import datetime

class Dehumidifier:
    def __init__(self, actuator_id="dehumidifier_001"):
        self.actuator_id = actuator_id
        self.is_on = False
        self.output_level = 0  # 0-100%
        self.last_activation = None
        self.last_deactivation = None
        
    def turn_on(self, output_level=100):
        """Turn on the dehumidifier with specified output level"""
        self.is_on = True
        self.output_level = max(0, min(100, output_level))  # Clamp between 0-100
        self.last_activation = datetime.now()
        return True
    
    def turn_off(self):
        """Turn off the dehumidifier"""
        self.is_on = False
        self.output_level = 0
        self.last_deactivation = datetime.now()
        return True
    
    def set_output_level(self, output_level):
        """Set the dehumidifier output level"""
        if self.is_on:
            self.output_level = max(0, min(100, output_level))
            return True
        return False
    
    def get_status(self):
        """Get dehumidifier status"""
        return {
            "actuator_id": self.actuator_id,
            "is_on": self.is_on,
            "output_level": self.output_level,
            "last_activation": self.last_activation.isoformat() if self.last_activation else None,
            "last_deactivation": self.last_deactivation.isoformat() if self.last_deactivation else None
        }

if __name__ == "__main__":
    # Test the dehumidifier
    dehumidifier = Dehumidifier()
    print("Dehumidifier initial status:", dehumidifier.get_status())
    
    # Turn on dehumidifier
    dehumidifier.turn_on(75)
    print("Dehumidifier turned on:", dehumidifier.get_status())
    
    # Turn off dehumidifier
    dehumidifier.turn_off()
    print("Dehumidifier turned off:", dehumidifier.get_status())
