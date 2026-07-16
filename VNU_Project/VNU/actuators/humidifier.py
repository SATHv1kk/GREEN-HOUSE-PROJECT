"""
Humidifier Actuator Module for Smart Greenhouse
"""
from datetime import datetime

class Humidifier:
    def __init__(self, actuator_id="humidifier_001"):
        self.actuator_id = actuator_id
        self.is_on = False
        self.output_level = 0  # 0-100%
        self.last_activation = None
        self.last_deactivation = None
        
    def turn_on(self, output_level=100):
        """Turn on the humidifier with specified output level"""
        self.is_on = True
        self.output_level = max(0, min(100, output_level))  # Clamp between 0-100
        self.last_activation = datetime.now()
        return True
    
    def turn_off(self):
        """Turn off the humidifier"""
        self.is_on = False
        self.output_level = 0
        self.last_deactivation = datetime.now()
        return True
    
    def set_output_level(self, output_level):
        """Set the humidifier output level"""
        if self.is_on:
            self.output_level = max(0, min(100, output_level))
            return True
        return False
    
    def get_status(self):
        """Get humidifier status"""
        return {
            "actuator_id": self.actuator_id,
            "is_on": self.is_on,
            "output_level": self.output_level,
            "last_activation": self.last_activation.isoformat() if self.last_activation else None,
            "last_deactivation": self.last_deactivation.isoformat() if self.last_deactivation else None
        }

if __name__ == "__main__":
    # Test the humidifier
    humidifier = Humidifier()
    print("Humidifier initial status:", humidifier.get_status())
    
    # Turn on humidifier
    humidifier.turn_on(75)
    print("Humidifier turned on:", humidifier.get_status())
    
    # Turn off humidifier
    humidifier.turn_off()
    print("Humidifier turned off:", humidifier.get_status())
