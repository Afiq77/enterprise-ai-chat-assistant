# app/external_api_loader.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")
API_TOKEN = os.getenv("API_TOKEN")

def get_live_vehicle_data():
    """
    Simulated function to fetch live vehicle data from an external API.
    """

    if not BASE_URL or not API_TOKEN:
        print("❌ API_BASE_URL or API_TOKEN not set.")
        return []

    url = f"{BASE_URL}/vehicles/lists?token={API_TOKEN}"

    payload = {
        "data": {
            "offset": 0,
            "limit": 1000,
            "projection": ["basic", "last_update", "telemetry", "driver"]
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            print("✅ Live vehicle data fetched successfully.")
            return response.json().get("data", [])
        else:
            print(f"❌ API request failed. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")

    return []
