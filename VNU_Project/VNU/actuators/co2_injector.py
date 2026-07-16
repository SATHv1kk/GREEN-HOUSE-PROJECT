"""
CO2 Injector Actuator Module for Smart Greenhouse
"""
from datetime import datetime

class CO2Injector:
    def __init__(self, actuator_id="co2_injector_001"):
        self.actuator_id = actuator_id
        self.is_on = False
        self.injection_rate = 0  # 0-100%
        self.last_activation = None
        self.last_deactivation = None
        
    def turn_on(self, injection_rate=100):
        """Turn on the CO2 injector with specified injection rate"""
        self.is_on = True
        self.injection_rate = max(0, min(100, injection_rate))  # Clamp between 0-100
        self.last_activation = datetime.now()
        return True
    
    def turn_off(self):
        """Turn off the CO2 injector"""
        self.is_on = False
        self.injection_rate = 0
        self.last_deactivation = datetime.now()
        return True
    
    def set_injection_rate(self, injection_rate):
        """Set the CO2 injection rate"""
        if self.is_on:
            self.injection_rate = max(0, min(100, injection_rate))
            return True
        return False
    
    def get_status(self):
        """Get CO2 injector status"""
        return {
            "actuator_id": self.actuator_id,
            "is_on": self.is_on,
            "injection_rate": self.injection_rate,
            "last_activation": self.last_activation.isoformat() if self.last_activation else None,
            "last_deactivation": self.last_deactivation.isoformat() if self.last_deactivation else None
        }

if __name__ == "__main__":
    # Test the CO2 injector
    co2_injector = CO2Injector()
    print("CO2 injector initial status:", co2_injector.get_status())
    
    # Turn on CO2 injector
    co2_injector.turn_on(75)
    print("CO2 injector turned on:", co2_injector.get_status())
    
    # Turn off CO2 injector
    co2_injector.turn_off()
    print("CO2 injector turned off:", co2_injector.get_status())
