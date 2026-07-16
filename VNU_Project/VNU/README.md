# Smart Greenhouse for Elderly Farmers with ROS

A comprehensive greenhouse simulation system designed for elderly farmers with realistic sensor values, actuator controls, and voice command functionality.

## Features

### Realistic Sensor Simulation
- **Temperature**: 22-28°C (day) / 16-20°C (night)
- **Humidity**: 60-80% (day) / 65-85% (night)
- **Soil Moisture**: 40-60% (day) / 35-55% (night)
- **Light Intensity**: 600-1000 lux (day) / 0-50 lux (night)
- **CO2 Level**: 350-800 ppm (day) / 300-500 ppm (night)
- **pH Level**: 6.0-6.8
- **Nutrient Level**: 70-90% (day) / 65-85% (night)

### Actuator Controls
- Heater
- Cooling Fan
- Humidifier
- Dehumidifier
- Irrigation System
- Grow Lights
- CO2 Injector
- Nutrient Pump

### Voice Command System
- Web Speech API integration for voice recognition
- Text-to-speech feedback for system responses
- Visual feedback display for voice commands

### Robot Control (RX200 Simulation)
- Zone-based navigation (A, B, C, D)
- Animated robot movement between zones
- Watering, fertilizing, and manure application

### Day/Night Cycle
- Toggle between day and night modes
- Automatic sensor value adjustments
- Visual theme changes

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd smart-greenhouse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application at `http://localhost:5000`

## Usage

### Web Interface
- **Left Sidebar**: Live sensor values with optimal ranges
- **Center Panel**: Robot status and greenhouse layout with animated robot
- **Right Sidebar**: Actuator controls with toggle buttons
- **Top Bar**: Green title bar with tomato emoji and day/night toggle

### Voice Commands
Click the microphone icon to activate voice control, then say commands like:
- "Move to zone A"
- "Water zone B"
- "Apply manure to zone C"
- "Fertilize zone D"
- "Toggle day night"
- "Turn on heater"
- "Turn off lights"

### Actuator Controls
Each actuator button toggles between green (on) and grey (off) states:
- Heater
- Cooling Fan
- Humidifier
- Dehumidifier
- Irrigation
- Grow Lights
- CO2 Injector
- Nutrient Pump

## Technical Implementation

### Backend (Flask)
- Real-time sensor simulation with realistic value ranges
- Actuator state management
- Robot position tracking
- RESTful API endpoints

### Frontend (JavaScript/HTML/CSS)
- Dynamic sensor value updates
- Animated robot movement between zones
- Web Speech API integration
- Responsive design with day/night themes
- Visual feedback for all interactions

### ROS Integration
- RX200 robot simulation
- Zone-based navigation system
- Task execution for watering, fertilizing, and manure application

## API Endpoints

- `GET /api/data` - Retrieve current sensor, actuator, and robot data
- `POST /api/toggle_actuator` - Toggle actuator state
- `POST /api/toggle_day_night` - Toggle day/night mode
- `POST /api/move_robot` - Move robot to specified zone
- `POST /api/water_zone` - Water specified zone
- `POST /api/manure_zone` - Apply manure to specified zone
- `POST /api/fertilize_zone` - Fertilize specified zone

## Browser Support

Voice recognition features require a modern browser that supports the Web Speech API:
- Google Chrome (recommended)
- Microsoft Edge
- Safari (limited support)

## Development

### Project Structure
```
smart-greenhouse/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── actuators/          # Actuator classes
├── controllers/        # Controller classes
├── ros_simulation/      # ROS simulation classes
├── sensors/            # Sensor classes
├── static/
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript files
└── templates/          # HTML templates
```

### Customization
- Adjust sensor ranges in `app.py`
- Modify actuator behavior in respective actuator files
- Update UI styling in `static/css/style.css`
- Extend voice commands in `static/js/app.js`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
