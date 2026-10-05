"""Weather forecast tool using Open-Meteo free API."""

import json
import urllib.parse
import urllib.request
from typing import Any

WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


def get_city_weather_forecast(city: str) -> dict[str, Any]:
    """Fetches real-time weather and outdoor walking suitability for a city using Open-Meteo.

    Args:
        city: Name of the destination city (e.g. 'Tokyo', 'Lisbon', 'Kyoto', 'Oaxaca').

    Returns:
        Dictionary containing current temperature, weather condition, wind speed, and walking tour advisory.
    """
    try:
        # 1. Geocode city name to lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"
        req = urllib.request.Request(geo_url, headers={"User-Agent": "TravelConciergeAgent/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            geo_data = json.loads(response.read().decode("utf-8"))

        results = geo_data.get("results")
        if not results:
            return {"error": f"City '{city}' not found."}

        location = results[0]
        lat, lon = location["latitude"], location["longitude"]
        city_name = location.get("name", city)
        country = location.get("country", "")

        # 2. Fetch current weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        req_w = urllib.request.Request(weather_url, headers={"User-Agent": "TravelConciergeAgent/1.0"})
        with urllib.request.urlopen(req_w, timeout=5) as response:
            weather_data = json.loads(response.read().decode("utf-8"))

        current = weather_data.get("current_weather", {})
        temp_c = current.get("temperature", 0.0)
        temp_f = round((temp_c * 9 / 5) + 32, 1)
        weather_code = current.get("weathercode", 0)
        condition = WMO_WEATHER_CODES.get(weather_code, "Clear/Cloudy")
        wind_kmh = current.get("windspeed", 0.0)

        # 3. Determine outdoor walking advisory
        if weather_code in [61, 63, 65, 80, 81, 82, 95]:
            advisory = "Rain expected. Bring an umbrella or consider indoor artisan workshops."
        elif temp_c > 32:
            advisory = "Hot weather. Plan 4-hour walking tours in early morning or evening; carry water."
        elif temp_c < 5:
            advisory = "Cold weather. Dress warmly in layers for extended outdoor walks."
        else:
            advisory = "Great weather for outdoor neighborhood walking tours!"

        return {
            "city": f"{city_name}, {country}".strip(", "),
            "temperature_celsius": temp_c,
            "temperature_fahrenheit": temp_f,
            "condition": condition,
            "wind_speed_kmh": wind_kmh,
            "walking_advisory": advisory,
        }
    except Exception as e:
        return {"error": f"Failed to fetch weather for '{city}': {e!s}"}
