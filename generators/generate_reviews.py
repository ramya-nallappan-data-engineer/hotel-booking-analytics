import random
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

REVIEW_TITLES = [
    "Excellent Stay",
    "Highly Recommended",
    "Great Experience",
    "Comfortable Rooms",
    "Value for Money",
    "Pleasant Stay",
    "Average Experience",
    "Needs Improvement"
]

REVIEW_TEXTS = [

    "Room was clean and staff were very friendly.",

    "Excellent location with comfortable rooms.",

    "Great hospitality and smooth check-in process.",

    "Breakfast was good and amenities were well maintained.",

    "Would definitely stay here again.",

    "Very pleasant stay with excellent service.",

    "Overall a good experience for the price paid.",

    "Hotel was neat but food could be improved.",

    "The room was spacious and comfortable.",

    "Amazing experience from check-in to checkout.",

    "Good value for money.",

    "The stay exceeded my expectations.",

    "Staff were courteous and always ready to help.",

    "Clean rooms and peaceful atmosphere.",

    "The property was conveniently located.",

    "Wi-Fi and room service were excellent.",

    "Expected slightly better maintenance.",

    "Could improve cleanliness in common areas.",

    "Loved the facilities and ambience.",

    "Would happily recommend this hotel."
]

def generate_review_id(
    review_number: int
) -> str:
    """
    Generate review ID.
    """

    return f"RV{review_number:06d}"


def generate_review_date(
    checkout_date: datetime
) -> datetime:
    """
    Generate review date 1–15 days
    after checkout.
    """

    return checkout_date + timedelta(
        days=random.randint(1, 15)
    )

def build_review_record(
    review_number: int,
    booking: dict[str, Any]
) -> dict[str, Any]:
    """
    Build a review record.
    """

    rating = random.choices(
        population=[5, 4, 3, 2, 1],
        weights=[45, 30, 15, 7, 3],
        k=1
    )[0]

    review_date = generate_review_date(
        booking["check_out_date"]
    )

    audit_timestamp = datetime.now()

    return {

        "review_id":
            generate_review_id(review_number),

        "booking_id":
            booking["booking_id"],

        "customer_id":
            booking["customer_id"],

        "hotel_id":
            booking["hotel_id"],

        "rating":
            rating,

        "review_title":
            random.choice(REVIEW_TITLES),

        "review_text":
            random.choice(REVIEW_TEXTS),

        "review_date":
            review_date,

        "created_at":
            audit_timestamp,

        "updated_at":
            audit_timestamp

    }

def generate_reviews(
    bookings_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate customer reviews.
    """

    print("\nStarting Review Generation...")

    review_records = []

    review_number = 1

    eligible_bookings = bookings_df[
        bookings_df["booking_status"] == "Completed"
    ]

    for _, booking in eligible_bookings.iterrows():

        if random.random() > 0.70:
            continue

        review_records.append(

            build_review_record(
                review_number=review_number,
                booking=booking.to_dict()
            )

        )

        review_number += 1

    reviews_df = pd.DataFrame(
        review_records
    )

    if not reviews_df.empty:

        date_columns = [
            "review_date",
            "created_at",
            "updated_at"
        ]

        for column in date_columns:

            reviews_df[column] = pd.to_datetime(
                reviews_df[column]
            )

        reviews_df = (

            reviews_df

            .sort_values(
                by=[
                    "review_date",
                    "review_id"
                ]
            )

            .reset_index(
                drop=True
            )

        )

    print(
        f"Generated {len(reviews_df):,} reviews."
    )

    return reviews_df