import random
from datetime import datetime, timedelta

import pandas as pd

from config import (
    ROOM_PRICE_BY_STAR,
    ROOM_TYPE_MULTIPLIERS,
    SEASON_MULTIPLIERS,
    WEEKEND_MULTIPLIER,
    MAX_STAY_NIGHTS,
    ROOM_TYPES,
    ROOM_TYPE_WEIGHTS,
    GST_PERCENTAGE,
    SERVICE_FEE_PERCENTAGE,
    MAX_DISCOUNT_PERCENTAGE,
    MARKET_VARIATION_RANGE,
    CANCELLATION_FEE_RATE
)

CURRENT_TIMESTAMP = datetime.now()

BOOKING_STATUS = [
    "Completed",
    "Cancelled",
    "Pending"
]

BOOKING_SOURCE_MAPPING = {
    "Website": "Direct",
    "Mobile App": "Direct",
    "Corporate": "Corporate",
    "Travel Agent": "OTA"
}

MONTH_WEIGHTS = {

    1: 7,

    2: 5,

    3: 7,

    4: 8,

    5: 10,

    6: 12,

    7: 14,

    8: 13,

    9: 8,

    10: 9,

    11: 9,

    12: 18

}

def build_customer_lookup(customers_df):

    return customers_df.set_index(

        "customer_id"

    ).to_dict("index")

def build_hotel_lookup(hotels_df):

    return hotels_df.set_index(

        "hotel_id"

    ).to_dict("index")

def build_star_groups(hotels_df):

    active_hotels = hotels_df[
        hotels_df["hotel_status"] == "Active"
        ]

    return {

        3: active_hotels[
            active_hotels.star_rating == 3
            ],

        4: active_hotels[
            active_hotels.star_rating == 4
            ],

        5: active_hotels[
            active_hotels.star_rating == 5
            ]

    }

def generate_booking_id(number):

    return f"BOOK{number:06}"

def is_weekend(date_value):

    return date_value.weekday() >= 4

def calculate_checkout(

    checkin,

    nights

):

    return checkin + timedelta(

        days=nights

    )

def create_booking_record(**kwargs):

    return kwargs

def random_row(df):
    """
    Return a random row from a DataFrame.
    """

    return df.sample(
        n=1,
        replace=False
    ).iloc[0]

def clamp(value, minimum, maximum):
    """
    Restrict a value within the specified range.

    Args:
        value: Value to clamp.
        minimum: Minimum allowed value.
        maximum: Maximum allowed value.

    Returns:
        Clamped value.
    """
    return max(minimum, min(value, maximum))

# ============================================================
# CUSTOMER BOOKING PLANNER
# ============================================================

def determine_booking_count(customer):
    """
    Determine how many bookings a customer should have
    based on traveller type and booking persona.
    """

    traveler_type = customer["traveler_type"]

    if traveler_type == "Frequent":

        persona = random.choices(
            ["VIP", "Normal", "Dormant"],
            weights=[30, 55, 15],
            k=1
        )[0]

        if persona == "VIP":
            return random.randint(28, 40)

        elif persona == "Normal":
            return random.randint(18, 28)

        return random.randint(10, 18)

    elif traveler_type == "Regular":

        persona = random.choices(
            ["Heavy", "Normal", "Light"],
            weights=[25, 60, 15],
            k=1
        )[0]

        if persona == "Heavy":
            return random.randint(12, 18)

        elif persona == "Normal":
            return random.randint(6, 12)

        return random.randint(3, 6)

    else:

        persona = random.choices(
            ["Vacation", "Occasional"],
            weights=[70, 30],
            k=1
        )[0]

        if persona == "Vacation":
            return random.randint(1, 3)

        return random.randint(4, 6)


def build_customer_booking_plan(
    customers_df,
    num_bookings
):
    """
    Build a realistic booking plan.

    Customers receive multiple booking entries based on
    their traveller profile.

    The final output is a shuffled list of customer IDs
    with exactly num_bookings records.
    """

    booking_plan = []

    frequent_customers = []
    regular_customers = []

    for _, customer in customers_df.iterrows():

        booking_count = determine_booking_count(customer)

        customer_id = customer["customer_id"]

        booking_plan.extend(
            [customer_id] * booking_count
        )

        if customer["traveler_type"] == "Frequent":
            frequent_customers.append(customer_id)

        elif customer["traveler_type"] == "Regular":
            regular_customers.append(customer_id)

    random.shuffle(booking_plan)

    if len(booking_plan) > num_bookings:

        booking_plan = booking_plan[:num_bookings]

    while len(booking_plan) < num_bookings:

        preferred_pool = frequent_customers + regular_customers

        booking_plan.append(
            random.choice(preferred_pool)
        )

    random.shuffle(booking_plan)

    return booking_plan


def prepare_booking_tracker(customers_df):
    """
    Track booking sequence for each customer.

    Example

    CUS00001

    Booking 1

    Booking 2

    Booking 3
    """

    return {

        customer_id: 0

        for customer_id in customers_df["customer_id"]

    }


def next_booking_sequence(
    booking_tracker,
    customer_id
):
    """
    Increment and return booking sequence.
    """

    booking_tracker[customer_id] += 1

    return booking_tracker[customer_id]

# ============================================================
# BOOKING DATE & SEASONALITY ENGINE
# ============================================================

def select_booking_month():
    """
    Select booking month based on realistic hotel demand.
    """

    months = list(MONTH_WEIGHTS.keys())
    weights = list(MONTH_WEIGHTS.values())

    return random.choices(
        months,
        weights=weights,
        k=1
    )[0]


def generate_booking_date(start_year=2022, end_year=2025):
    """
    Generate a realistic booking date.
    """

    year = random.randint(start_year, end_year)

    month = select_booking_month()

    while True:

        try:

            day = random.randint(1, 28)

            booking_date = datetime(
                year,
                month,
                day
            )

            if booking_date <= CURRENT_TIMESTAMP:
                return booking_date

        except ValueError:
            continue


def determine_lead_time(customer):
    """
    Days between booking and check-in.

    Frequent travellers usually book later.
    Leisure travellers usually book earlier.
    """

    traveler_type = customer["traveler_type"]

    loyalty = customer["loyalty_tier"]

    if loyalty == "Platinum":
        return random.randint(2, 20)

    if loyalty == "Gold":
        return random.randint(5, 35)

    if traveler_type == "Frequent":
        return random.randint(3, 25)

    if traveler_type == "Regular":
        return random.randint(10, 45)

    return random.randint(15, 90)


def determine_stay_nights(customer: dict) -> int:
    traveler_type = customer["traveler_type"]

    min_nights, max_nights = MAX_STAY_NIGHTS.get(
        traveler_type,
        (1, 4)   # Default if traveler type isn't found
    )

    return random.randint(min_nights, max_nights)


def generate_checkin_date(
    booking_date,
    lead_time_days
):
    """
    Calculate check-in date.
    """

    return booking_date + timedelta(
        days=lead_time_days
    )


def determine_season(checkin_date):
    """
    Determine season from check-in month.
    """

    month = checkin_date.month

    if month in [12, 1]:
        return "Peak"

    if month in [6, 7, 8]:
        return "Summer"

    if month in [3, 4, 5]:
        return "Spring"

    return "Off Peak"


def determine_day_type(checkin_date):
    """
    Weekday or weekend.
    """

    if is_weekend(checkin_date):
        return "Weekend"

    return "Weekday"


def determine_booking_channel(customer):
    """
    Determine booking channel.
    """

    traveler = customer["traveler_type"]

    if traveler == "Frequent":

        return random.choices(

            ["Corporate", "Website", "Mobile App"],

            weights=[45, 25, 30],

            k=1

        )[0]

    elif traveler == "Regular":

        return random.choices(

            ["Website", "Mobile App", "Travel Agent"],

            weights=[40, 35, 25],

            k=1

        )[0]

    else:

        return random.choices(

            ["Travel Agent", "Website", "Mobile App"],

            weights=[45, 30, 25],

            k=1

        )[0]


def determine_booking_source(channel):
    """
    Map booking channel to booking source.
    """

    return BOOKING_SOURCE_MAPPING[channel]


def determine_booking_status(
    customer,
    lead_time_days
):
    """
    Determine booking status.

    Long lead times are cancelled more often.

    Loyal customers rarely cancel.
    """

    loyalty = customer["loyalty_tier"]

    if loyalty == "Platinum":

        weights = [95, 3, 2]

    elif loyalty == "Gold":

        weights = [90, 7, 3]

    else:

        if lead_time_days > 60:

            weights = [75, 20, 5]

        elif lead_time_days > 30:

            weights = [82, 13, 5]

        else:

            weights = [88, 8, 4]

    return random.choices(

        BOOKING_STATUS,

        weights=weights,

        k=1

    )[0]


def determine_guest_count(
    room_type
):
    """
    Guest count based on room type.
    """

    mapping = {

        "Standard": [1, 2],

        "Deluxe": [2, 3],

        "Suite": [2, 3, 4]

    }

    return random.choice(
        mapping[room_type]
    )


def determine_occupancy_type(
    guest_count
):
    """
    Occupancy category.
    """

    if guest_count == 1:
        return "Solo"

    if guest_count == 2:
        return "Couple"

    return "Family"

# ============================================================
# HOTEL & ROOM SELECTION ENGINE
# ============================================================

def determine_preferred_star(customer):
    """
    Determine the preferred hotel star rating based on
    customer loyalty and traveller profile.
    """

    loyalty = customer["loyalty_tier"]
    traveler = customer["traveler_type"]

    if loyalty == "Platinum":

        return random.choices(
            [5, 4],
            weights=[75, 25],
            k=1
        )[0]

    elif loyalty == "Gold":

        return random.choices(
            [5, 4, 3],
            weights=[30, 55, 15],
            k=1
        )[0]

    elif loyalty == "Silver":

        return random.choices(
            [4, 3],
            weights=[60, 40],
            k=1
        )[0]

    if traveler == "Frequent":

        return random.choices(
            [5, 4],
            weights=[40, 60],
            k=1
        )[0]

    return random.choices(
        [3, 4],
        weights=[70, 30],
        k=1
    )[0]


def select_hotel(
    customer,
    star_groups
):
    """
    Select an eligible hotel.
    """

    preferred_star = determine_preferred_star(customer)

    eligible = star_groups.get(preferred_star)

    if eligible is None or eligible.empty:

        eligible = pd.concat(star_groups.values())

    hotel = random_row(eligible)

    return hotel.to_dict()


def determine_room_type(hotel):
    """
    Select room type based on hotel star rating.
    """

    star = int(hotel.get("star_rating", 3))

    weights = ROOM_TYPE_WEIGHTS.get(star)

    if weights is None:
        raise ValueError(f"Unsupported hotel star rating: {star}")

    return random.choices(
        population=ROOM_TYPES,
        weights=weights,
        k=1
    )[0]


def determine_hotel_occupancy(
    hotel,
    season
):
    """
    Estimate occupancy.
    """

    occupancy = hotel["average_occupancy_rate"]

    if season == "Peak":
        occupancy += random.randint(10, 18)

    elif season == "Summer":
        occupancy += random.randint(6, 12)

    elif season == "Spring":
        occupancy += random.randint(2, 6)

    else:
        occupancy -= random.randint(2, 8)

    return clamp(
        occupancy,
        40,
        100
    )

def determine_demand_level(
    occupancy
):
    """
    Convert occupancy to demand level.
    """

    if occupancy >= 90:
        return "Very High"

    elif occupancy >= 80:
        return "High"

    elif occupancy >= 65:
        return "Medium"

    return "Low"


def determine_room_availability(
    hotel,
    occupancy
):
    """
    Simulate room availability.
    """

    total_rooms = hotel["room_count"]

    occupied = int(
        total_rooms * occupancy / 100
    )

    available = total_rooms - occupied

    return max(
        available,
        0
    )


def determine_booking_priority(
    customer
):
    """
    Booking priority used later for upgrades.
    """

    loyalty = customer["loyalty_tier"]

    if loyalty == "Platinum":
        return "VIP"

    elif loyalty == "Gold":
        return "High"

    elif loyalty == "Silver":
        return "Medium"

    return "Standard"


def determine_upgrade_eligibility(
    customer,
    occupancy
):
    """
    Whether customer may receive a complimentary room upgrade.
    """

    loyalty = customer["loyalty_tier"]

    if occupancy > 90:
        return False

    if loyalty == "Platinum":

        return random.random() < 0.60

    elif loyalty == "Gold":

        return random.random() < 0.30

    elif loyalty == "Silver":

        return random.random() < 0.15

    return False


def apply_room_upgrade(
    room_type,
    eligible
):
    """
    Upgrade room where applicable.
    """

    if not eligible:

        return room_type

    if room_type == "Standard":
        return "Deluxe"

    if room_type == "Deluxe":
        return "Suite"

    return room_type

# ============================================================
# DYNAMIC PRICING ENGINE
# ============================================================

def calculate_base_room_rate(hotel, room_type):
    """
    Base room rate using hotel star rating
    and room category.
    """

    star = hotel["star_rating"]

    base_rate = ROOM_PRICE_BY_STAR[star]

    multiplier = ROOM_TYPE_MULTIPLIERS[room_type]

    return round(base_rate * multiplier, 2)


def apply_season_multiplier(
    room_rate,
    season
):
    """
    Adjust room rate based on season.
    """

    multiplier = SEASON_MULTIPLIERS.get(
        season,
        1.0
    )

    return round(
        room_rate * multiplier,
        2
    )


def apply_weekend_multiplier(
    room_rate,
    checkin_date
):
    """
    Weekend bookings generally cost more.
    """

    if is_weekend(checkin_date):

        room_rate *= WEEKEND_MULTIPLIER

    return round(room_rate, 2)


def apply_demand_multiplier(
    room_rate,
    occupancy
):
    """
    Higher occupancy drives higher prices.
    """

    if occupancy >= 95:

        multiplier = 1.30

    elif occupancy >= 90:

        multiplier = 1.20

    elif occupancy >= 80:

        multiplier = 1.10

    elif occupancy >= 70:

        multiplier = 1.05

    else:

        multiplier = 1.00

    return round(
        room_rate * multiplier,
        2
    )


def apply_market_variation(room_rate):
    """
    Introduce small market fluctuations.
    """

    variation = random.uniform(
        *MARKET_VARIATION_RANGE
    )

    return round(
        room_rate * variation,
        2
    )


def calculate_total_room_charges(
    room_rate,
    stay_nights
):
    """
    Room charge for entire stay.
    """

    return round(
        room_rate * stay_nights,
        2
    )


def determine_discount_percentage(
    customer,
    stay_nights,
    booking_channel
):
    """
    Loyalty and promotional discounts.
    """

    loyalty = customer["loyalty_tier"]

    discount = 0

    if loyalty == "Platinum":

        discount += 15

    elif loyalty == "Gold":

        discount += 10

    elif loyalty == "Silver":

        discount += 5

    if stay_nights >= 5:

        discount += 5

    if booking_channel == "Website":

        discount += 3

    elif booking_channel == "Mobile App":

        discount += 2

    return min(
        discount,
        MAX_DISCOUNT_PERCENTAGE
    )


def calculate_discount_amount(
    total_room_charges,
    discount_percentage
):
    """
    Discount value.
    """

    return round(
        total_room_charges *
        discount_percentage / 100,
        2
    )


def calculate_tax_amount(
    taxable_amount
):
    """
    Hotel tax.
    """

    return round(
        taxable_amount *
        GST_PERCENTAGE / 100,
        2

    )


def calculate_service_fee(
    taxable_amount
):
    """
    Service fee.
    """

    return round(
        taxable_amount *
        SERVICE_FEE_PERCENTAGE / 100,
        2
    )


def calculate_pricing(
    customer,
    hotel,
    room_type,
    season,
    occupancy,
    stay_nights,
    booking_channel,
    checkin_date,
    booking_status
):
    """
    Master pricing engine.
    """

    room_rate = calculate_base_room_rate(
        hotel,
        room_type
    )

    room_rate = apply_season_multiplier(
        room_rate,
        season
    )

    room_rate = apply_weekend_multiplier(
        room_rate,
        checkin_date
    )

    room_rate = apply_demand_multiplier(
        room_rate,
        occupancy
    )

    room_rate = apply_market_variation(
        room_rate
    )

    total_room_charges = calculate_total_room_charges(
        room_rate,
        stay_nights
    )

    discount_percentage = determine_discount_percentage(
        customer,
        stay_nights,
        booking_channel
    )

    discount_amount = calculate_discount_amount(
        total_room_charges,
        discount_percentage
    )

    taxable_amount = (
        total_room_charges -
        discount_amount
    )

    tax_amount = calculate_tax_amount(
        taxable_amount
    )

    service_fee = calculate_service_fee(
        taxable_amount
    )

    gross_amount = round(
        total_room_charges +
        tax_amount +
        service_fee,
        2
    )

    net_amount = round(
        gross_amount -
        discount_amount,
        2
    )

    if booking_status == "Cancelled":

        cancellation_fee = round(
            room_rate * CANCELLATION_FEE_RATE,
            2
        )

        net_amount = cancellation_fee

        gross_amount = cancellation_fee

        tax_amount = 0

        service_fee = 0

        discount_amount = 0

    return {

        "room_rate": room_rate,

        "total_room_charges": total_room_charges,

        "discount_percentage": discount_percentage,

        "discount_amount": discount_amount,

        "tax_amount": tax_amount,

        "service_fee": service_fee,

        "gross_amount": gross_amount,

        "net_amount": net_amount

    }

# ============================================================
# BOOKING RECORD BUILDER
# ============================================================

def build_booking_record(
    booking_number,
    customer_id,
    customer_lookup,
    star_groups,
    booking_tracker
):
    """
    Build one complete booking record.
    """

    customer = customer_lookup[customer_id]

    # --------------------------------------------------------
    # Booking Sequence
    # --------------------------------------------------------

    booking_sequence = next_booking_sequence(
        booking_tracker,
        customer_id
    )

    booking_id = generate_booking_id(
        booking_number
    )

    # --------------------------------------------------------
    # Booking Dates
    # --------------------------------------------------------

    booking_date = generate_booking_date()

    lead_time_days = determine_lead_time(
        customer
    )

    check_in_date = generate_checkin_date(
        booking_date,
        lead_time_days
    )

    stay_nights = determine_stay_nights(
        customer
    )

    check_out_date = calculate_checkout(
        check_in_date,
        stay_nights
    )

    season = determine_season(
        check_in_date
    )

    day_type = determine_day_type(check_in_date)

    day_type = day_type

    # --------------------------------------------------------
    # Hotel Selection
    # --------------------------------------------------------

    hotel = select_hotel(
        customer,
        star_groups
    )

    room_type = determine_room_type(
        hotel
    )

    occupancy = determine_hotel_occupancy(
        hotel,
        season
    )

    demand_level = determine_demand_level(
        occupancy
    )

    available_rooms = determine_room_availability(
        hotel,
        occupancy
    )

    booking_priority = determine_booking_priority(
        customer
    )

    upgrade_given = determine_upgrade_eligibility(
        customer,
        occupancy
    )

    room_type = apply_room_upgrade(
        room_type,
        upgrade_given
    )

    # --------------------------------------------------------
    # Guests
    # --------------------------------------------------------

    guest_count = determine_guest_count(
        room_type
    )

    occupancy_type = determine_occupancy_type(
        guest_count
    )

    # --------------------------------------------------------
    # Booking Source
    # --------------------------------------------------------

    booking_channel = determine_booking_channel(
        customer
    )

    booking_source = determine_booking_source(
        booking_channel
    )

    booking_status = determine_booking_status(
        customer,
        lead_time_days
    )

    # --------------------------------------------------------
    # Pricing
    # --------------------------------------------------------

    pricing = calculate_pricing(
        customer=customer,
        hotel=hotel,
        room_type=room_type,
        season=season,
        occupancy=occupancy,
        stay_nights=stay_nights,
        booking_channel=booking_channel,
        checkin_date=check_in_date,
        booking_status=booking_status
    )

    # --------------------------------------------------------
    # Cancellation Date
    # --------------------------------------------------------

    cancellation_date = None

    if booking_status == "Cancelled":

        cancellation_date = booking_date + timedelta(
            days=random.randint(
                1,
                max(1, lead_time_days - 1)
            )
        )

    # --------------------------------------------------------
    # Build Record
    # --------------------------------------------------------

    return create_booking_record(

        booking_id=booking_id,

        booking_sequence=booking_sequence,

        customer_id=customer_id,

        hotel_id=hotel["hotel_id"],

        booking_date=booking_date,

        booking_year=booking_date.year,

        booking_month=booking_date.month,

        booking_quarter=f"Q{((booking_date.month - 1) // 3) + 1}",

        lead_time_days=lead_time_days,

        check_in_date=check_in_date,

        check_out_date=check_out_date,

        stay_nights=stay_nights,

        season=season,

        room_type=room_type,

        guest_count=guest_count,

        occupancy_type=occupancy_type,

        booking_channel=booking_channel,

        booking_source=booking_source,

        booking_status=booking_status,

        booking_priority=booking_priority,

        demand_level=demand_level,

        available_rooms=available_rooms,

        upgrade_given=upgrade_given,

        cancellation_date=cancellation_date,

        created_at=datetime.now(),

        updated_at = datetime.now(),

        **pricing

    )

# ============================================================
# VALIDATION ENGINE
# ============================================================

def validate_bookings(
    bookings_df,
    customers_df,
    hotels_df
):
    """
    Validate generated booking dataset.

    Raises ValueError if any validation fails.
    """

    print("\nRunning Booking Validation...")

    # --------------------------------------------------------
    # Primary Key Validation
    # --------------------------------------------------------

    if bookings_df["booking_id"].duplicated().any():
        raise ValueError(
            "Duplicate Booking IDs found."
        )

    # --------------------------------------------------------
    # Foreign Key Validation
    # --------------------------------------------------------

    customer_ids = set(customers_df["customer_id"])

    invalid_customers = bookings_df[
        ~bookings_df["customer_id"].isin(customer_ids)
    ]

    if not invalid_customers.empty:

        raise ValueError(
            f"Invalid Customer IDs : {len(invalid_customers)}"
        )

    hotel_ids = set(hotels_df["hotel_id"])

    invalid_hotels = bookings_df[
        ~bookings_df["hotel_id"].isin(hotel_ids)
    ]

    if not invalid_hotels.empty:

        raise ValueError(
            f"Invalid Hotel IDs : {len(invalid_hotels)}"
        )

    # --------------------------------------------------------
    # Date Validation
    # --------------------------------------------------------

    invalid_dates = bookings_df[
        bookings_df["check_out_date"]
        <= bookings_df["check_in_date"]
    ]

    if not invalid_dates.empty:

        raise ValueError(
            "Checkout date must be after check-in date."
        )

    invalid_booking_dates = bookings_df[
        bookings_df["booking_date"]
        > bookings_df["check_in_date"]
    ]

    if not invalid_booking_dates.empty:

        raise ValueError(
            "Booking date occurs after check-in."
        )

    # --------------------------------------------------------
    # Stay Validation
    # --------------------------------------------------------

    if (bookings_df["stay_nights"] <= 0).any():

        raise ValueError(
            "Invalid stay duration detected."
        )

    # --------------------------------------------------------
    # Guest Validation
    # --------------------------------------------------------

    if (bookings_df["guest_count"] <= 0).any():

        raise ValueError(
            "Guest count cannot be zero."
        )

    if (bookings_df["guest_count"] > 4).any():

        raise ValueError(
            "Guest count exceeds room capacity."
        )

    # --------------------------------------------------------
    # Pricing Validation
    # --------------------------------------------------------

    money_columns = [

        "room_rate",

        "total_room_charges",

        "discount_amount",

        "tax_amount",

        "service_fee",

        "gross_amount",

        "net_amount"

    ]

    for column in money_columns:

        negative_values = bookings_df[
            bookings_df[column] < 0
        ]

        if not negative_values.empty:

            raise ValueError(
                f"Negative values found in {column}"
            )

    # --------------------------------------------------------
    # Discount Validation
    # --------------------------------------------------------

    invalid_discount = bookings_df[
        bookings_df["discount_percentage"] > 25
    ]

    if not invalid_discount.empty:

        raise ValueError(
            "Discount exceeds maximum allowed."
        )

    # --------------------------------------------------------
    # Cancellation Validation
    # --------------------------------------------------------

    cancelled = bookings_df[
        bookings_df["booking_status"] == "Cancelled"
    ]

    if not cancelled.empty:

        invalid_cancel = cancelled[
            cancelled["cancellation_date"].isna()
        ]

        if not invalid_cancel.empty:

            raise ValueError(
                "Cancelled bookings missing cancellation date."
            )

    # --------------------------------------------------------
    # Completed Booking Validation
    # --------------------------------------------------------

    completed = bookings_df[
        bookings_df["booking_status"] == "Completed"
    ]

    invalid_completed = completed[
        completed["cancellation_date"].notna()
    ]

    if not invalid_completed.empty:

        raise ValueError(
            "Completed bookings cannot have cancellation dates."
        )

    # --------------------------------------------------------
    # Null Validation
    # --------------------------------------------------------

    required_columns = [

        "booking_id",

        "customer_id",

        "hotel_id",

        "booking_date",

        "check_in_date",

        "check_out_date",

        "room_type",

        "booking_status",

        "gross_amount",

        "net_amount"

    ]

    for column in required_columns:

        if bookings_df[column].isnull().any():

            raise ValueError(
                f"Null values found in {column}"
            )

    # --------------------------------------------------------
    # Booking Sequence Validation
    # --------------------------------------------------------

    duplicate_sequence = bookings_df.duplicated(
        subset=[
            "customer_id",
            "booking_sequence"
        ]
    )

    if duplicate_sequence.any():

        raise ValueError(
            "Duplicate booking sequence detected."
        )

    print("Booking Validation Successful.")

    return True

# ============================================================
# BOOKING GENERATION ORCHESTRATOR
# ============================================================

def generate_bookings(
    customers_df,
    hotels_df,
    num_bookings=10000
):
    """
    Generate realistic hotel booking dataset.

    Parameters
    ----------
    customers_df : pd.DataFrame

    hotels_df : pd.DataFrame

    num_bookings : int

    Returns
    -------
    pd.DataFrame
    """

    print("\nStarting Booking Generation...")

    # --------------------------------------------------------
    # Build Lookups
    # --------------------------------------------------------

    customer_lookup = build_customer_lookup(
        customers_df
    )

    hotel_lookup = build_hotel_lookup(
        hotels_df
    )

    star_groups = build_star_groups(
        hotels_df
    )

    # --------------------------------------------------------
    # Customer Booking Plan
    # --------------------------------------------------------

    booking_plan = build_customer_booking_plan(
        customers_df,
        num_bookings
    )

    booking_tracker = prepare_booking_tracker(
        customers_df
    )

    # --------------------------------------------------------
    # Generate Records
    # --------------------------------------------------------

    booking_records = []

    for booking_number, customer_id in enumerate(
        booking_plan,
        start=1
    ):

        booking = build_booking_record(

            booking_number=booking_number,

            customer_id=customer_id,

            customer_lookup=customer_lookup,

            star_groups=star_groups,

            booking_tracker=booking_tracker

        )

        booking_records.append(
            booking
        )

    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    bookings_df = pd.DataFrame(
        booking_records
    )

    # --------------------------------------------------------
    # Data Type Standardization
    # --------------------------------------------------------

    date_columns = [

        "booking_date",

        "check_in_date",

        "check_out_date",

        "cancellation_date",

        "created_at",

        "updated_at"

    ]

    for column in date_columns:

        bookings_df[column] = pd.to_datetime(
            bookings_df[column]
        )

    numeric_columns = [

        "booking_sequence",

        "lead_time_days",

        "stay_nights",

        "guest_count",

        "available_rooms",

        "room_rate",

        "total_room_charges",

        "discount_percentage",

        "discount_amount",

        "tax_amount",

        "service_fee",

        "gross_amount",

        "net_amount"

    ]

    for column in numeric_columns:

        bookings_df[column] = pd.to_numeric(
            bookings_df[column]
        )

    # --------------------------------------------------------
    # Sorting
    # --------------------------------------------------------

    bookings_df = bookings_df.sort_values(

        [

            "booking_date",

            "booking_id"

        ]

    ).reset_index(

        drop=True

    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    validate_bookings(

        bookings_df,

        customers_df,

        hotels_df

    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    completed_count = len(
        bookings_df.loc[
            bookings_df["booking_status"] == "Completed"
            ]
    )

    cancelled_count = len(
        bookings_df.loc[
            bookings_df["booking_status"] == "Cancelled"
            ]
    )

    total_revenue = bookings_df["net_amount"].sum()

    print("\nBooking Generation Summary")
    print("-" * 40)
    print(f"Bookings  : {len(bookings_df):,}")
    print(f"Customers : {bookings_df['customer_id'].nunique():,}")
    print(f"Hotels    : {bookings_df['hotel_id'].nunique():,}")
    print(f"Completed : {completed_count:,}")
    print(f"Cancelled : {cancelled_count:,}")
    print(f"Revenue   : {total_revenue:,.2f}")
    print("-" * 40)

    return bookings_df