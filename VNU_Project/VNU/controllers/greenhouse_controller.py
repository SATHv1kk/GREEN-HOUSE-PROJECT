"""
Main Controller for Smart Greenhouse Simulation
This controller integrates all sensors, actuators, and the RX200 robot
"""
import time
import threading
import json
from datetime import datetime

# Import sensor modules
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.light_sensor import LightSensor
from sensors.co2_sensor import CO2Sensor
from sensors.ph_sensor import PHSensor
from sensors.nutrient_sensor import NutrientSensor

# Import actuator modules
from actuators.heater import Heater
from actuators.cooling_fan import CoolingFan
from actuators.humidifier import Humidifier
from actuators.dehumidifier import Dehumidifier
from actuators.irrigation import IrrigationSystem
from actuators.lights import GrowLights
from actuators.co2_injector import CO2Injector
from actuators.nutrient_pump import NutrientPump

# Import ROS simulation
from ros_simulation.rx200_robot import RX200Robot

class GreenhouseController:
    def __init__(self):
        # Initialize sensors
        self.temperature_sensor = TemperatureSensor()
        self.humidity_sensor = HumiditySensor()
        self.soil_moisture_sensor = SoilMoistureSensor()
        self.light_sensor = LightSensor()
        self.co2_sensor = CO2Sensor()
        self.ph_sensor = PHSensor()
        self.nutrient_sensor = NutrientSensor()
        
        # Initialize actuators
        self.heater = Heater()
        self.cooling_fan = CoolingFan()
        self.humidifier = Humidifier()
        self.dehumidifier = Dehumidifier()
        self.irrigation = IrrigationSystem()
        self.lights = GrowLights()
        self.co2_injector = CO2Injector()
        self.nutrient_pump = NutrientPump()
        
        # Initialize robot
        self.robot = RX200Robot()
        
        # Greenhouse settings
        self.is_day = True
        self.day_start = 6
        self.day_end = 18
        self.zone_effects = {
            "A": {"watering": 0, "manure": 0, "fertilizer": 0},
            "B": {"watering": 0, "manure": 0, "fertilizer": 0},
            "C": {"watering": 0, "manure": 0, "fertilizer": 0},
            "D": {"watering": 0, "manure": 0, "fertilizer": 0}
        }
        
        # Start background thread for sensor updates
        self.sensor_thread = threading.Thread(target=self._update_sensors_continuously, daemon=True)
        self.sensor_thread.start()
        
    def _update_sensors_continuously(self):
        """Background thread to continuously update sensor values"""
        while True:
            time.sleep(2)  # Update every 2 seconds
            # Sensors update automatically in their read methods
            pass
    
    def get_all_sensor_data(self):
        """Get data from all sensors"""
        # Check if irrigation is active
        irrigation_active = self.irrigation.is_on
        
        return {
            "temperature": self.temperature_sensor.read_temperature(self.is_day),
            "humidity": self.humidity_sensor.read_humidity(self.is_day),
            "soil_moisture": self.soil_moisture_sensor.read_moisture(irrigation_active=irrigation_active),
            "light_intensity": self.light_sensor.read_lux(self.is_day),
            "co2_level": self.co2_sensor.read_co2(self.is_day),
            "ph_level": self.ph_sensor.read_ph(),
            "nutrient_level": self.nutrient_sensor.read_nutrient_level()
        }
    
    def get_zone_specific_data(self, zone):
        """Get sensor data specific to a zone with applied effects"""
        # Check if irrigation is active
        irrigation_active = self.irrigation.is_on
        
        # Get base data with irrigation status
        base_data = {
            "temperature": self.temperature_sensor.read_temperature(self.is_day),
            "humidity": self.humidity_sensor.read_humidity(self.is_day),
            "soil_moisture": self.soil_moisture_sensor.read_moisture(irrigation_active=irrigation_active),
            "light_intensity": self.light_sensor.read_lux(self.is_day),
            "co2_level": self.co2_sensor.read_co2(self.is_day),
            "ph_level": self.ph_sensor.read_ph(),
            "nutrient_level": self.nutrient_sensor.read_nutrient_level()
        }
        
        # Apply zone-specific effects
        effects = self.zone_effects.get(zone, {"watering": 0, "manure": 0, "fertilizer": 0})
        
        # Modify soil moisture based on watering to keep in optimal range (40-60%)
        if effects["watering"] > 0:
            # Ensure soil moisture stays in optimal range (40-60%)
            optimal_min, optimal_max = (40, 60)
            # Read moisture with optimal flag to keep in range
            base_data["soil_moisture"] = self.soil_moisture_sensor.read_moisture(is_optimal=True, irrigation_active=irrigation_active)
            # Apply additional boost from watering effect
            boost = (effects["watering"] / 100.0) * 20  # Up to 20% boost
            base_data["soil_moisture"] = min(optimal_max, base_data["soil_moisture"] + boost)
            
        # Modify nutrient level based on fertilizer to keep in optimal range (70-90%)
        if effects["fertilizer"] > 0 or effects["manure"] > 0:
            # Ensure nutrient level stays in optimal range (70-90%)
            optimal_min, optimal_max = (70, 90)
            # Read nutrient level with optimal flag to keep in range
            base_data["nutrient_level"] = self.nutrient_sensor.read_nutrient_level(is_optimal=True)
            # Apply boost from fertilizer/manure effects
            fertilizer_boost = (effects["fertilizer"] / 100.0) * 20  # Up to 20% boost
            manure_boost = (effects["manure"] / 100.0) * 15  # Up to 15% boost
            total_boost = fertilizer_boost + manure_boost
            base_data["nutrient_level"] = min(optimal_max, base_data["nutrient_level"] + total_boost)
            
        # Modify pH level based on manure to keep in optimal range (6.0-6.8)
        if effects["manure"] > 0:
            # Apply boost from manure effect
            boost = (effects["manure"] / 100.0) * 0.8  # Up to 0.8 pH boost
            base_data["ph_level"] = max(6.0, min(6.8, base_data["ph_level"] + boost))
            
        return base_data
    
    def get_all_actuator_status(self):
        """Get status of all actuators"""
        return {
            "heater": self.heater.get_status(),
            "cooling_fan": self.cooling_fan.get_status(),
            "humidifier": self.humidifier.get_status(),
            "dehumidifier": self.dehumidifier.get_status(),
            "irrigation": self.irrigation.get_status(),
            "lights": self.lights.get_status(),
            "co2_injector": self.co2_injector.get_status(),
            "nutrient_pump": self.nutrient_pump.get_status()
        }
    
    def toggle_actuator(self, actuator_name, state=None):
        """Toggle or set state of an actuator"""
        actuators = {
            "heater": self.heater,
            "cooling_fan": self.cooling_fan,
            "humidifier": self.humidifier,
            "dehumidifier": self.dehumidifier,
            "irrigation": self.irrigation,
            "lights": self.lights,
            "co2_injector": self.co2_injector,
            "nutrient_pump": self.nutrient_pump
        }
        
        if actuator_name not in actuators:
            return False, f"Invalid actuator: {actuator_name}"
            
        actuator = actuators[actuator_name]
        
        if state is None:
            # Toggle state
            if actuator.is_on:
                actuator.turn_off()
            else:
                actuator.turn_on()
        else:
            # Set specific state
            if state:
                actuator.turn_on()
            else:
                actuator.turn_off()
                
        return True, f"{actuator_name} {'turned on' if actuator.is_on else 'turned off'}"
    
    def move_robot_to_zone(self, zone):
        """Move robot to specified zone"""
        try:
            success = self.robot.move_to_zone(zone)
            return success, f"Robot moved to zone {zone}" if success else "Failed to move robot"
        except ValueError as e:
            return False, str(e)
    
    def water_zone(self, zone):
        """Water specified zone"""
        try:
            success = self.robot.water_zone(zone)
            if success:
                # Apply watering effect to zone
                self.zone_effects[zone]["watering"] = min(100, self.zone_effects[zone]["watering"] + 20)
                # Start decay timer
                threading.Thread(target=self._decay_effect, args=(zone, "watering"), daemon=True).start()
            return success, f"Watered zone {zone}" if success else "Failed to water zone"
        except ValueError as e:
            return False, str(e)
    
    def apply_manure_to_zone(self, zone):
        """Apply manure to specified zone"""
        try:
            success = self.robot.apply_manure(zone)
            if success:
                # Apply manure effect to zone
                self.zone_effects[zone]["manure"] = min(100, self.zone_effects[zone]["manure"] + 15)
                # Start decay timer
                threading.Thread(target=self._decay_effect, args=(zone, "manure"), daemon=True).start()
            return success, f"Applied manure to zone {zone}" if success else "Failed to apply manure"
        except ValueError as e:
            return False, str(e)
    
    def apply_fertilizer_to_zone(self, zone):
        """Apply fertilizer to specified zone"""
        try:
            success = self.robot.apply_fertilizer(zone)
            if success:
                # Apply fertilizer effect to zone
                self.zone_effects[zone]["fertilizer"] = min(100, self.zone_effects[zone]["fertilizer"] + 25)
                # Start decay timer
                threading.Thread(target=self._decay_effect, args=(zone, "fertilizer"), daemon=True).start()
            return success, f"Applied fertilizer to zone {zone}" if success else "Failed to apply fertilizer"
        except ValueError as e:
            return False, str(e)
    
    def _decay_effect(self, zone, effect_type):
        """Decay the effect of operations over time"""
        time.sleep(30)  # Wait 30 seconds before starting decay
        while self.zone_effects[zone][effect_type] > 0:
            time.sleep(5)  # Decay every 5 seconds
            self.zone_effects[zone][effect_type] = max(0, self.zone_effects[zone][effect_type] - 5)
    
    def toggle_day_night(self):
        """Toggle between day and night mode"""
        self.is_day = not self.is_day
        return self.is_day, f"Switched to {'day' if self.is_day else 'night'} mode"
    
    def get_complete_status(self):
        """Get complete status of greenhouse system"""
        return {
            "sensors": self.get_all_sensor_data(),
            "actuators": self.get_all_actuator_status(),
            "robot": self.robot.get_status(),
            "settings": {
                "is_day": self.is_day,
                "day_start": self.day_start,
                "day_end": self.day_end
            },
            "zone_effects": self.zone_effects
        }

if __name__ == "__main__":
    # Test the greenhouse controller
    controller = GreenhouseController()
    print("Greenhouse Controller initialized")
    print("Initial status:", json.dumps(controller.get_complete_status(), indent=2))
    
    # Test toggling an actuator
    success, message = controller.toggle_actuator("heater")
    print(f"Heater toggle: {message}")
    
    # Test moving robot
    success, message = controller.move_robot_to_zone("B")
    print(f"Robot movement: {message}")
    
    # Test watering
    success, message = controller.water_zone("B")
    print(f"Watering: {message}")
    
    # Show updated status
    print("Updated status:", json.dumps(controller.get_complete_status(), indent=2))
