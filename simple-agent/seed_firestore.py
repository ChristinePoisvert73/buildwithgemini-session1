#!/usr/bin/env python3
"""Seed script for Firestore collection 'walking_tours'.

Hardcoded GCP Project ID: qwiklabs-gcp-02-d2b5e9270243
Do NOT use google.auth.default() or GOOGLE_CLOUD_PROJECT env var for project ID,
as Agent Platform sets those to project number instead of project ID.
"""

import os
from pathlib import Path
from google.cloud import firestore

# HARDCODED GCP PROJECT ID
PROJECT_ID = "qwiklabs-gcp-02-d2b5e9270243"

# Ensure ADC is used if available locally
adc_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ and adc_path.exists():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(adc_path)

COLLECTION_NAME = "walking_tours"

SEED_TOURS = [
    {
        "id": "tokyo-street-food-walk",
        "title": "Sunamachi Hidden Alley Food Walk",
        "city": "Tokyo",
        "duration_hours": 3.5,
        "price_usd": 35.0,
        "vibe": "Food & Local Nightlife",
        "description": "Stroll through a traditional Shotengai (shopping street) away from tourists. Meet local family shop owners, sample homemade tempura and side dishes, and share stories with locals at a neighborhood izakaya.",
        "highlights": [
            "Sample fresh fried tempura at a 50-year-old stall",
            "Chat with neighborhood merchants with live translation",
            "Share drinks and yakitori at a cozy local izakaya"
        ],
        "meetup_point": "Nishi-ojima Station Exit A1",
        "max_group_size": 6
    },
    {
        "id": "lisbon-artisans-fado",
        "title": "Mourama Craft & Secret Fado Stroll",
        "city": "Lisbon",
        "duration_hours": 3.0,
        "price_usd": 28.0,
        "vibe": "Cultural & Music",
        "description": "Walk the historic cobblestone alleys of Mouraria. Meet traditional tile painters and local guitar makers before ending at an informal neighborhood Tasca where locals gather to sing acoustic Fado.",
        "highlights": [
            "Visit an authentic azulejo (tile) restoration workshop",
            "Explore hidden community gardens",
            "Listen to authentic, non-touristy Fado over ginjinha liqueur"
        ],
        "meetup_point": "Praça Martim Moniz (near Hotel Mundial)",
        "max_group_size": 8
    },
    {
        "id": "kyoto-crafts-philosophers-path",
        "title": "Eastern Hills Craft & Zen Path Walk",
        "city": "Kyoto",
        "duration_hours": 4.0,
        "price_usd": 40.0,
        "vibe": "Artisans & Peaceful Nature",
        "description": "Walk along quieter canals and residential backstreets. Stop by local pottery studios, converse with tea masters, and explore small family-run craft shops along the Philosopher's Path.",
        "highlights": [
            "Visit a 4th-generation Kiyomizu pottery workshop",
            "Sip matcha with a local artisan master",
            "Scenic quiet walk through Higashiyama backstreets"
        ],
        "meetup_point": "Keihan Demachiyanagi Station Exit 1",
        "max_group_size": 6
    },
    {
        "id": "mexico-city-coyoacan-bohemian",
        "title": "Coyoacán Markets & Bohemian Alleyways",
        "city": "Mexico City",
        "duration_hours": 3.5,
        "price_usd": 25.0,
        "vibe": "Bohemian Art & Markets",
        "description": "Meander through colorful plazas, historic courtyards, and bustling local markets. Chat with traditional churro bakers, artisanal coffee roasters, and local painters.",
        "highlights": [
            "Taste fresh churros and traditional Mexican cacao",
            "Browse local artisan crafts at Mercado de Coyoacán",
            "Explore leafy residential side streets and quiet parks"
        ],
        "meetup_point": "Plaza Hidalgo (in front of San Juan Bautista church)",
        "max_group_size": 10
    },
    {
        "id": "oaxaca-zapotec-textiles-food",
        "title": "Jalatlaco Street Art & Mezcal Heritage Walk",
        "city": "Oaxaca",
        "duration_hours": 3.0,
        "price_usd": 30.0,
        "vibe": "Street Art & Culinary",
        "description": "Explore the vibrant, cobblestone neighborhood of Jalatlaco. Meet local muralists, visit small family textile workshops, and sample traditional mole made by local grandmothers.",
        "highlights": [
            "Guided tour of iconic neighborhood street art murals",
            "Meet Zapotec weaver families showcasing natural dyes",
            "Taste artisanal mole and traditional Oaxacan drinking chocolate"
        ],
        "meetup_point": "Templo de San Matías Jalatlaco",
        "max_group_size": 8
    }
]


def seed_firestore():
    print(f"Connecting to Firestore for project '{PROJECT_ID}'...")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    print(f"Seeding '{COLLECTION_NAME}' collection...")
    for tour in SEED_TOURS:
        doc_id = tour["id"]
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(tour)
        print(f"  [+] Seeded tour: {doc_id} ('{tour['title']}')")

    print(f"Successfully seeded {len(SEED_TOURS)} tours in Firestore collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    seed_firestore()
