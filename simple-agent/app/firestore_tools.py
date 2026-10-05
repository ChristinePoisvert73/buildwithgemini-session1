"""Firestore tools for Authentic Adventure Travel Concierge.

HARDCODED GCP PROJECT ID: qwiklabs-gcp-02-d2b5e9270243
Crucial: Do NOT read project ID from google.auth.default() or GOOGLE_CLOUD_PROJECT env var,
as Agent Platform returns the project NUMBER there, breaking Firestore access after deployment.
"""

import os
from pathlib import Path
from typing import Any
from google.cloud import firestore

# HARDCODED GCP PROJECT ID STRING
FIRESTORE_PROJECT = "qwiklabs-gcp-02-d2b5e9270243"
COLLECTION_NAME = "walking_tours"


def _get_db_client() -> firestore.Client:
    """Initialize and return Firestore client with hardcoded project ID."""
    adc_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ and adc_path.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(adc_path)
    return firestore.Client(project=FIRESTORE_PROJECT)


def list_walking_tours(
    city: str | None = None,
    max_duration_hours: float = 4.0,
    max_price_usd: float | None = None
) -> list[dict[str, Any]]:
    """Lists walking tours from Firestore matching duration, city, and price criteria.

    Args:
        city: Optional city name to filter tours (e.g. 'Tokyo', 'Lisbon', 'Kyoto').
        max_duration_hours: Maximum duration of walking tour in hours (default 4.0).
        max_price_usd: Optional maximum price limit in USD.

    Returns:
        List of matching walking tour documents.
    """
    db = _get_db_client()
    collection_ref = db.collection(COLLECTION_NAME)

    # Fetch all tours and apply filtering
    docs = collection_ref.stream()
    tours = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id

        # Duration filter
        duration = data.get("duration_hours", 0.0)
        if duration > max_duration_hours:
            continue

        # City filter (case-insensitive substring)
        if city:
            doc_city = str(data.get("city", "")).lower()
            if city.lower() not in doc_city:
                continue

        # Price filter
        if max_price_usd is not None:
            price = data.get("price_usd", 0.0)
            if price > max_price_usd:
                continue

        tours.append(data)

    return tours


def get_walking_tour_details(tour_id: str) -> dict[str, Any]:
    """Retrieves full details for a specific walking tour by ID.

    Args:
        tour_id: The document ID of the tour (e.g. 'tokyo-street-food-walk').

    Returns:
        Dictionary containing tour details, or error message if not found.
    """
    db = _get_db_client()
    doc_ref = db.collection(COLLECTION_NAME).document(tour_id)
    doc = doc_ref.get()

    if not doc.exists:
        return {"error": f"Walking tour with ID '{tour_id}' not found."}

    data = doc.to_dict()
    data["id"] = doc.id
    return data


def add_walking_tour(
    title: str,
    city: str,
    duration_hours: float,
    price_usd: float,
    description: str,
    vibe: str = "Cultural & Local",
    highlights: list[str] | None = None,
    meetup_point: str = "Central Square",
    max_group_size: int = 8
) -> dict[str, Any]:
    """Adds a new walking tour to the Firestore database.

    Args:
        title: Title of the walking tour.
        city: City where the tour takes place.
        duration_hours: Duration in hours (must be <= 4.0 for walking tours).
        price_usd: Price per person in USD.
        description: Brief description focusing on local culture and authentic human connections.
        vibe: Theme/vibe of the tour (e.g. 'Food & Local Nightlife', 'Artisans & Crafts').
        highlights: List of key tour highlights or stops.
        meetup_point: Meeting location for the tour group.
        max_group_size: Maximum group size.

    Returns:
        Dictionary with status and the newly created tour document details.
    """
    db = _get_db_client()

    # Create slug ID from city and title
    slug = f"{city.lower().replace(' ', '-')}-{title.lower().replace(' ', '-')}"
    slug = "".join(c for c in slug if c.isalnum() or c == "-")[:40].strip("-")

    tour_doc = {
        "id": slug,
        "title": title,
        "city": city,
        "duration_hours": min(duration_hours, 4.0),
        "price_usd": float(price_usd),
        "vibe": vibe,
        "description": description,
        "highlights": highlights or [],
        "meetup_point": meetup_point,
        "max_group_size": max_group_size
    }

    doc_ref = db.collection(COLLECTION_NAME).document(slug)
    doc_ref.set(tour_doc)

    return {
        "status": "success",
        "message": f"Added new walking tour '{title}' to Firestore.",
        "tour": tour_doc
    }
