# app/vehicle_filter.py

import re
from app.vehicle_formatter import reverse_geocode, angle_to_direction

def extract_vehicle_filters(query: str) -> dict:
    query = query.lower()
    filters = {}

    def convert_to_kmph(value: int) -> int:
        if "mph" in query:
            return int(round(value * 1.60934))
        return value

    speed_keywords_pattern = re.search(
        r"(?:vehicle|vehicles)?\s*(moving\s*)?"
        r"(faster than|slower than|greater than|lower than|above|below|over|under|"
        r"at least|at most|at or above|at or below|exactly)?\s*(\d+)",
        query
    )
    if speed_keywords_pattern:
        comp = speed_keywords_pattern.group(2) or ""
        value = convert_to_kmph(int(speed_keywords_pattern.group(3)))

        op_map = {
            "faster than": ">", "greater than": ">", "above": ">", "over": ">",
            "slower than": "<", "lower than": "<", "below": "<", "under": "<",
            "at least": ">=", "at or above": ">=",
            "at most": "<=", "at or below": "<=",
            "exactly": "=", "": "="
        }
        filters["speed_filter"] = {"op": op_map.get(comp.strip(), "="), "value": value}

    if "speed_filter" not in filters:
        speed_patterns = [
            r"(?:speed|moving|travelling|traveling)\s*(>|<|=|>=|<=|above|below|over|under|"
            r"at least|at most|at or above|at or below)?\s*(\d+)",
            r"(?:speed|moving|travelling|traveling)\s*(?:more than|less than|greater than|lower than|exactly)?\s*(\d+)"
        ]
        for pattern in speed_patterns:
            match = re.search(pattern, query)
            if match:
                op_raw = match.group(1) or ""
                value = convert_to_kmph(int(match.group(2)))
                op_map = {
                    "above": ">", "over": ">", "more than": ">",
                    "below": "<", "under": "<", "less than": "<",
                    "greater than": ">", "lower than": "<",
                    "at least": ">=", "at or above": ">=",
                    "at most": "<=", "at or below": "<=",
                    "exactly": "=", "": "="
                }
                filters["speed_filter"] = {"op": op_map.get(op_raw.strip(), "="), "value": value}
                break

    range_match = re.search(r"\b(?:between|from)\s*(\d+)\s*(?:and|to)\s*(\d+)\b", query)
    if range_match and any(word in query for word in ["speed", "moving", "travelling", "traveling"]):
        min_val = convert_to_kmph(int(range_match.group(1)))
        max_val = convert_to_kmph(int(range_match.group(2)))
        filters.pop("speed_filter", None)
        filters["speed_range"] = {"min": min_val, "max": max_val}

    if "speed_range" not in filters and "speed_filter" not in filters:
        if any(kw in query for kw in ["moving", "in motion", "driving", "on the move", "active"]):
            filters["moving"] = True
        if any(kw in query for kw in ["stationary", "stopped", "idle", "not moving"]):
            filters["moving"] = False

    if "diesel" in query:
        filters["fuel_type"] = "diesel"

    if "hard cornering" in query or "cornering alarm" in query:
        filters["alarm"] = "hardCornering"

    region_match = re.search(r"(in|from|at|near|around)\s+([a-zA-Z\s]+)", query)
    if region_match:
        region = region_match.group(2).strip()
        if len(region) > 2:
            filters["region"] = region

    directions = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"]
    for dir_word in directions:
        if dir_word in query.replace("-", " "):
            filters["direction"] = dir_word.replace(" ", "-").capitalize()
            break

    name_match = re.search(r"(\d+\s*[A-Za-z]+)", query)
    if name_match:
        filters["name"] = name_match.group(0).strip()

    return filters

def filter_vehicles(data: list[dict], criteria: dict) -> list[dict]:
    filtered = []

    for item in data:
        profile = item.get("profile", {}) or {}
        last_update = item.get("last_update", {}) or {}
        location_str = item.get("_location_str", "Unknown")
        chPrams = last_update.get("chPrams", {}) or {}
        speed = last_update.get("spd", 0)

        if "name" in criteria and criteria["name"].lower() not in item.get("name", "").lower():
            continue

        if "moving" in criteria and "speed_filter" not in criteria and "speed_range" not in criteria:
            if criteria["moving"] != (speed > 0):
                continue

        if "alarm" in criteria and chPrams.get("alarm", {}).get("v") != criteria["alarm"]:
            continue

        if "fuel_type" in criteria and profile.get("fuel_type") != criteria["fuel_type"]:
            continue

        if "region" in criteria and criteria["region"].lower() not in location_str.lower():
            continue

        if "direction" in criteria:
            angle = last_update.get("ang")
            if angle_to_direction(angle).lower().replace(" ", "-") != criteria["direction"].lower():
                continue

        if "speed_range" in criteria:
            if not (criteria["speed_range"]["min"] <= speed <= criteria["speed_range"]["max"]):
                continue

        if "speed_filter" in criteria:
            op = criteria["speed_filter"]["op"]
            val = criteria["speed_filter"]["value"]
            if (op == ">" and speed <= val) or (op == "<" and speed >= val) or \
               (op == ">=" and speed < val) or (op == "<=" and speed > val) or \
               (op == "=" and speed != val):
                continue

        filtered.append(item)

    return filtered

def summarize_vehicle_list(vehicles: list[dict], criteria: dict = None) -> str:
    if not vehicles:
        return "No matching vehicles found."

    criteria = criteria or {}
    summary_lines = []

    intro_parts = []
    if "moving" in criteria:
        intro_parts.append("currently moving" if criteria["moving"] else "currently stationary")
    if "fuel_type" in criteria:
        intro_parts.append(f"with fuel type '{criteria['fuel_type']}'")
    if "alarm" in criteria:
        intro_parts.append(f"with alarm '{criteria['alarm']}'")
    if "region" in criteria:
        intro_parts.append(f"in region '{criteria['region']}'")
    if "direction" in criteria:
        intro_parts.append(f"heading '{criteria['direction']}'")
    if "speed_range" in criteria:
        r = criteria["speed_range"]
        intro_parts.append(f"speed between {r['min']} and {r['max']} km/h")
    if "speed_filter" in criteria:
        sf = criteria["speed_filter"]
        intro_parts.append(f"speed {sf['op']} {sf['value']} km/h")

    intro = "The following vehicles " + (" and ".join(intro_parts) if intro_parts else "match your criteria") + ":\n"

    info = []
    for v in vehicles:
        name = v.get("name", "Unknown")
        driver = v.get("driver", {}).get("name", "Unknown")
        speed = v.get("last_update", {}).get("spd", 0)
        direction = angle_to_direction(v.get("last_update", {}).get("ang"))
        info.append(f"{name} (Driver: {driver}, Direction: {direction}, Speed: {speed} km/h)")

    if "moving" in criteria or "speed_filter" in criteria or "speed_range" in criteria:
        info.sort()

    return intro + "\n".join(info)
