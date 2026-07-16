from flask import Flask, render_template, jsonify, request
import json
import threading
import time
from datetime import datetime
import os

# Import the greenhouse controller
from controllers.greenhouse_controller import GreenhouseController

# Get the directory of the current file
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(basedir, 'templates'),
            static_folder=os.path.join(basedir, 'static'),
            static_url_path='/static')

# Initialize the greenhouse controller
controller = GreenhouseController()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """Get complete greenhouse data"""
    try:
        # Get robot position to determine which zone data to show
        robot_status = controller.robot.get_status()
        current_zone = robot_status["current_position"]
        
        # Get zone-specific sensor data
        zone_data = controller.get_zone_specific_data(current_zone)
        
        # Get complete status
        complete_status = controller.get_complete_status()
        
        # Update sensor data with zone-specific values
        complete_status["sensors"] = zone_data
        complete_status["zone_sensors"] = {
            zone: controller.get_zone_specific_data(zone) 
            for zone in controller.zone_effects.keys()
        }
        
        return jsonify(complete_status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/toggle_actuator', methods=['POST'])
def toggle_actuator():
    """Toggle an actuator on/off"""
    try:
        data = request.get_json()
        actuator = data.get('actuator')
        
        if not actuator:
            return jsonify({"success": False, "error": "Actuator name required"}), 400
            
        success, message = controller.toggle_actuator(actuator)
        return jsonify({"success": success, "message": message})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/toggle_day_night', methods=['POST'])
def toggle_day_night():
    """Toggle between day and night mode"""
    try:
        is_day, message = controller.toggle_day_night()
        return jsonify({"success": True, "is_day": is_day, "message": message})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/move_robot', methods=['POST'])
def move_robot():
    """Move robot to a specific zone"""
    try:
        data = request.get_json()
        zone = data.get('zone')
        
        if not zone:
            return jsonify({"success": False, "error": "Zone required"}), 400
            
        success, message = controller.move_robot_to_zone(zone)
        return jsonify({"success": success, "message": message})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/water_zone', methods=['POST'])
def water_zone():
    """Water a specific zone"""
    try:
        data = request.get_json()
        zone = data.get('zone')
        
        if not zone:
            return jsonify({"success": False, "error": "Zone required"}), 400
            
        success, message = controller.water_zone(zone)
        return jsonify({"success": success, "message": message, "zone": zone})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/manure_zone', methods=['POST'])
def manure_zone():
    """Apply manure to a specific zone"""
    try:
        data = request.get_json()
        zone = data.get('zone')
        
        if not zone:
            return jsonify({"success": False, "error": "Zone required"}), 400
            
        success, message = controller.apply_manure_to_zone(zone)
        return jsonify({"success": success, "message": message, "zone": zone})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/fertilize_zone', methods=['POST'])
def fertilize_zone():
    """Apply fertilizer to a specific zone"""
    try:
        data = request.get_json()
        zone = data.get('zone')
        
        if not zone:
            return jsonify({"success": False, "error": "Zone required"}), 400
            
        success, message = controller.apply_fertilizer_to_zone(zone)
        return jsonify({"success": success, "message": message, "zone": zone})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
