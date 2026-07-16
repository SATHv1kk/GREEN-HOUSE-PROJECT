# Smart Greenhouse Sensor-Actuator Relationships

## Overview
This document describes the relationships between sensors and actuators in the Smart Greenhouse system for elderly farmers. The system uses a closed-loop control approach where actuators respond to sensor readings to maintain optimal growing conditions.

## Sensor-Actuator Pairs

### 1. Temperature Control System
**Sensors:**
- Temperature Sensor (`sensors/temperature_sensor.py`)

**Actuators:**
- Heater (`actuators/heater.py`)
- Cooling Fan (`actuators/cooling_fan.py`)

**Relationship:**
- When temperature drops below optimal range (22-28°C during day, 16-20°C during night), the Heater is activated
- When temperature rises above optimal range, the Cooling Fan is activated
- The controller monitors temperature readings and automatically adjusts these actuators

### 2. Humidity Control System
**Sensors:**
- Humidity Sensor (`sensors/humidity_sensor.py`)

**Actuators:**
- Humidifier (`actuators/humidifier.py`)
- Dehumidifier (`actuators/dehumidifier.py`)

**Relationship:**
- When humidity drops below optimal range (60-80% during day, 65-85% during night), the Humidifier is activated
- When humidity rises above optimal range, the Dehumidifier is activated
- The controller maintains humidity within the target range for tomato plants

### 3. Soil Moisture Control System
**Sensors:**
- Soil Moisture Sensor (`sensors/soil_moisture_sensor.py`)

**Actuators:**
- Irrigation System (`actuators/irrigation.py`)

**Relationship:**
- When soil moisture drops below optimal range (40-60%), the Irrigation System is activated
- The soil moisture sensor has special logic to maintain readings within optimal range when irrigation is active
- The controller ensures plants receive adequate water without overwatering

### 4. Light Control System
**Sensors:**
- Light Sensor (`sensors/light_sensor.py`)

**Actuators:**
- Grow Lights (`actuators/lights.py`)

**Relationship:**
- During night mode or low light conditions, Grow Lights are activated to maintain optimal light intensity (600-1000 lux during day, 0-50 lux during night)
- The controller adjusts light levels based on time of day and natural light availability

### 5. CO2 Control System
**Sensors:**
- CO2 Sensor (`sensors/co2_sensor.py`)

**Actuators:**
- CO2 Injector (`actuators/co2_injector.py`)

**Relationship:**
- When CO2 levels drop below optimal range (350-800 ppm during day, 300-500 ppm during night), the CO2 Injector is activated
- The controller maintains CO2 levels to promote photosynthesis

### 6. Nutrient Control System
**Sensors:**
- Nutrient Sensor (`sensors/nutrient_sensor.py`)
- pH Sensor (`sensors/ph_sensor.py`)

**Actuators:**
- Nutrient Pump (`actuators/nutrient_pump.py`)
- Robot operations (watering, manure application, fertilization)

**Relationship:**
- When nutrient levels drop below optimal range (70-90%), the Nutrient Pump is activated
- The pH sensor monitors soil acidity, which is affected by manure application
- The robot can apply manure and fertilizer to specific zones to boost nutrient levels
- Zone-specific effects are tracked and decay over time

## Zone-Based Operations
The greenhouse is divided into 4 zones (A, B, C, D) where the robot can perform targeted operations:
- Watering: Increases soil moisture in specific zone
- Manure Application: Increases nutrient levels and affects pH in specific zone
- Fertilization: Increases nutrient levels in specific zone

Each zone has its own effect tracking that decays over time (30 seconds initial delay, then 5% decay every 5 seconds).

## Controller Logic
The main controller (`controllers/greenhouse_controller.py`) manages all sensor-actuator relationships:
1. Continuously monitors sensor readings
2. Automatically adjusts actuators to maintain optimal conditions
3. Tracks zone-specific effects from robot operations
4. Manages day/night cycle which affects optimal ranges for all parameters
5. Provides real-time data through the Flask API for the web interface

## Realistic Simulation Features
- Sensors have realistic fluctuation patterns
- Actuators have activation/deactivation timestamps
- Day/night cycle affects optimal ranges for all parameters
- Zone-specific effects with decay over time
- Integration with RX200 robot for targeted operations
