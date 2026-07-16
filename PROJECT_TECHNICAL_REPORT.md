# A Simulated Smart Greenhouse Control System for Elderly Farmers with ROS-Based Robotic Assistance

**Comprehensive Technical Report — Master's-Level Submission Documentation**

**Companion / Testbed Project — Linked to Multispectral Imaging Thesis Work**

Project codename: **VNU** (`VNU_Project/VNU`)
Report prepared: 2026-07-16

---

## How to Read This Document

This report documents **exactly what exists in this project folder today**, derived by reading every source file (`app.py`, `controllers/greenhouse_controller.py`, all seven sensor modules, all eight actuator modules, the ROS robot simulation, the frontend JavaScript, the HTML template, and the project's own existing `Project_Report.tex`). It is written so that it can be dropped into a thesis appendix or used as a standalone technical report chapter.

**Important scope note up front:** this folder does **not** contain any multispectral imaging, hyperspectral analysis, or computer-vision code. It is a **greenhouse environmental control and robotics simulation** (a Flask web app + Python "digital twin" of sensors/actuators + a simulated ROS robotic arm + a voice UI). If this project is linked to a multispectral-imaging thesis, the honest and defensible framing — and the one used throughout this report — is that **this project is the control/automation/robotics testbed that a multispectral plant-health-sensing module would eventually plug into**, not that it already performs multispectral analysis. Section 11 ("Relationship to the Multispectral Thesis") lays out exactly where that integration point is and what would need to be built to connect the two. Do not present this report as containing multispectral results unless that integration is actually implemented — a committee will ask to see the code.

---

## Table of Contents

1. Executive Summary
2. Problem Statement and Motivation
3. Project Objectives and Scope
4. High-Level System Architecture
5. Repository / File Structure
6. Technology Stack
7. The Simulated Environment — Sensors
8. The Simulated Environment — Actuators
9. The Robotic Subsystem (RX200 / ROS Simulation)
10. The Controller — Core Orchestration Logic
11. The REST API Layer (Flask)
12. The Frontend — UI and State Rendering
13. The Voice Command System (Web Speech API)
14. Algorithms — Full Formal Treatment
15. Data Flow — End-to-End Request Lifecycle
16. Concurrency Model (Threading)
17. Critical Engineering Finding: The "Closed-Loop" Claim vs. Actual Implementation
18. Design Patterns and Software Engineering Practices
19. Testing Strategy
20. Known Limitations
21. Relationship to the Multispectral Thesis (Integration Roadmap)
22. Future Work
23. Conclusion
24. Appendix A — Full REST API Reference
25. Appendix B — Sensor Range Reference Table
26. Appendix C — Glossary

---

## 1. Executive Summary

This project is a **software-only simulation** ("digital twin") of a smart greenhouse designed to demonstrate how automation, robotics, and voice-based human-computer interaction can reduce the physical and cognitive burden of greenhouse management for elderly farmers. It targets tomato cultivation as its reference crop.

The system is implemented as a **Flask web application** that serves a single-page dashboard. Behind that dashboard sits a **`GreenhouseController`** object that owns seven simulated environmental sensors, eight simulated actuators, and one simulated ROS robotic arm (an "RX200" 4-DOF style arm). The frontend polls a REST API every two seconds to refresh sensor readings, actuator states, and robot position, and can also drive the same API through browser-native speech recognition and speech synthesis (the Web Speech API), so the whole system can be operated by voice.

There is no physical hardware, no real ROS installation, and no real network of IoT sensors — everything is generated in-process by Python classes using bounded random-walk logic. This is explicitly and repeatedly stated as a design choice in the project's own `Project_Report.tex`, and this report preserves that honesty.

## 2. Problem Statement and Motivation

Global agriculture is aging: a large and increasing share of the farming workforce is elderly, while the physical demands of greenhouse operation (watering, monitoring multiple environmental variables, adjusting equipment) remain largely unchanged. Four specific pain points motivate the design:

- **Physical strain** — manual watering, ventilation adjustment, and fertilizing are physically taxing.
- **Constant monitoring burden** — a greenhouse has many interacting variables (temperature, humidity, soil moisture, light, CO₂, pH, nutrients) that must be watched continuously.
- **Cognitive load** — knowing what the "correct" range for each variable is, and what to do when it drifts, requires domain expertise.
- **Interface inaccessibility** — most commercial smart-greenhouse dashboards are built for tech-fluent commercial operators, not elderly hobbyist/smallholder farmers.

The system responds to these four pressures with, respectively: (1) a robotic arm that can perform watering/fertilizing/manure tasks on command, (2) a live dashboard that surfaces every parameter in one place, (3) simplified optimal-range framing baked into the simulation, and (4) a voice interface that removes the need to navigate a complex UI.

## 3. Project Objectives and Scope

Stated objectives (from the project's own design docs, verified against the implementation):

1. Build a realistic software simulation of a greenhouse's environmental sensors.
2. Implement actuator control that can respond to that environment (see Section 17 for an important caveat on how "automatic" this currently is).
3. Integrate a simulated ROS-based robotic arm capable of zone-targeted tasks.
4. Provide an accessible, web-based dashboard.
5. Provide a voice command layer for both input (speech-to-text) and output (text-to-speech).

**Scope boundaries** (explicit, by design):

- Everything is software simulation — there is no physical sensor, actuator, or robot anywhere in this codebase.
- The reference crop is tomato, and the coded optimal ranges (Section 8/Appendix B) reflect tomato-growing literature values, not a general-purpose crop model.
- The "ROS" robot is a plain Python class (`ros_simulation/rx200_robot.py`) that mimics ROS-style state/behavior; it does not use `rospy`, ROS topics, nodes, or any actual ROS middleware. `requirements.txt` confirms this — it lists only `flask`, `numpy`, `pandas`, `matplotlib`, `requests`.
- Voice control depends on the client browser implementing the (non-standardized, Chromium-centric) Web Speech API.

## 4. High-Level System Architecture

The system is organized into four architectural layers, communicating strictly through well-defined interfaces:

```
┌───────────────────────────────────────────────────────────────┐
│  Layer 1 — Client (Browser)                                    │
│  templates/index.html + static/js/app.js + static/css/style.css│
│  • Renders dashboard (sensor cards, actuator toggles, robot)   │
│  • Polls REST API every 2s (setInterval)                       │
│  • Web Speech API: SpeechRecognition (STT) + SpeechSynthesis   │
│    (TTS) for voice command input/output                        │
└───────────────────────────────────┬───────────────────────────┘
                                     │ HTTP (fetch, JSON)
┌───────────────────────────────────▼───────────────────────────┐
│  Layer 2 — Web/API Layer (Flask)                                │
│  app.py                                                          │
│  • Serves index.html                                             │
│  • Exposes 7 REST endpoints (GET/POST, JSON in/out)             │
│  • Translates HTTP requests into GreenhouseController calls      │
└───────────────────────────────────┬───────────────────────────┘
                                     │ direct Python method calls
┌───────────────────────────────────▼───────────────────────────┐
│  Layer 3 — Orchestration / Domain Logic                         │
│  controllers/greenhouse_controller.py — GreenhouseController     │
│  • Single object instantiated once at process start (app.py:20) │
│  • Owns every sensor, actuator, and the robot                    │
│  • Holds day/night state and per-zone effect state               │
│  • Exposes a facade of high-level operations to app.py           │
└───────┬───────────────────────────┬──────────────────┬─────────┘
        │                           │                  │
┌───────▼────────┐         ┌────────▼────────┐  ┌──────▼─────────┐
│ Layer 4a        │         │ Layer 4b         │  │ Layer 4c        │
│ Sensors (7)      │         │ Actuators (8)     │  │ RX200 Robot      │
│ sensors/*.py     │         │ actuators/*.py    │  │ ros_simulation/  │
│ Stateful random-  │         │ Stateful on/off   │  │ rx200_robot.py   │
│ walk generators   │         │ state machines     │  │ Zone navigation, │
│                   │         │                    │  │ task simulation, │
│                   │         │                    │  │ battery drain     │
└──────────────────┘         └───────────────────┘  └─────────────────┘
```

This is a **layered / loosely-MVC** architecture:

- **Model** ≈ the sensor, actuator, and robot classes plus the controller's state (`zone_effects`, `is_day`, etc.)
- **View** ≈ `templates/index.html` + the DOM manipulation in `app.js`
- **Controller** ≈ both the Flask route functions in `app.py` *and* the `GreenhouseController` class — the naming is slightly overloaded relative to classic MVC, since Flask's routing layer is itself sometimes called a "controller" in web-framework parlance. In this codebase, `app.py` is the thin HTTP-to-domain adapter, and `GreenhouseController` is the actual domain/business-logic controller.

Two diagram source files exist in the repo and were authored as Mermaid graphs, reproduced here for completeness:

**System Architecture** (`System_Architecture_Diagram.md`): Browser UI + Voice Interface → Flask REST API → Greenhouse Controller → {Sensors, Actuators, ROS Simulation}, with state/data flowing back up the same chain as a JSON response.

**Temperature Control Loop** (`Temperature_Control_Loop_Diagram.md`): Temperature (environment) → measured by Temperature Sensor → reading compared against an Optimal Range/Setpoint → Controller decision → Heater (if too low) or Cooling Fan (if too high) → actuator acts back on the environment, closing the loop. **This diagram describes the intended design.** Section 17 documents that the *implemented* code does not currently execute this comparison-and-decide step automatically — this is the single most important engineering finding in this report.

## 5. Repository / File Structure

```
GREEN HOUSE PROJECT/
├── VNU_PDF_REPORT_DOCX.docx / .pdf         # Pre-existing generated report exports
├── Similarity-VNU_PDF_REPORT_DOCX.pdf      # Plagiarism/similarity report export
├── VNU_Project.zip                         # Archived copy of the project
└── VNU_Project/VNU/                        # Actual application source
    ├── app.py                              # Flask entrypoint, REST routes
    ├── requirements.txt                    # flask, numpy, pandas, matplotlib, requests
    ├── Project_Report.tex                  # Existing LaTeX thesis-style report
    ├── README.md                           # User-facing feature/usage documentation
    ├── SENSOR_ACTUATOR_RELATIONSHIPS.md    # Design doc: sensor↔actuator pairing rules
    ├── System_Architecture_Diagram.md      # Mermaid architecture diagram source
    ├── Temperature_Control_Loop_Diagram.md # Mermaid control-loop diagram source
    ├── controllers/
    │   ├── __init__.py
    │   └── greenhouse_controller.py        # GreenhouseController — the domain core
    ├── sensors/
    │   ├── temperature_sensor.py
    │   ├── humidity_sensor.py
    │   ├── soil_moisture_sensor.py
    │   ├── light_sensor.py
    │   ├── co2_sensor.py
    │   ├── ph_sensor.py
    │   └── nutrient_sensor.py
    ├── actuators/
    │   ├── heater.py
    │   ├── cooling_fan.py
    │   ├── humidifier.py
    │   ├── dehumidifier.py
    │   ├── irrigation.py
    │   ├── lights.py
    │   ├── co2_injector.py
    │   └── nutrient_pump.py
    ├── ros_simulation/
    │   └── rx200_robot.py                  # Simulated RX200 arm / robot state machine
    ├── static/
    │   ├── css/style.css                   # Day/night theming, layout styling
    │   └── js/app.js                       # Frontend logic, polling, voice commands
    └── templates/
        └── index.html                      # Single-page dashboard (Jinja2 template)
```

Every `sensors/` and `actuators/` module also ships a `__pycache__/` compiled bytecode directory (Python 3.13), confirming the project has actually been executed locally, and each module has a `if __name__ == "__main__":` self-test block that exercises its own class in isolation — a lightweight substitute for a formal unit test suite (see Section 19).

## 6. Technology Stack

| Layer | Technology | Version (pinned in `requirements.txt`) | Role |
|---|---|---|---|
| Backend web framework | Flask | 2.3.2 | HTTP server, routing, templating, JSON responses |
| Backend language | Python | 3.13 (per compiled `.pyc` tags) | All simulation and domain logic |
| Numerical/data libs | NumPy, Pandas, Matplotlib | 1.24.3 / 2.0.3 / 3.7.1 | Declared as dependencies; not directly imported in the core modules reviewed — likely reserved for offline analysis/plotting of simulation data, or a leftover from an earlier iteration |
| HTTP client lib | Requests | 2.31.0 | Declared dependency, not used inside the reviewed backend code path (backend only *serves* HTTP, it doesn't call out) |
| Frontend markup/styling | HTML5, CSS3, Bootstrap 5.3.0 (CDN) | — | Page layout and components |
| Frontend icons | Font Awesome 6.0.0 (CDN) | — | Sun/moon/robot/mic icons etc. |
| Frontend scripting | Vanilla JavaScript (ES6 class syntax) | — | `GreenhouseApp` class drives all client logic; no framework (no React/Vue/Angular) |
| Voice I/O | Web Speech API (`SpeechRecognition`, `SpeechSynthesis`) | Browser-native | STT for commands, TTS for spoken feedback |
| Robotics abstraction | Custom Python simulation (`enum.Enum`-based state machine) | — | Stands in for a real ROS 1/2 node; **no actual ROS dependency** |
| Concurrency | Python `threading` module | — | Background daemon threads for sensor loop, battery drain, and zone-effect decay |
| Persistence | None | — | All state is in-memory; restarting the Flask process resets the entire simulation |

## 7. The Simulated Environment — Sensors

All seven sensor classes live in `sensors/` and follow an identical structural pattern:

- Constructor takes a `sensor_id` and an `initial_<value>`, sets `is_active = True`, records `last_update`.
- A `read_<value>(...)` method returns the *current* simulated reading, having first nudged it by a small random increment (a **bounded random walk**, not an independent-sample-per-call model — see Section 14.1 for the formal algorithm).
- `calibrate(reference_value)` hard-resets the internal state to a given value.
- `get_status()` returns a JSON-serializable dict.
- `activate()` / `deactivate()` toggle `is_active`; when inactive, `read_*()` returns `None`.

| Sensor | File | Day range | Night range | Per-call fluctuation | Special behavior |
|---|---|---|---|---|---|
| Temperature | `temperature_sensor.py` | 22–28 °C | 16–20 °C | `uniform(-0.5, +0.5)` °C | Clamped hard to the active range every call |
| Humidity | `humidity_sensor.py` | 60–80 % | 65–85 % | `uniform(-1.0, +1.0)` % | Clamped hard to the active range every call |
| Soil Moisture | `soil_moisture_sensor.py` | 40–60 % ("optimal") | — (no day/night split) | `uniform(-0.5, +0.2)` % (net downward drift = evaporation) | Three modes: (a) `irrigation_active=True` → clamp to 40–60 %; (b) `is_optimal=True` → clamp to 40–60 %; (c) default → clamp to a floor of 20 % but **no ceiling below 100 %**, allowing it to dry out |
| Light Intensity | `light_sensor.py` | 20,000–50,000 lux | 10–50 lux | `uniform(-20, +20)` lux | Large day/night gap models sunlight vs. artificial/ambient light |
| CO₂ | `co2_sensor.py` | 350–800 ppm | 300–500 ppm | `uniform(-10, +10)` ppm | — |
| pH | `ph_sensor.py` | 5.5–7.5 (no day/night split) | — | `uniform(-0.05, +0.05)` | Narrowest relative fluctuation of all sensors, modeling pH's physical stability |
| Nutrient Level | `nutrient_sensor.py` | 0–100 % (no day/night split) | — | `uniform(-0.3, +0.1)` % (net downward = consumption) | `is_optimal=True` clamps to 70–90 %; default mode floors at 1 % (never literally zero) |

Note on the README's advertised ranges: the README states `Light Intensity: 600-1000 lux (day) / 0-50 lux (night)`, but the actual `light_sensor.py` code uses `20000–50000` lux for day. This is a **documentation/code mismatch** worth calling out explicitly in a report — the README was evidently written against an earlier version of the sensor ranges and never updated. All numeric values in this report and its appendix table are taken from the source code, which is authoritative over the README.

## 8. The Simulated Environment — Actuators

All eight actuator classes (`heater.py`, `cooling_fan.py`, `humidifier.py`, `dehumidifier.py`, `irrigation.py`, `lights.py`, `co2_injector.py`, `nutrient_pump.py`) are **structurally identical state machines** — verified by direct inspection of `heater.py`, `cooling_fan.py`, `irrigation.py`, and `lights.py`, which are byte-for-byte the same pattern with only naming and the "intensity" attribute name changed (`power_level`, `speed_level`, `flow_rate`, `brightness_level`, etc.):

```python
class <Actuator>:
    def __init__(self, actuator_id="..."):
        self.is_on = False
        self.<intensity_attr> = 0          # 0-100, semantics vary by actuator
        self.last_activation = None
        self.last_deactivation = None

    def turn_on(self, <intensity_attr>=100):
        self.is_on = True
        self.<intensity_attr> = clamp(<intensity_attr>, 0, 100)
        self.last_activation = datetime.now()
        return True

    def turn_off(self):
        self.is_on = False
        self.<intensity_attr> = 0
        self.last_deactivation = datetime.now()
        return True

    def set_<intensity_attr>(self, value):
        if self.is_on:
            self.<intensity_attr> = clamp(value, 0, 100)
            return True
        return False

    def get_status(self) -> dict: ...
```

Actuators carry **no decision logic of their own** — they do not know what the "correct" state is; they are dumb, clamp-bounded on/off relays with an intensity dial. All decision-making about *when* to flip an actuator is meant to live in `GreenhouseController` (see Section 17 for the finding that this decision logic is largely absent in the current code).

| Actuator | Intensity attribute | Paired sensor(s) (by design intent, per `SENSOR_ACTUATOR_RELATIONSHIPS.md`) |
|---|---|---|
| Heater | `power_level` | Temperature (low) |
| Cooling Fan | `speed_level` | Temperature (high) |
| Humidifier | (same pattern) | Humidity (low) |
| Dehumidifier | (same pattern) | Humidity (high) |
| Irrigation | `flow_rate` | Soil Moisture (low) — the one actuator whose effect **is** actually wired back into a sensor: `soil_moisture_sensor.read_moisture(irrigation_active=...)` reads `self.irrigation.is_on` in `greenhouse_controller.py` |
| Grow Lights | `brightness_level` | Light Intensity (low / night) |
| CO₂ Injector | (same pattern) | CO₂ (low) |
| Nutrient Pump | (same pattern) | Nutrient Level (low) |

## 9. The Robotic Subsystem (RX200 / ROS Simulation)

`ros_simulation/rx200_robot.py` defines `RX200Robot`, a stand-in for a ROS-driven robotic arm/mobile unit operating across four fixed greenhouse zones.

**State model** — an `enum.Enum` called `RobotState`: `IDLE`, `MOVING`, `WATERING`, `APPLYING_MANURE`, `APPLYING_FERTILIZER`.

**Spatial model** — a fixed lookup table of zone → (x, y) coordinates:
```python
zone_coordinates = {"A": (10, 10), "B": (10, 30), "C": (30, 10), "D": (30, 30)}
```
This is a **discrete zone graph**, not continuous path planning — the robot does not compute a trajectory between coordinates; it "teleports" logically to the target zone after a fixed simulated delay.

**Core operations**, all following the same pattern (validate zone → check `is_active` → set state → `time.sleep(duration * 0.1)` to simulate elapsed work time → reset to `IDLE` → record `last_operation` with an ISO-8601 timestamp):

| Operation | Simulated duration (real seconds elapsed, scaled ×0.1) | Auto-navigates first? |
|---|---|---|
| `move_to_zone(zone)` | 2 → 0.2s | N/A (this *is* the navigation) |
| `water_zone(zone)` | 3 → 0.3s | Yes — calls `move_to_zone` first if not already there |
| `apply_manure(zone)` | 4 → 0.4s | Yes |
| `apply_fertilizer(zone)` | 3 → 0.3s | Yes |

**Battery model** — a background daemon thread (`_simulate_battery_drain`) wakes every 10 real seconds and decrements `battery_level` by 0.1 if the robot is mid-operation, or 0.05 if idle, floored at 0. `charge_battery()` instantly restores it to 100.0 after a 0.5s simulated delay. There is no code path that triggers charging automatically when battery is low, nor any behavior change (e.g., refusing tasks) when battery reaches 0 — `is_active`/state checks are independent of `battery_level`. This is a simulated telemetry value for UI display purposes rather than a functional constraint.

**Invalid input handling** — `move_to_zone`, `water_zone`, `apply_manure`, and `apply_fertilizer` all raise `ValueError` for a zone key not present in `zone_coordinates`; the calling layer (`GreenhouseController`) catches this and converts it into a `(False, error_message)` tuple, which `app.py` in turn serializes into a JSON error response (Section 11).

## 10. The Controller — Core Orchestration Logic

`controllers/greenhouse_controller.py::GreenhouseController` is instantiated exactly once, at Flask app import time (`app.py`, line 20: `controller = GreenhouseController()`), making it a **de facto process-wide singleton** (not enforced by a singleton pattern/metaclass — just by the fact that only one instance is ever constructed in the running application).

**Responsibilities:**

1. **Composition root** — constructs and owns all 7 sensors, 8 actuators, and the 1 robot as instance attributes.
2. **Global simulation state** — `is_day` (bool), `day_start=6`, `day_end=18` (declared but not used to auto-derive `is_day`; day/night is only ever changed by the explicit `toggle_day_night()` call, never by wall-clock time).
3. **Zone-effect ledger** — `zone_effects`, a dict keyed `A`–`D`, each holding `{"watering": 0, "manure": 0, "fertilizer": 0}` — an integer 0–100 "recency/intensity" score per effect type per zone.
4. **Facade methods** consumed by `app.py`: `get_all_sensor_data`, `get_zone_specific_data`, `get_all_actuator_status`, `toggle_actuator`, `move_robot_to_zone`, `water_zone`, `apply_manure_to_zone`, `apply_fertilizer_to_zone`, `toggle_day_night`, `get_complete_status`.
5. **A background daemon thread**, `_update_sensors_continuously`, that wakes every 2 seconds and does — literally, per the source — nothing (`pass`), since sensor state is instead lazily recomputed on-demand inside each sensor's own `read_*` call whenever `get_all_sensor_data`/`get_zone_specific_data` is invoked by an incoming HTTP request. This thread is effectively a no-op placeholder in the current implementation.

**Zone-specific sensor blending (`get_zone_specific_data`)** — this is the most algorithmically interesting method in the controller. It starts from the same global sensor readings every zone would get, then *overlays* zone-local boosts:

- If `zone_effects[zone]["watering"] > 0`: re-reads soil moisture in `is_optimal=True` mode (forcing it into 40–60 %), then adds an **extra boost** of up to +20 %: `boost = (watering / 100.0) * 20`, clamped so the result never exceeds 60 %.
- If `fertilizer > 0` or `manure > 0`: re-reads nutrient level in `is_optimal=True` mode (forcing 70–90 %), then adds a combined boost: `fertilizer_boost = (fertilizer/100)*20` plus `manure_boost = (manure/100)*15`, summed, clamped to a ceiling of 90 %.
- If `manure > 0`: pH gets a boost of `(manure/100) * 0.8`, clamped to the 6.0–6.8 window.

This means the four zones are **not independent simulations** — three of the seven sensor readings (temperature, humidity, light, CO₂) are shared globally across all zones every polling cycle, while soil moisture, nutrient level, and pH are zone-specific overlays computed on top of that shared baseline. This is a deliberate simplification appropriate for a UI-demonstration simulation, not a spatial/CFD-accurate microclimate model.

**Effect decay (`_decay_effect`)** — every time a zone operation succeeds, the controller spawns a new daemon thread that: sleeps 30 seconds (a "grace period" where the boost stays at full strength), then loops decrementing that effect by 5 every 5 seconds until it reaches 0. Multiple operations on the same zone/effect within the 30s grace window simply re-add to the existing value (capped at 100 via `min(100, ...)`) — the decay thread does **not** get cancelled or reset, so calling `water_zone("A")` twice in quick succession can spawn two concurrent decay threads racing on the same dict value (see Section 16 for the concurrency implication).

## 11. The REST API Layer (Flask)

`app.py` is intentionally thin — every route does input validation → delegate to `controller` → wrap result in `jsonify(...)` → catch-all `except Exception` returning HTTP 500 with an error payload. Full reference in Appendix A. Summary:

| Method | Path | Body | Delegates to |
|---|---|---|---|
| GET | `/` | — | Renders `templates/index.html` |
| GET | `/api/data` | — | `robot.get_status()`, `get_zone_specific_data()` for every zone, `get_complete_status()` — merged into one payload |
| POST | `/api/toggle_actuator` | `{"actuator": "<name>"}` | `controller.toggle_actuator(name)` |
| POST | `/api/toggle_day_night` | — | `controller.toggle_day_night()` |
| POST | `/api/move_robot` | `{"zone": "<A-D>"}` | `controller.move_robot_to_zone(zone)` |
| POST | `/api/water_zone` | `{"zone": "<A-D>"}` | `controller.water_zone(zone)` |
| POST | `/api/manure_zone` | `{"zone": "<A-D>"}` | `controller.apply_manure_to_zone(zone)` |
| POST | `/api/fertilize_zone` | `{"zone": "<A-D>"}` | `controller.apply_fertilizer_to_zone(zone)` |

`GET /api/data` is worth expanding since it's the single most-called endpoint (every 2 seconds from three separate frontend polling calls — see Section 12): it first asks the robot for its current zone, fetches that zone's blended sensor readings, fetches the full system status (`sensors`/`actuators`/`robot`/`settings`/`zone_effects`), overwrites the `sensors` key with the current-zone-blended values, and *additionally* attaches a `zone_sensors` map with blended readings for **all four zones at once** (used by the frontend to highlight the active zone — see `updateZoneSensors` in Section 12).

No authentication, no CSRF protection, no rate limiting, and no input schema validation beyond a presence check (`if not actuator: return 400`) exist anywhere in this API layer — appropriate for a local single-user demo, not for any kind of exposed/multi-tenant deployment.

## 12. The Frontend — UI and State Rendering

`templates/index.html` is a Jinja2 template rendering a Bootstrap 5 three-column layout:

- **Left sidebar** — `#sensorValues` (live readings) and a 4-button zone-selector (`#zone-A..D`) that calls `moveRobotToZone`.
- **Center panel** — RX200 status card (position, state) with an animated robot emoji (`#robot-indicator`) whose `top`/`left` CSS percentages are updated per zone via a hardcoded lookup table duplicated in `app.js` (`{'A': {top:'20%',left:'20%'}, 'B': {top:'20%',left:'80%'}, 'C': {top:'80%',left:'20%'}, 'D': {top:'80%',left:'80%'}}`), plus zone-action buttons (`#waterZoneBtn`, `#manureZoneBtn`, `#fertilizeZoneBtn`) that always act on *wherever the robot currently is*, read from the DOM text of `#robotPosition`.
- **Right sidebar** — actuator toggle buttons, rendered dynamically (see below).
- **Top bar** — tomato emoji brand mark, title, and a day/night toggle icon.

`static/js/app.js` defines a single `GreenhouseApp` ES6 class instantiated on `DOMContentLoaded`. Its core loop, `startDataUpdates()`, sets a 2-second `setInterval` that calls three methods in sequence, **each of which independently calls `fetch('/api/data')`**:

```js
this.updateInterval = setInterval(() => {
    this.updateSensorData();      // fetch #1 — sensors + day/night + zone highlighting
    this.updateActuatorControls(); // fetch #2 — actuator button states
    this.updateRobotStatus();      // fetch #3 — robot position/state
}, 2000);
```

This is a notable **inefficiency**: the frontend issues three separate HTTP GET requests to the same idempotent endpoint every 2 seconds instead of one shared fetch reused across the three update functions — functionally correct (each call gets a fresh, consistent snapshot) but triples network/serialization overhead for no benefit, since the underlying data is generated together server-side in a single `get_complete_status()` call. A straightforward optimization would be to fetch once per tick and pass the parsed JSON into all three update functions.

Actuator buttons and sensor cards are rendered via full `innerHTML` replacement on every poll (`renderActuatorControls`, `updateSensors`) rather than incremental DOM diffing — again, simple and correct for this scale, but it means click handlers are re-attached from scratch every 2 seconds (`document.querySelectorAll('.actuator-btn').forEach(...)` inside `renderActuatorControls`).

Day/night mode is applied by toggling a `.night-mode` CSS class across roughly a dozen different selector groups (cards, buttons, labels, zone views, voice feedback panel, etc.) — a manual, enumerated approach rather than a single CSS custom-property/theme-attribute switch, meaning any newly added UI element must be remembered and added to this list to respect the theme.

## 13. The Voice Command System (Web Speech API)

Voice control is entirely client-side — the backend has no awareness that voice was the input source; it only ever sees the resulting REST calls.

**Speech-to-Text pipeline (`startVoiceRecognition`)**:
1. Feature-detect `SpeechRecognition`/`webkitSpeechRecognition`.
2. Configure `continuous = true`, `interimResults = false`, `lang = 'en-US'`.
3. On `onresult`, take the transcript of the *last* result and hand it to `processVoiceCommand`.
4. On `onend`, if the user hasn't explicitly turned voice off, immediately restart recognition — this creates a persistent "always listening while active" loop rather than a single-shot command capture.
5. If the API is unsupported, a fallback path shows an error, speaks an apology via TTS, and auto-cancels the "recording" UI state after a 5-second timer (a demo/graceful-degradation path).

**Command interpretation (`processVoiceCommand`)** is a **keyword substring matcher**, not a real NLU/intent-classification model:

```js
for (const [key, func] of Object.entries(this.voiceCommands)) {
    if (command.includes(key)) {
        const zoneMatch = command.match(/zone ([a-d])/);
        const zone = zoneMatch ? zoneMatch[1] : null;
        ...
        zone ? func(zone) : func();
        return true;
    }
}
```

`this.voiceCommands` is a dictionary of ~20 fixed phrase keys (e.g. `'move to zone'`, `'water zone'`, `'turn on heater'`, `'turn off co2 injector'`) mapped to closures that call the corresponding frontend method. Because `Object.entries` iteration order in modern JS engines follows insertion order, and the check is `command.includes(key)` (first match wins, no ranking), phrase **ordering in the source is load-bearing**: if a shorter/more general key phrase happened to be a substring of a longer one and were listed first, it would shadow the more specific command. In the current list this does not actually occur (all keys are disjoint prefixes), but it is a latent fragility of substring-based dispatch versus a proper intent parser.

A regex `/zone ([a-d])/` extracts the target zone letter from anywhere in the transcript, independent of which command key matched — meaning `"water zone b"` is parsed by finding the `'water zone'` key *and separately* regex-extracting `b` from the same string.

**Text-to-Speech (`speakResponse`)** — feature-detects `speechSynthesis`, wraps the response string in a `SpeechSynthesisUtterance` at rate/pitch/volume all `1.0` (defaults), and speaks it. Every successful command also gets a matching entry in `this.voiceResponses` used purely to generate the spoken confirmation text (e.g. `"Turning on the heater"`) — this text is cosmetic/UX only and does not affect control flow.

## 14. Algorithms — Full Formal Treatment

### 14.1 Sensor Reading Algorithm (Bounded Random Walk)

Every sensor implements the same generic algorithm, parameterized by `(low, high, δ)`:

```
state ← initial_value
function read(is_day):
    (low, high) ← day_range if is_day else night_range
    ε ← uniform_random(-δ, +δ)          # δ differs per sensor, see Section 7 table
    state ← state + ε
    state ← max(low, min(high, state))   # hard clamp — reflects at the boundary
    return round(state, precision)
```

This is a **discrete-time bounded random walk with reflecting boundaries**: rather than clamping producing a "sticking" effect, because ε is resampled independently each call, a value at the boundary has ~50% probability of moving back inward on the very next call — so the simulated series tends to hover near either boundary under sustained drift and wander freely in the interior, which is a reasonably convincing approximation of real sensor noise around a slowly changing physical setpoint. There is no actual physical model (no thermal mass, no PID plant model, no time-of-day interpolation curve) — the day/night ranges are two discrete regimes toggled instantaneously by `is_day`, not a continuous diurnal cycle.

Soil moisture and nutrient level additionally implement **directionally-biased** fluctuation (mean of the uniform range is negative, e.g. `uniform(-0.5, +0.2)` for soil moisture), modeling net consumption/evaporation between replenishment events (irrigation, fertilization) — this is the one piece of physically-motivated asymmetry in an otherwise symmetric-noise design.

### 14.2 Zone Effect Application (Nutrient/Moisture/pH Boost Blending)

For a zone `z` with ledger `{watering, manure, fertilizer} ∈ [0,100]³`:

```
soil_moisture(z)   = clamp( optimal_soil_moisture() + (watering/100)·20,   40, 60 )   if watering > 0
nutrient_level(z)  = clamp( optimal_nutrient_level() + (fertilizer/100)·20
                                                       + (manure/100)·15,  70, 90 )    if fertilizer>0 or manure>0
ph_level(z)        = clamp( ph_reading() + (manure/100)·0.8,               6.0, 6.8 ) if manure > 0
```
where `optimal_soil_moisture()`/`optimal_nutrient_level()` are the sensor's own `is_optimal=True` reads (already pre-clamped to their respective optimal band), so the boost term is added *on top of* an already-in-range base reading and then re-clamped — meaning the boost's practical effect is to push the *displayed* value toward the top of the optimal band rather than ever exceed it. This is a **linear proportional blending model**, not a differential-equation or compartmental nutrient/water-balance model.

### 14.3 Effect Decay Algorithm

```
function decay(zone, effect_type):
    sleep(30)                                    # grace period — value stays at last-set level
    while zone_effects[zone][effect_type] > 0:
        sleep(5)
        zone_effects[zone][effect_type] = max(0, zone_effects[zone][effect_type] - 5)
```
This is a **linear decay with initial dead-time**, run as an independent daemon thread per triggering event (Section 16 covers the resulting race condition when triggered repeatedly).

### 14.4 Robot Task State Machine

```
states = {IDLE, MOVING, WATERING, APPLYING_MANURE, APPLYING_FERTILIZER}
function do_task(task, zone):
    if zone not in zone_coordinates: raise ValueError
    if not is_active: return False
    if current_position != zone:
        state ← MOVING; sleep(0.2); current_position ← zone; state ← IDLE
    state ← task.state_enum
    sleep(task.duration × 0.1)
    state ← IDLE
    last_operation ← {operation: task.name, zone, timestamp: now()}
    return True
```
Every task (`water_zone`, `apply_manure`, `apply_fertilizer`) is thus **compositionally built** on top of `move_to_zone` — a simple but effective example of code reuse over an explicit finite-state machine, implemented with `if`-guards rather than a formal FSM/transition-table library.

### 14.5 Voice Command Dispatch Algorithm

```
function process(transcript):
    transcript ← lowercase(transcript)
    for (key, handler) in voiceCommands (insertion order):
        if transcript.contains(key):
            zone ← first regex match of /zone ([a-d])/ in transcript, or null
            speak(voiceResponses[key](zone))
            zone ? handler(zone) : handler()
            return true
    speak("Sorry, I didn't understand that command.")
    return false
```
First-match, order-dependent, O(n) linear scan over ~20 fixed phrases — adequate at this scale, would not scale to an open-vocabulary command set without a real intent classifier.

## 15. Data Flow — End-to-End Request Lifecycle

Example: a user says **"Water zone B"**.

1. Browser mic captures audio → Web Speech API STT → transcript `"water zone b"` delivered to `recognition.onresult`.
2. `processVoiceCommand("water zone b")` matches key `'water zone'`, regex-extracts zone `b` → uppercased to `"B"`.
3. `speakResponse("Watering zone B")` fires immediately (optimistic — spoken before the server confirms success).
4. `this.waterZone("B")` issues `POST /api/water_zone` with body `{"zone": "B"}`.
5. Flask route `water_zone()` in `app.py` parses the JSON, calls `controller.water_zone("B")`.
6. `GreenhouseController.water_zone("B")` calls `self.robot.water_zone("B")`.
7. `RX200Robot.water_zone("B")`: if not already at B, transitions `IDLE→MOVING→IDLE` (0.2s) to relocate; then `IDLE→WATERING→IDLE` (0.3s); records `last_operation`.
8. Back in the controller: on success, `zone_effects["B"]["watering"] += 20` (capped at 100), and a new decay daemon thread is spawned for `("B", "watering")`.
9. `app.py` wraps the `(True, "Watered zone B")` tuple into `{"success": true, "message": "Watered zone B", "zone": "B"}` and returns HTTP 200.
10. Frontend receives the response, logs the message, and calls `showZoneEffect("B", "water")` — a transient DOM element (a "●" glyph) is animated at zone B's screen coordinates and removed after 2 seconds via `setTimeout`.
11. On the *next* 2-second polling tick (independent of this request), `updateSensorData()` calls `GET /api/data`, which now reflects `zone_effects["B"]["watering"] = 20` and therefore returns a boosted `soil_moisture` reading for zone B if the robot happens to currently be positioned there — the dashboard's headline sensor panel only ever shows the **current-zone** blended reading (Section 11), so the boost is only visibly reflected in the main panel while the robot remains in zone B; the `zone_sensors` map in the same response carries all four zones' figures for any UI element that chooses to display them (used by `updateZoneSensors` purely for CSS zone-highlighting today, not for displaying all four zones' numbers simultaneously).

## 16. Concurrency Model (Threading)

The application relies on Python's `threading` module (green threads under the GIL, not multiprocessing) for three categories of background work, all as **daemon threads** (so they die automatically when the Flask process exits, never block shutdown):

1. **`GreenhouseController._update_sensors_continuously`** — wakes every 2s, currently a no-op (`pass`). Vestigial.
2. **`RX200Robot._simulate_battery_drain`** — wakes every 10s, mutates `battery_level`.
3. **`GreenhouseController._decay_effect`** — one new thread spawned *per successful zone operation*, each independently mutating `zone_effects[zone][effect_type]` over time.

Flask's development server (`app.run(debug=True, ...)`) is itself multi-threaded per request by default in modern Flask, meaning **HTTP request handling threads and these background daemon threads all mutate shared mutable state (`zone_effects`, sensor `current_*` attributes, actuator `is_on`) without any locks, mutexes, or atomic operations**. In CPython, individual dict/attribute writes are effectively atomic under the GIL, so this does not crash, but compound read-modify-write sequences (e.g., `zone_effects[zone][effect_type] = max(0, zone_effects[zone][effect_type] - 5)` racing against `zone_effects[zone]["watering"] = min(100, ... + 20)` from a fresh operation) are **not** atomic as a unit — a rapid double-trigger of `water_zone("A")` can produce two concurrent decay threads for the same `(zone, effect)` key, each independently decrementing, which can decay the value faster than the single-trigger design intends. This is a real, identifiable race condition, though its consequence is cosmetic (a display value decaying slightly faster than designed) rather than a correctness-critical failure.

## 17. Critical Engineering Finding: The "Closed-Loop" Claim vs. Actual Implementation

This is the single most important finding in this report, and the kind of discrepancy a thesis committee or code reviewer would be expected to catch.

**What the documentation claims:**
- `SENSOR_ACTUATOR_RELATIONSHIPS.md`: *"When temperature drops below optimal range... the Heater is activated. When temperature rises above optimal range, the Cooling Fan is activated. The controller monitors temperature readings and automatically adjusts these actuators."* Similar automatic-activation language is written for humidity, CO₂, and nutrients.
- `Temperature_Control_Loop_Diagram.md` draws an explicit closed feedback loop: sensor → compare vs. setpoint → controller decision → heater/fan → acts back on temperature.
- `Project_Report.tex`, Section 3.4 ("Closed-Loop Control Systems"): *"The foundation of the greenhouse's autonomy lies in its array of simulated closed-loop control systems... control strategies are implemented as core logic within the `GreenhouseController`."*

**What the code actually does:** `GreenhouseController` contains no method, branch, or scheduled routine that reads a sensor value, compares it to a threshold, and calls `turn_on()`/`turn_off()` on an actuator as a consequence. The only two ways any actuator's `is_on` state ever changes are:
1. `toggle_actuator()`, invoked exclusively by an explicit `POST /api/toggle_actuator` — i.e., a human clicking a button or speaking a "turn on/off X" voice command.
2. Nothing else — there is no third path.

The `_update_sensors_continuously` background thread (Section 10, item 5), which is the only plausible place such logic could live given its name and 2-second cadence, is an empty `pass` loop.

**The one partial exception** is irrigation → soil moisture, which *is* wired, but in the *opposite direction* of a control loop: the **actuator's state influences the sensor reading** (`soil_moisture_sensor.read_moisture(irrigation_active=self.irrigation.is_on)` forces the reading into the 40–60% optimal band while irrigation is on), rather than the **sensor reading triggering the actuator**. This produces a superficially plausible demo (turn on irrigation, watch soil moisture rise into range) without actually implementing autonomous decision-making — a human still has to turn irrigation on and off.

**Why this matters for a report:** presenting this project as containing "autonomous closed-loop environmental control" without qualification would be inaccurate and could be flagged in an academic review. The accurate characterization is: **the simulation provides all the state and infrastructure a closed-loop controller would need (live sensor values, actuator toggles, optimal-range constants implicitly encoded in each sensor's clamp bounds), but the actual threshold-comparison-and-actuate decision logic has not been implemented — every actuator transition today is either manually triggered via UI or via voice command.** This is not a criticism of the project's value as a proof-of-concept for the UI/robotics/voice layers, which are fully implemented; it is a precise scoping statement that should appear in any report claiming to describe "what the system does," and it is a natural, well-defined next implementation task (see Section 22).

## 18. Design Patterns and Software Engineering Practices

- **Facade pattern** — `GreenhouseController` presents a small, high-level surface (`toggle_actuator`, `water_zone`, `get_complete_status`, etc.) over eight actuator objects, seven sensor objects, and one robot object, so `app.py` never touches a sensor/actuator/robot instance directly.
- **De facto singleton** — one `GreenhouseController` instance for the process lifetime (Section 10), though not enforced structurally (nothing prevents a second instantiation; it simply never happens in this codebase).
- **State pattern (light)** — `RobotState` as an `Enum` driving the robot's behavior/reporting, though transitions are still procedural `if`/assignment rather than a table-driven state machine.
- **Uniform interface convention** — every sensor class exposes the same five-method shape (`read_*`, `calibrate`, `get_status`, `activate`, `deactivate`); every actuator class exposes the same five-method shape (`turn_on`, `turn_off`, `set_*_level`, `get_status`, plus implicit `is_on`). This consistency is what makes the controller's composition code (Section 10) so uniform, and is good practice for a component library even though no formal interface/ABC (`abc.ABC`) is declared to *enforce* the shape.
- **Fail-soft API layer** — every Flask route wraps its body in `try/except Exception as e: return jsonify({"error": str(e)}), 500`, so a bug in domain logic degrades to a JSON error rather than an unhandled server crash/HTML stack trace.
- **Daemon-thread background work** — consistently marked `daemon=True` so background loops never prevent process shutdown (Section 16).
- **Self-testing modules** — every sensor/actuator/robot file ends with an `if __name__ == "__main__":` block exercising the class standalone, which is how the developer likely validated each component in isolation before wiring it into the controller (a lightweight, informal precursor to `pytest`-style unit tests — no actual test framework or assertions are used, only printed output for manual inspection).

## 19. Testing Strategy

As implemented, testing consists entirely of the **manual self-test blocks** described above (Section 18) — there is no `tests/` directory, no `pytest`/`unittest` files, and no CI configuration in the repository. The project's own `Project_Report.tex` (Chapter 5) describes an *intended* testing strategy — unit tests, integration tests for the API, and user-acceptance tests — and lists five representative manual test cases in tabular form (automated temperature control expectation [not actually automatic — see Section 17], manual actuator override via UI, voice-driven robot movement, voice-driven watering with a soil-moisture increase check, and day/night toggling). These read as a **test plan**, not **executed and reported test results** — no pass/fail evidence, screenshots, or logged output accompany them in the repository. Any thesis submission drawing on this report should describe this section as "a defined manual test plan" rather than "a validated test suite," unless such validation is separately performed and evidenced.

## 20. Known Limitations

1. **No real closed-loop automation** (Section 17) — the headline "autonomous control" claim is not yet implemented in code.
2. **No persistence** — every value resets to its constructor default on process restart; there is no database, file, or cache layer.
3. **No authentication/authorization** — any client that can reach the Flask port can control every actuator and robot action.
4. **Global (not per-zone) primary sensors** — temperature, humidity, light, and CO₂ are identical across all four zones; only soil moisture, nutrient level, and pH vary by zone, and even those share a common global baseline (Section 10).
5. **README/code drift** — at minimum, the light sensor's day-mode lux range differs materially between `README.md` (600–1000 lux) and `sensors/light_sensor.py` (20,000–50,000 lux).
6. **Frontend polling inefficiency** — three redundant `fetch('/api/data')` calls per 2-second tick instead of one shared fetch (Section 12).
7. **Unsynchronized shared mutable state** across HTTP request threads and background daemon threads with no locking (Section 16) — low-severity in practice under CPython's GIL, but a latent race condition on `zone_effects`.
8. **No actual ROS dependency** — despite the "ROS-based" framing in the title and report, no `rospy`/ROS 2 client library is imported or required; `requirements.txt` confirms only Flask/NumPy/Pandas/Matplotlib/Requests.
9. **No physical hardware, no field data, no computer vision or multispectral sensing of any kind** — everything is a bounded-random-walk numerical simulation (Section 14.1).
10. **Voice recognition is entirely dependent on browser support** for a non-standard, primarily Chromium-implemented API (Safari support is explicitly called out as "limited" in the README).

## 21. Relationship to the Multispectral Thesis (Integration Roadmap)

This project, as it stands, is a **greenhouse control/automation/HCI/robotics simulation**. It contains **zero** multispectral, hyperspectral, RGB-plant-health, or image-processing code — no camera model, no spectral band simulation, no vegetation-index computation (NDVI, GNDVI, etc.), no image files or datasets referencing plant canopies. If this document is to be cited from or embedded in a multispectral-imaging thesis, the accurate and defensible relationship to describe is one of these two framings, not "this system performs multispectral analysis":

**Framing A — Control testbed / integration target.** This project already supplies the exact scaffolding a multispectral plant-health module needs to plug into: (a) a zone-based spatial model (`zone_coordinates`, four discrete zones) that a camera-equipped scan could be indexed against; (b) a robot with movement primitives (`move_to_zone`) that could be extended with a `capture_multispectral_image(zone)` action, following the same pattern as `water_zone`/`apply_fertilizer`; (c) a REST API and dashboard that could surface a derived vegetation-health index or per-zone spectral summary exactly the way it currently surfaces `nutrient_level` or `ph_level`; and (d) a `GreenhouseController` facade that is the natural place to translate "low NDVI in zone C" into an automated irrigation/fertilizer action — which is precisely the closed-loop decision logic identified as *missing* in Section 17, and which a multispectral health signal would be a compelling, novel input to.

**Framing B — Companion system in a broader thesis narrative.** The thesis's actual multispectral contribution (image acquisition, band selection, index computation, disease/stress classification, etc., which lives outside this folder) is the sensing and diagnosis half of a smart-greenhouse system; this project is the actuation/HCI/robotics half. Presented together, they form a complete sense→decide→act pipeline: multispectral imaging (sense: plant physiological state) → a to-be-implemented decision layer (decide: is intervention needed, in which zone) → this project's actuator/robot layer (act: irrigate, fertilize, adjust climate). Framed this way, this report's job is to precisely document the "act" half so the thesis can correctly scope what is proven versus what remains integration work.

**Concrete integration points if development continues:**
- Add a `sensors/multispectral_camera.py` module returning either simulated or real per-band reflectance/derived-index values, following the existing sensor interface convention (Section 18) so it drops into `GreenhouseController.get_zone_specific_data` with minimal churn.
- Extend `zone_effects` (or a parallel structure) with a per-zone health/stress score derived from that module.
- Implement the missing threshold-comparison logic from Section 17, now driven in part by the multispectral signal rather than only the existing bounded-random-walk sensors.
- Extend `RX200Robot` with an imaging action (analogous to `water_zone`) so the dashboard/voice system can trigger "scan zone C" the same way it triggers "water zone C" today.
- Surface the derived index on the dashboard (`sensorValues` card) and as a new voice command entry in `app.js`'s `voiceCommands` map.

## 22. Future Work

Directly from the project's own `Project_Report.tex`, corroborated as genuinely open (none of these exist in the current code):

1. **Physical prototyping** — replace every simulated sensor/actuator/robot class with a hardware-backed equivalent behind the same interface (Section 18's uniform-interface convention makes this a relatively contained swap).
2. **Predictive control** — ML-based forecasting of environmental drift to pre-emptively actuate rather than react.
3. **Computer vision / multispectral plant-health monitoring** — explicitly named in the source `Project_Report.tex` as future work, and the natural connective tissue to a multispectral thesis (Section 21).
4. **Expanded crop support** — parameterize the currently tomato-hardcoded optimal ranges into a swappable crop profile.
5. **Mobile companion app.**

Additional, code-derived (not previously written down) recommendations from this review:
6. Implement the actual threshold-based auto-control logic described in Section 17 — arguably higher-priority than any of the above, since it is the gap between what the system is documented to do and what it currently does.
7. Reconcile README/code numeric drift (Section 20, item 5).
8. Add a real automated test suite (`pytest`) replacing the manual `__main__` self-test blocks.
9. Add basic auth and input validation before any deployment beyond a local single-user demo.
10. Collapse the frontend's three-fetches-per-tick pattern into one.

## 23. Conclusion

This project is a coherent, well-structured software simulation demonstrating four genuinely integrated subsystems: a Flask REST backend, a set of uniformly-designed simulated sensors and actuators, a simulated ROS-style robotic arm operating over a four-zone spatial model, and a voice-driven accessibility layer built on the browser's native Speech API. The engineering is consistent (a repeated, disciplined class-shape convention across all sensor and actuator modules), the API surface is small and clean, and the zone-effect/decay mechanism shows real algorithmic thought beyond boilerplate CRUD. Its most significant gap, identified precisely in Section 17, is that the "closed-loop autonomous control" described in every piece of project documentation is not actually implemented — actuators today respond only to explicit human/voice commands, not to sensor thresholds. This is a well-scoped, addressable next step rather than a fundamental flaw, and closing it is also the most natural on-ramp for a multispectral-imaging signal to eventually drive real decisions in this system, per the integration roadmap in Section 21. As submitted, this report accurately reflects a control/robotics/HCI simulation testbed, and should not be cited as evidence of implemented multispectral sensing or of implemented autonomous environmental control until those specific gaps are closed in code.

---

## Appendix A — Full REST API Reference

| Endpoint | Method | Request Body | Success Response Shape | Failure Response |
|---|---|---|---|---|
| `/` | GET | — | Rendered HTML page | — |
| `/api/data` | GET | — | `{sensors, actuators, robot, settings, zone_effects, zone_sensors}` | `{"error": "..."}`, 500 |
| `/api/toggle_actuator` | POST | `{"actuator": str}` | `{"success": bool, "message": str}` | `{"success": false, "error": "Actuator name required"}`, 400; or 500 |
| `/api/toggle_day_night` | POST | — | `{"success": true, "is_day": bool, "message": str}` | 500 |
| `/api/move_robot` | POST | `{"zone": "A"|"B"|"C"|"D"}` | `{"success": bool, "message": str}` | `{"success": false, "error": "Zone required"}`, 400; or 500 |
| `/api/water_zone` | POST | `{"zone": str}` | `{"success": bool, "message": str, "zone": str}` | 400/500 |
| `/api/manure_zone` | POST | `{"zone": str}` | `{"success": bool, "message": str, "zone": str}` | 400/500 |
| `/api/fertilize_zone` | POST | `{"zone": str}` | `{"success": bool, "message": str, "zone": str}` | 400/500 |

## Appendix B — Sensor Range Reference Table (authoritative, from source code)

| Parameter | Day Range | Night Range | Optimal-mode Range (where applicable) | Absolute Floor/Ceiling (uncontrolled mode) |
|---|---|---|---|---|
| Temperature | 22–28 °C | 16–20 °C | n/a (day/night range *is* the clamp) | Same as active range |
| Humidity | 60–80 % | 65–85 % | n/a | Same as active range |
| Soil Moisture | 40–60 % (irrigation on / optimal mode) | — | 40–60 % | Floor 20 %, no explicit ceiling below 100 % |
| Light Intensity | 20,000–50,000 lux | 10–50 lux | n/a | Same as active range |
| CO₂ | 350–800 ppm | 300–500 ppm | n/a | Same as active range |
| pH | 5.5–7.5 (no day/night split) | — | n/a | Same as range |
| Nutrient Level | 0–100 % (no day/night split) | — | 70–90 % | Floor 1 % |

## Appendix C — Glossary

- **STT** — Speech-to-Text; **TTS** — Text-to-Speech.
- **RX200** — the name given to the simulated robotic arm/unit in this project (an homage to Interbotix's real RX200 robotic arm product line; no actual hardware SDK is used here).
- **ROS** — Robot Operating System; note this project simulates ROS-style behavior without an actual ROS dependency (Section 20, item 8).
- **Daemon thread** — a background thread that does not prevent process exit; used throughout for sensor/battery/decay loops.
- **Bounded random walk** — the core sensor-simulation algorithm: a running value nudged by small random increments each call, clamped to a fixed range (Section 14.1).
- **Zone-effect ledger** — the `zone_effects` dict tracking watering/manure/fertilizer intensity per zone, decaying over time (Section 14.3).
- **Facade pattern** — a software design pattern where one class exposes a simplified interface over a more complex set of subsystems; used by `GreenhouseController` here.

---

*This report was compiled by direct inspection of every source file in `VNU_Project/VNU/` as of 2026-07-16, cross-referenced against the project's own `README.md`, `SENSOR_ACTUATOR_RELATIONSHIPS.md`, `System_Architecture_Diagram.md`, `Temperature_Control_Loop_Diagram.md`, and `Project_Report.tex`. Where those documents' claims diverged from the actual code, the code was treated as authoritative and the divergence was explicitly flagged (Sections 7, 17, 20) rather than silently reconciled.*
