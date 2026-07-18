import random
from datetime import datetime

import pandas as pd

from config import (
    LOCATIONS,
    HOTEL_CHAINS,
    HOTEL_CHAIN_WEIGHTS,
    HOTEL_STAR_RATINGS,
    HOTEL_STAR_WEIGHTS,
    HOTEL_TYPES,
    HOTEL_STATUS,
    HOTEL_STATUS_WEIGHTS,
    NUM_HOTELS
)


def determine_hotel_type(city):
    """
    Determine hotel type based on city.
    """

    if city in ["Barcelona", "Dubai"]:
        return "Resort"

    if city in ["Amsterdam", "London", "Singapore", "Frankfurt", "Munich"]:
        return random.choice(["Business", "City"])

    if city in ["Paris", "Rome", "Madrid", "Milan"]:
        return "City"

    return random.choice(HOTEL_TYPES)


def generate_hotels():
    """
    Generate hotel master data.

    Returns:
        pandas.DataFrame
    """

    hotels = []

    current_timestamp = datetime.now()

    for i in range(1, NUM_HOTELS + 1):

        city, country = random.choice(LOCATIONS)

        hotel_chain = random.choices(
            HOTEL_CHAINS,
            weights=HOTEL_CHAIN_WEIGHTS,
            k=1
        )[0]

        star_rating = random.choices(
            HOTEL_STAR_RATINGS,
            weights=HOTEL_STAR_WEIGHTS,
            k=1
        )[0]

        # ----------------------------------------------------
        # Hotel Name
        # ----------------------------------------------------

        if hotel_chain == "Independent":

            prefix = random.choice([
                "Grand",
                "Royal",
                "Elite",
                "Golden",
                "Blue",
                "Imperial",
                "Palm",
                "Regency"
            ])

            suffix = random.choice([
                "Hotel",
                "Suites",
                "Palace",
                "Resort",
                "Inn"
            ])

            hotel_name = f"{prefix} {city} {suffix}"

        else:

            hotel_name = f"{hotel_chain} {city}"

        # ----------------------------------------------------
        # Room Count
        # ----------------------------------------------------

        if star_rating == 5:
            room_count = random.randint(220, 400)

        elif star_rating == 4:
            room_count = random.randint(120, 250)

        else:
            room_count = random.randint(70, 180)

        # Independent hotels are usually smaller

        if hotel_chain == "Independent":
            room_count = int(room_count * 0.80)

        # ----------------------------------------------------
        # Opened Year
        # ----------------------------------------------------

        if star_rating == 5:
            opened_year = random.randint(1990, 2023)

        elif star_rating == 4:
            opened_year = random.randint(1995, 2024)

        else:
            opened_year = random.randint(2000, 2025)

        # ----------------------------------------------------
        # Facilities
        # ----------------------------------------------------

        if star_rating == 5:

            has_spa = True
            has_pool = True
            has_gym = True

        elif star_rating == 4:

            has_spa = random.random() < 0.70
            has_pool = random.random() < 0.90
            has_gym = random.random() < 0.95

        else:

            has_spa = random.random() < 0.20
            has_pool = random.random() < 0.60
            has_gym = random.random() < 0.75

        # ----------------------------------------------------
        # Average Occupancy
        # ----------------------------------------------------

        if star_rating == 5:

            average_occupancy_rate = random.randint(82, 95)

        elif star_rating == 4:

            average_occupancy_rate = random.randint(75, 90)

        else:

            average_occupancy_rate = random.randint(65, 85)

        # ----------------------------------------------------
        # Hotel Type
        # ----------------------------------------------------

        hotel_type = determine_hotel_type(city)

        # ----------------------------------------------------
        # Hotel Status
        # ----------------------------------------------------

        hotel_status = random.choices(
            HOTEL_STATUS,
            weights=HOTEL_STATUS_WEIGHTS,
            k=1
        )[0]

        # ----------------------------------------------------
        # Record
        # ----------------------------------------------------

        hotel = {

            "hotel_id": f"HOT{i:04}",

            "hotel_name": hotel_name,

            "hotel_chain": hotel_chain,

            "hotel_type": hotel_type,

            "hotel_status": hotel_status,

            "city": city,

            "country": country,

            "star_rating": star_rating,

            "room_count": room_count,

            "average_occupancy_rate": average_occupancy_rate,

            "opened_year": opened_year,

            "has_spa": has_spa,

            "has_pool": has_pool,

            "has_gym": has_gym,

            "created_at": current_timestamp,

            "updated_at": current_timestamp

        }

        hotels.append(hotel)

    return pd.DataFrame(hotels)