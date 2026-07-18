import random
from faker import Faker
from datetime import datetime

fake = Faker()

Faker.seed(42)

# ============================================================
# RECORD COUNTS
# ============================================================

# Dataset Size
NUM_CUSTOMERS = 500
NUM_HOTELS = 100
NUM_PRODUCTS = 30
NUM_BOOKINGS = 10000

# Customer Attributes
GENDERS = [
    "Male",
    "Female"
]

LOYALTY_TIERS = [
    "Bronze",
    "Silver",
    "Gold",
    "Platinum"
]

LOYALTY_WEIGHTS = [
    50,
    25,
    18,
    7
]

CUSTOMER_SEGMENTS = [
    "Business",
    "Leisure"
]

CUSTOMER_SEGMENT_WEIGHTS = [
    35,
    65
]

SIGNUP_CHANNELS = [
    "Website",
    "Mobile App",
    "Corporate"
]

SIGNUP_CHANNEL_WEIGHTS = [
    45,
    45,
    10
]

ROOM_TYPES = [
    "Standard",
    "Deluxe",
    "Suite"
]

ROOM_TYPE_WEIGHTS = {
    3: [75, 20, 5],
    4: [40, 40, 20],
    5: [20, 40, 40]
}

BOOKING_CHANNELS = [
    "Website",
    "Mobile App",
    "Travel Agent",
    "Corporate"
]

BOOKING_CHANNEL_WEIGHTS = [
    40,
    35,
    15,
    10
]

DISCOUNTS = [
    0,
    5,
    10,
    15,
    20
]

DISCOUNT_WEIGHTS = [
    55,
    20,
    12,
    8,
    5
]

HOTEL_CHAINS = [
    "Hilton",
    "Marriott",
    "Hyatt",
    "Radisson",
    "Holiday Inn",
    "Novotel",
    "Taj",
    "Independent"
]

HOTEL_CHAIN_WEIGHTS = [
    10,
    12,
    8,
    10,
    10,
    10,
    15,
    25
]

LANGUAGES = {

        "Netherlands": "Dutch",

        "Germany": "German",

        "France": "French",

        "Spain": "Spanish",

        "Italy": "Italian",

        "United Kingdom": "English",

        "Singapore": "English",

        "UAE": "Arabic",

        "India": "English"

    }

ROOM_TYPE_MULTIPLIERS = {
    "Standard": 1.00,
    "Deluxe": 1.40,
    "Suite": 2.20
}

SEASON_MULTIPLIERS = {

    1: 1.00,   # Jan
    2: 0.95,
    3: 1.00,
    4: 1.05,
    5: 1.10,
    6: 1.15,
    7: 1.20,
    8: 1.20,
    9: 1.05,
    10: 1.10,
    11: 1.10,
    12: 1.30

}

WEEKEND_MULTIPLIER = 1.15

MAX_STAY_NIGHTS = {
    "Business": (1,3),
    "Leisure": (2,7)
}

# ============================================================
# CITY - COUNTRY MAPPING
# ============================================================

LOCATIONS = [
    ("Amsterdam", "Netherlands"),
    ("Rotterdam", "Netherlands"),
    ("Utrecht", "Netherlands"),
    ("Berlin", "Germany"),
    ("Munich", "Germany"),
    ("Hamburg", "Germany"),
    ("Paris", "France"),
    ("Lyon", "France"),
    ("Barcelona", "Spain"),
    ("Madrid", "Spain"),
    ("Rome", "Italy"),
    ("Milan", "Italy"),
    ("London", "United Kingdom"),
    ("Manchester", "United Kingdom"),
    ("Singapore", "Singapore"),
    ("Dubai", "UAE"),
    ("Bangalore", "India"),
    ("Chennai", "India")
]

# ============================================================
# HOTEL NAMES
# ============================================================

HOTEL_PREFIXES = [
    "Grand",
    "Royal",
    "Elite",
    "Golden",
    "Blue",
    "Palm",
    "Ocean",
    "Imperial",
    "Regency",
    "Sunrise"
]

HOTEL_SUFFIXES = [
    "Hotel",
    "Resort",
    "Suites",
    "Palace",
    "Inn",
    "Residency"
]

HOTEL_ROOM_COUNT = [
    (40,80),
    (81,120),
    (121,180),
    (181,250),
    (251,400)
]

FACILITY_WEIGHTS = {
    "spa": 35,
    "pool": 55,
    "gym": 70
}

# ============================================================
# PRODUCTS (Hotel Services)
# ============================================================

PRODUCTS = [

    # Food & Beverage
    ("Breakfast Buffet", "Food", 20),
    ("Lunch Buffet", "Food", 30),
    ("Dinner Buffet", "Food", 35),
    ("Mini Bar", "Food", 18),
    ("Coffee", "Food", 8),
    ("Wine Bottle", "Food", 45),

    # Wellness
    ("Spa", "Wellness", 60),
    ("Massage", "Wellness", 80),
    ("Sauna", "Wellness", 25),
    ("Yoga Session", "Wellness", 30),

    # Transport
    ("Airport Pickup", "Transport", 40),
    ("Airport Drop", "Transport", 35),
    ("Taxi Booking", "Transport", 25),
    ("City Tour", "Transport", 70),

    # Room Services
    ("Extra Bed", "Room", 25),
    ("Late Checkout", "Room", 30),
    ("Early Check-in", "Room", 20),
    ("Room Decoration", "Room", 50),

    # Laundry
    ("Laundry", "Laundry", 15),
    ("Dry Cleaning", "Laundry", 20),

    # Entertainment
    ("Swimming Pool", "Entertainment", 15),
    ("Gym Access", "Entertainment", 12),
    ("Bicycle Rental", "Entertainment", 20),
    ("Kids Play Area", "Entertainment", 18),

    # Premium
    ("Executive Lounge", "Premium", 90),
    ("Private Dining", "Premium", 120),
    ("Conference Room", "Premium", 150),
    ("Business Center", "Premium", 35),
    ("VIP Airport Transfer", "Premium", 180),
    ("Helicopter Tour", "Premium", 500)
]

PRODUCT_VENDORS = [
    "Hotel Supply Co",
    "Fresh Foods Ltd",
    "Wellness Partners",
    "Travel Services",
    "Luxury Essentials"
]

DEFAULT_TAX_PERCENTAGE = 10

# ============================================================
# BOOKING STATUS
# ============================================================

BOOKING_STATUS_WEIGHTS = [
    0.80,
    0.10,
    0.10
]

ROOM_PRICE_BY_STAR = {
    1: 70,
    2: 100,
    3: 150,
    4: 250,
    5: 400
}

# ============================================================
# PAYMENT
# ============================================================

# ============================================================
# PAYMENT CONFIGURATION
# ============================================================

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking",
    "Wallet",
    "Cash",
    "Corporate Billing"
]

PAYMENT_STATUS = [
    "Successful",
    "Refunded",
    "Pending",
    "Failed"
]

PAYMENT_TYPES = [
    "Full",
    "Partial"
]

PAYMENT_GATEWAYS = [
    "Stripe",
    "Razorpay",
    "PayU",
    "PayPal"
]

PAYMENT_GATEWAY_FEES = {
    "Stripe": 2.90,
    "Razorpay": 2.00,
    "PayU": 1.80,
    "PayPal": 3.50
}

PAYMENT_PROVIDER_MAPPING = {

    "Credit Card": [
        "Visa",
        "Mastercard",
        "Amex"
    ],

    "Debit Card": [
        "Visa Debit",
        "RuPay",
        "Mastercard Debit"
    ],

    "UPI": [
        "Google Pay",
        "PhonePe",
        "Paytm"
    ],

    "Wallet": [
        "Amazon Pay",
        "Mobikwik"
    ],

    "Net Banking": [
        "HDFC",
        "ICICI",
        "SBI"
    ],

    "Cash": [
        "Front Desk"
    ],

    "Corporate Billing": [
        "Corporate Account"
    ]
}

SETTLEMENT_DAYS = {
    "Stripe": 2,
    "Razorpay": 1,
    "PayU": 2,
    "PayPal": 3
}

DEFAULT_CURRENCY = "INR"

CURRENCIES = [
    "EUR",
    "GBP",
    "USD",
    "INR"
]

CURRENCY_WEIGHTS = [
    55,
    15,
    15,
    15
]

REFUND_REASONS = [
    "Customer Cancellation",
    "Duplicate Booking",
    "Hotel Issue",
    "Payment Failure",
    "No Refund"
]

BOOKING_SOURCES = [

    "Direct",

    "OTA",

    "Corporate"

]

PAYMENT_GATEWAY_WEIGHTS = [

    30,

    20,

    20,

    30

]

GST_PERCENTAGE = 12.0
SERVICE_FEE_PERCENTAGE = 5.0
MAX_DISCOUNT_PERCENTAGE = 25
MARKET_VARIATION_RANGE = (0.95, 1.05)
CANCELLATION_FEE_RATE = 0.20

# ============================================================
# REVIEWS
# ============================================================

REVIEW_COMMENTS = [
    "Excellent stay.",
    "Very clean rooms.",
    "Friendly staff.",
    "Amazing breakfast.",
    "Would definitely return.",
    "Average experience.",
    "Great location.",
    "Highly recommended.",
    "Room was spacious.",
    "Value for money."
]

REVIEW_RATINGS = [1, 2, 3, 4, 5]

REVIEW_RATING_WEIGHTS = [
    5,
    10,
    15,
    30,
    40
]

REVIEW_SENTIMENT = [
    "Positive",
    "Neutral",
    "Negative"
]

REVIEW_TITLES = [
    "Excellent Stay",
    "Great Experience",
    "Very Comfortable",
    "Good Value",
    "Average Stay",
    "Needs Improvement",
    "Fantastic Service",
    "Highly Recommended",
    "Wonderful Staff",
    "Clean & Comfortable"
]

TRAVELER_TYPES = [
    "Frequent",
    "Regular",
    "Casual"
]

TRAVELER_TYPE_WEIGHTS = [
    10,
    30,
    60
]

HOTEL_STAR_RATINGS = [

    3,

    4,

    5

]

HOTEL_STAR_WEIGHTS = [

    45,

    35,

    20

]

HOTEL_TYPES = [
    "Business",
    "City",
    "Airport",
    "Resort"
]

HOTEL_STATUS = [
    "Active",
    "Renovation",
    "Closed"
]

HOTEL_STATUS_WEIGHTS = [
    96,
    2,
    2
]