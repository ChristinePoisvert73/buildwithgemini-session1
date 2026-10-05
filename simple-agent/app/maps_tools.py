"""Google Maps Geocoding and Places (New) API tools."""

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

# Ensure .env variables are loaded
load_dotenv()


def _get_api_key() -> str:
    """Retrieve Google Maps API key from environment."""
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        # Fallback to checking local .env directly if needed
        env_file = Path(__file__).resolve().parent.parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set.")
    return key


def geocode_address(address: str) -> dict[str, Any]:
    """Converts an address or location name into geographic coordinates (latitude and longitude).

    Args:
        address: The address or location string to geocode (e.g. 'Shinjuku Station, Tokyo', 'Mouraria, Lisbon').

    Returns:
        Dictionary with formatted address and coordinates (latitude, longitude).
    """
    try:
        key = _get_api_key()
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(address)}&key={key}"

        req = urllib.request.Request(url, headers={"User-Agent": "TravelConciergeAgent/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        results = data.get("results")
        if not results:
            return {"error": f"No geocoding results found for '{address}'."}

        first_match = results[0]
        loc = first_match.get("geometry", {}).get("location", {})

        return {
            "name": address,
            "formatted_address": first_match.get("formatted_address", ""),
            "location": {
                "latitude": loc.get("lat"),
                "longitude": loc.get("lng")
            }
        }
    except Exception as e:
        return {"error": f"Geocoding failed for '{address}': {e!s}"}


def find_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "tourist_attraction",
    radius_meters: float = 1000.0
) -> list[dict[str, Any]]:
    """Finds nearby places of a given type around a coordinate using Places API (New).

    Args:
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.
        place_type: Type of place to search for (e.g. 'tourist_attraction', 'restaurant', 'cafe', 'museum', 'bakery').
        radius_meters: Search radius in meters (default 1000m).

    Returns:
        List of nearby places with name, formatted address, and location coordinates.
    """
    try:
        key = _get_api_key()
        url = "https://places.googleapis.com/v1/places:searchNearby"

        body = json.dumps({
            "includedTypes": [place_type],
            "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": float(radius_meters)
                }
            }
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": key,
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location"
            }
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        places = data.get("places", [])
        formatted_places = []

        for p in places:
            display_name = p.get("displayName", {}).get("text", "")
            address = p.get("formattedAddress", "")
            loc = p.get("location", {})

            formatted_places.append({
                "name": display_name,
                "formatted_address": address,
                "location": {
                    "latitude": loc.get("latitude"),
                    "longitude": loc.get("longitude")
                }
            })

        return formatted_places
    except Exception as e:
        return [{"error": f"Nearby search failed: {e!s}"}]
