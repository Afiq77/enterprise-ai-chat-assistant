# app/vehicle_formatter.py

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut
import requests
from datetime import datetime

geolocator = Nominatim(user_agent="vehicle-formatter")

def reverse_geocode(lat: float, lng: float) -> str:
    try:
        location = geolocator.reverse((lat, lng), exactly_one=True, language="en")
        return location.address if location else "Location unavailable"
    except (GeocoderUnavailable, GeocoderTimedOut):
        return "Location unavailable"

def angle_to_direction(angle):
    if angle is None:
        return "Unknown"
    directions = ["North", "North-East", "East", "South-East",
                  "South", "South-West", "West", "North-West"]
    idx = int((angle + 22.5) % 360 / 45)
    return directions[idx]

def get_weather_data(lat, lon, days=1):
    try:
        if days > 1:
            url = f"http://api.weatherapi.com/v1/forecast.json?key=YOUR_API_KEY&q={lat},{lon}&days={days}&aqi=no&alerts=yes"
        else:
            url = f"http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q={lat},{lon}&aqi=no"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'location' not in data or 'current' not in data:
            return None

        return data
    except Exception:
        return None

def format_vehicle_data(vehicle: dict, section: str = "all") -> str:
    name = vehicle.get('name', 'Unknown')
    last_update = vehicle.get("last_update", {}) or {}
    chPrams = last_update.get("chPrams", {}) or {}
    driver = vehicle.get("driver") or {}
    profile = vehicle.get("profile") or {}
    counters = vehicle.get("counters") or {}

    lat = last_update.get("lat")
    lng = last_update.get("lng")

    location_str = reverse_geocode(lat, lng) if lat and lng else None
    full_location_str = (
        f"The vehicle {name} is currently located at {location_str}" if location_str
        else f"The vehicle {name}'s location is currently unknown"
    )

    weather_info = get_weather_data(lat, lng) if lat and lng else None
    if weather_info:
        loc = weather_info.get("location", {})
        curr = weather_info.get("current", {})

        try:
            dt_obj = datetime.strptime(loc.get('localtime', ''), "%Y-%m-%d %H:%M")
            localtime = dt_obj.strftime("%Y-%m-%d %I:%M %p")
        except Exception:
            localtime = loc.get('localtime', 'Unknown')

        condition = curr.get('condition', {}).get('text', 'Unknown')
        weather_report = f"""
Weather at this location:
- Condition: {condition}, Temp: {curr.get('temp_c', 'N/A')}°C
- Wind: {curr.get('wind_kph', 'N/A')} km/h, Humidity: {curr.get('humidity', 'N/A')}%
- Local Time: {localtime}, Visibility: {curr.get('vis_km', 'N/A')} km
""".strip()
    else:
        weather_report = "Weather Info: Not available."

    if section == "weather":
        return weather_report
    if section == "location":
        return f"Location: {full_location_str}"
    if section == "speed":
        spd = last_update.get('spd', 'Unknown')
        alt = last_update.get('alt', 'Unknown')
        angle = last_update.get("ang")
        direction = angle_to_direction(angle)
        return f"Vehicle {name} is moving at {spd} km/h, direction: {direction}, altitude: {alt} m"

    # Full Report
    external_v = chPrams.get("ePwrV", {}).get("v")
    internal_v = chPrams.get("iPwrV", {}).get("v")
    ePwrV = external_v / 1000 if external_v and external_v > 100 else external_v
    iPwrV = internal_v / 1000 if internal_v and internal_v > 100 else internal_v

    engine_hours = counters.get("engine_hours", 0)
    engine_hr_display = f"{engine_hours / 3600:.1f} hours" if engine_hours else "Unknown"

    return f"""
Vehicle: {name} (Plate: {profile.get('plate_number')})
- Fuel Type: {profile.get('fuel_type')}, Seats: {profile.get('seats')}
Driver: {driver.get('name')} | Phone: {driver.get('phone')}
Location: {full_location_str}
Speed: {last_update.get('spd')} km/h, Altitude: {last_update.get('alt')} m
Direction: {angle_to_direction(last_update.get('ang'))}
External Power: {ePwrV}V | Internal Power: {iPwrV}V
Odometer: {counters.get('odometer')} km
Engine Hours: {engine_hr_display}
Ignition: {"ON" if last_update.get("acc") == 1 else "OFF"}
IP Address: {last_update.get('ip')}
{weather_report}
""".strip()
