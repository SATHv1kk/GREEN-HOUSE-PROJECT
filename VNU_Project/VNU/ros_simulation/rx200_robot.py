"""
RX200 Robot Simulation Module for Smart Greenhouse
This module simulates the ROS interface for the RX200 robot
"""
import time
import threading
from datetime import datetime
from enum import Enum

class RobotState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    WATERING = "watering"
    APPLYING_MANURE = "applying_manure"
    APPLYING_FERTILIZER = "applying_fertilizer"

class RX200Robot:
    def __init__(self, robot_id="rx200_001"):
        self.robot_id = robot_id
        self.current_position = "A"  # Default position
        self.state = RobotState.IDLE
        self.zone_coordinates = {
            "A": (10, 10),
            "B": (10, 30),
            "C": (30, 10),
            "D": (30, 30)
        }
        self.battery_level = 100.0  # Percentage
        self.last_operation = None
        self.is_active = True
        
        # Start background thread for battery drain simulation
        self.battery_thread = threading.Thread(target=self._simulate_battery_drain, daemon=True)
        self.battery_thread.start()
        
    def move_to_zone(self, zone):
        """Move robot to specified zone"""
        if zone not in self.zone_coordinates:
            raise ValueError(f"Invalid zone: {zone}. Valid zones are: {list(self.zone_coordinates.keys())}")
            
        if not self.is_active:
            return False
            
        # Simulate movement time
        self.state = RobotState.MOVING
        movement_time = 2  # seconds
        time.sleep(movement_time * 0.1)  # Simulated time
        
        self.current_position = zone
        self.state = RobotState.IDLE
        self.last_operation = {
            "operation": "move",
            "zone": zone,
            "timestamp": datetime.now().isoformat()
        }
        
        return True
    
    def water_zone(self, zone):
        """Water the specified zone"""
        if zone not in self.zone_coordinates:
            raise ValueError(f"Invalid zone: {zone}")
            
        if not self.is_active:
            return False
            
        # Move to zone if not already there
        if self.current_position != zone:
            self.move_to_zone(zone)
            
        # Perform watering
        self.state = RobotState.WATERING
        watering_time = 3  # seconds
        time.sleep(watering_time * 0.1)  # Simulated time
        
        self.state = RobotState.IDLE
        self.last_operation = {
            "operation": "watering",
            "zone": zone,
            "timestamp": datetime.now().isoformat()
        }
        
        return True
    
    def apply_manure(self, zone):
        """Apply manure to the specified zone"""
        if zone not in self.zone_coordinates:
            raise ValueError(f"Invalid zone: {zone}")
            
        if not self.is_active:
            return False
            
        # Move to zone if not already there
        if self.current_position != zone:
            self.move_to_zone(zone)
            
        # Apply manure
        self.state = RobotState.APPLYING_MANURE
        manure_time = 4  # seconds
        time.sleep(manure_time * 0.1)  # Simulated time
        
        self.state = RobotState.IDLE
        self.last_operation = {
            "operation": "manure",
            "zone": zone,
            "timestamp": datetime.now().isoformat()
        }
        
        return True
    
    def apply_fertilizer(self, zone):
        """Apply fertilizer to the specified zone"""
        if zone not in self.zone_coordinates:
            raise ValueError(f"Invalid zone: {zone}")
            
        if not self.is_active:
            return False
            
        # Move to zone if not already there
        if self.current_position != zone:
            self.move_to_zone(zone)
            
        # Apply fertilizer
        self.state = RobotState.APPLYING_FERTILIZER
        fertilizer_time = 3  # seconds
        time.sleep(fertilizer_time * 0.1)  # Simulated time
        
        self.state = RobotState.IDLE
        self.last_operation = {
            "operation": "fertilizer",
            "zone": zone,
            "timestamp": datetime.now().isoformat()
        }
        
        return True
    
    def _simulate_battery_drain(self):
        """Background thread to simulate battery drain"""
        while self.is_active:
            time.sleep(10)  # Check every 10 seconds
            if self.state != RobotState.IDLE:
                self.battery_level -= 0.1  # Drain during operation
            else:
                self.battery_level -= 0.05  # Slow drain when idle
            self.battery_level = max(0, self.battery_level)
    
    def charge_battery(self):
        """Charge the robot battery"""
        charging_time = 5  # seconds
        time.sleep(charging_time * 0.1)  # Simulated time
        self.battery_level = 100.0
        return True
    
    def get_status(self):
        """Get robot status"""
        return {
            "robot_id": self.robot_id,
            "current_position": self.current_position,
            "state": self.state.value,
            "zone_coordinates": self.zone_coordinates,
            "battery_level": round(self.battery_level, 1),
            "last_operation": self.last_operation,
            "is_active": self.is_active
        }
    
    def activate(self):
        """Activate the robot"""
        self.is_active = True
        
    def deactivate(self):
        """Deactivate the robot"""
        self.is_active = False
        self.state = RobotState.IDLE

if __name__ == "__main__":
    # Test the RX200 robot
    robot = RX200Robot()
    print("Robot initial status:", robot.get_status())
    
    # Move to zone B
    print("Moving to zone B...")
    robot.move_to_zone("B")
    print("Current status:", robot.get_status())
    
    # Water zone B
    print("Watering zone B...")
    robot.water_zone("B")
    print("Current status:", robot.get_status())
    
    # Apply manure to zone B
    print("Applying manure to zone B...")
    robot.apply_manure("B")
    print("Current status:", robot.get_status())
