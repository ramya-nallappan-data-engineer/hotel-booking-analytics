import random
import pandas as pd
from datetime import datetime, date

from config import (
    fake,
    GENDERS,
    TRAVELER_TYPES,
    TRAVELER_TYPE_WEIGHTS,
    LANGUAGES
)

from config import LOCATIONS, NUM_CUSTOMERS

def generate_customers() -> pd.DataFrame:

    num_customers = NUM_CUSTOMERS

    ...
    """
    Generate customer master data.

    Returns:
        pandas.DataFrame
    """

    customers = []

    current_timestamp = datetime.now()

    for i in range(1, num_customers + 1):

        city, country = random.choice(LOCATIONS)

        birth_year = random.randint(1955,2005)

        gender = random.choice(GENDERS)

        if gender == "Male":
            customer_name = fake.name_male()
        else:
            customer_name = fake.name_female()

        email = (
            customer_name
            .lower()
            .replace(" ", ".")
        )

        email = f"{email}{i}@example.com"

        preferred_language = LANGUAGES.get(
            country,
            "English"
        )

        birth_year = random.randint(1950, 2005)

        date_of_birth = fake.date_between(
            start_date=date(birth_year, 1, 1),
            end_date=date(birth_year, 12, 31)
        )

        traveler_type = random.choices(
            TRAVELER_TYPES,
            weights=TRAVELER_TYPE_WEIGHTS,
            k=1
            )[0]

        if traveler_type == "Frequent":
            customer_segment = random.choices(
                ["Business", "Leisure"],
                weights=[75, 25],
                k=1
            )[0]

        elif traveler_type == "Regular":
            customer_segment = random.choices(
                ["Business", "Leisure"],
                weights=[40, 60],
                k=1
            )[0]

        else:  # Casual
            customer_segment = random.choices(
                ["Business", "Leisure"],
                weights=[20, 80],
                k=1
            )[0]

        if customer_segment == "Business":
            signup_channel = random.choices(
                ["Corporate", "Website", "Mobile App"],
                weights=[45, 35, 20],
                k=1
            )[0]

        else:
            signup_channel = random.choices(
                ["Mobile App", "Website", "Corporate"],
                weights=[55, 35, 10],
                k=1
            )[0]

        if traveler_type == "Frequent":

            loyalty_tier = random.choices(
                ["Bronze", "Silver", "Gold", "Platinum"],
                weights=[15, 25, 35, 25],
                k=1
            )[0]

        elif traveler_type == "Regular":

            loyalty_tier = random.choices(
                ["Bronze", "Silver", "Gold", "Platinum"],
                weights=[35, 35, 20, 10],
                k=1
            )[0]

        else:

            loyalty_tier = random.choices(
                ["Bronze", "Silver", "Gold", "Platinum"],
                weights=[70, 20, 8, 2],
                k=1
            )[0]

        if traveler_type == "Frequent":

            signup_date = fake.date_between(
                start_date="-8y",
                end_date="-2y"
            )

        elif traveler_type == "Regular":

            signup_date = fake.date_between(
                start_date="-5y",
                end_date="-1y"
            )

        else:

            signup_date = fake.date_between(
                start_date="-3y",
                end_date="today"
            )

        if traveler_type == "Frequent":

            is_active = random.random() < 0.98

        elif traveler_type == "Regular":

            is_active = random.random() < 0.92

        else:

            is_active = random.random() < 0.82

        customer = {

            "customer_id": f"CUS{i:05}",

            "customer_name": customer_name,

            "gender": gender,

            "date_of_birth": date_of_birth,

            "email": email,

            "city": city,

            "country": country,

            "preferred_language": preferred_language,

            "signup_date": signup_date,

            "loyalty_tier": loyalty_tier,

            "traveler_type": traveler_type,

            "customer_segment": customer_segment,

            "signup_channel": signup_channel,

            "is_active": is_active,

            "created_at": current_timestamp,

            "updated_at": current_timestamp
        }

        customers.append(customer)

    return pd.DataFrame(customers)