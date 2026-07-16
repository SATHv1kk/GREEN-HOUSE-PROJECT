"""
Irrigation Actuator Module for Smart Greenhouse
"""
from datetime import datetime

class IrrigationSystem:
    def __init__(self, actuator_id="irrigation_001"):
        self.actuator_id = actuator_id
        self.is_on = False
        self.flow_rate = 0  # 0-100%
        self.last_activation = None
        self.last_deactivation = None
        
    def turn_on(self, flow_rate=100):
        """Turn on the irrigation system with specified flow rate"""
        self.is_on = True
        self.flow_rate = max(0, min(100, flow_rate))  # Clamp between 0-100
        self.last_activation = datetime.now()
        return True
    
    def turn_off(self):
        """Turn off the irrigation system"""
        self.is_on = False
        self.flow_rate = 0
        self.last_deactivation = datetime.now()
        return True
    
    def set_flow_rate(self, flow_rate):
        """Set the irrigation flow rate"""
        if self.is_on:
            self.flow_rate = max(0, min(100, flow_rate))
            return True
        return False
    
    def get_status(self):
        """Get irrigation system status"""
        return {
            "actuator_id": self.actuator_id,
            "is_on": self.is_on,
            "flow_rate": self.flow_rate,
            "last_activation": self.last_activation.isoformat() if self.last_activation else None,
            "last_deactivation": self.last_deactivation.isoformat() if self.last_deactivation else None
        }

if __name__ == "__main__":
    # Test the irrigation system
    irrigation = IrrigationSystem()
    print("Irrigation initial status:", irrigation.get_status())
    
    # Turn on irrigation
    irrigation.turn_on(75)
    print("Irrigation turned on:", irrigation.get_status())
    
    # Turn off irrigation
    irrigation.turn_off()
    print("Irrigation turned off:", irrigation.get_status())
