import random
import string
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from config import (
    DEFAULT_CURRENCY,
    PAYMENT_GATEWAYS,
    PAYMENT_GATEWAY_FEES,
    PAYMENT_PROVIDER_MAPPING,
    SETTLEMENT_DAYS,
)

# ---------------------------------------------------------------------
# Section 1 - Foundation
# ---------------------------------------------------------------------


def build_customer_lookup(
    customers_df: pd.DataFrame
) -> dict[str, dict[str, Any]]:
    """
    Build a customer lookup dictionary keyed by customer_id.

    Parameters
    ----------
    customers_df : pd.DataFrame

    Returns
    -------
    dict
        {
            customer_id: customer_record
        }
    """

    return customers_df.set_index(
        "customer_id"
    ).to_dict("index")


def generate_payment_id(
    payment_number: int
) -> str:
    """
    Generate sequential payment ID.

    Example
    -------
    PAY000001
    """

    return f"PAY{payment_number:06}"


def generate_transaction_reference(
    length: int = 14
) -> str:
    """
    Generate a random payment transaction reference.

    Example
    -------
    7GX91PQK82LMA3
    """

    alphabet = (
        string.ascii_uppercase +
        string.digits
    )

    return "".join(
        random.choices(
            alphabet,
            k=length
        )
    )


def calculate_settlement_date(
    payment_date: datetime,
    settlement_days: int
) -> datetime:
    """
    Calculate settlement date based on
    payment gateway settlement period.
    """

    return payment_date + timedelta(
        days=settlement_days
    )


def create_payment_record(
    **kwargs
) -> dict[str, Any]:
    """
    Create a payment record.

    This wrapper keeps record creation
    centralized so additional fields can
    be introduced without changing the
    orchestration logic.
    """

    return kwargs

# ---------------------------------------------------------------------
# Section 2 - Payment Behaviour Engine
# ---------------------------------------------------------------------


def determine_payment_method(
    customer: dict[str, Any]
) -> str:
    """
    Determine payment method based on
    customer loyalty tier and traveller profile.
    """

    loyalty_tier = customer["loyalty_tier"]
    traveler_type = customer["traveler_type"]

    if loyalty_tier == "Platinum":
        return random.choices(
            population=[
                "Corporate Billing",
                "Credit Card",
                "Debit Card"
            ],
            weights=[45, 45, 10],
            k=1
        )[0]

    if loyalty_tier == "Gold":
        return random.choices(
            population=[
                "Credit Card",
                "Debit Card",
                "UPI"
            ],
            weights=[55, 25, 20],
            k=1
        )[0]

    if loyalty_tier == "Silver":
        return random.choices(
            population=[
                "Debit Card",
                "UPI",
                "Wallet"
            ],
            weights=[45, 40, 15],
            k=1
        )[0]

    if traveler_type == "Frequent":
        return random.choices(
            population=[
                "Credit Card",
                "Corporate Billing",
                "UPI"
            ],
            weights=[50, 30, 20],
            k=1
        )[0]

    return random.choices(
        population=[
            "UPI",
            "Debit Card",
            "Wallet",
            "Cash"
        ],
        weights=[45, 30, 15, 10],
        k=1
    )[0]


def determine_payment_provider(
    payment_method: str
) -> str:
    """
    Select payment provider for
    the chosen payment method.
    """

    return random.choice(
        PAYMENT_PROVIDER_MAPPING[payment_method]
    )


def determine_payment_gateway() -> str:
    """
    Determine payment gateway used
    for processing the transaction.
    """

    return random.choices(
        population=PAYMENT_GATEWAYS,
        weights=[35, 35, 20, 10],
        k=1
    )[0]


def determine_payment_status(
    booking: dict[str, Any]
) -> str:
    """
    Determine payment status
    based on booking outcome.
    """

    booking_status = booking["booking_status"]

    if booking_status == "Cancelled":
        return random.choices(
            population=[
                "Refunded",
                "Pending"
            ],
            weights=[95, 5],
            k=1
        )[0]

    return random.choices(
        population=[
            "Successful",
            "Pending",
            "Failed"
        ],
        weights=[96, 3, 1],
        k=1
    )[0]


def determine_payment_type(
    customer: dict[str, Any]
) -> str:
    """
    Determine whether the booking
    is paid fully or partially.
    """

    if customer["traveler_type"] == "Frequent":
        return random.choices(
            population=[
                "Full",
                "Partial"
            ],
            weights=[85, 15],
            k=1
        )[0]

    return random.choices(
        population=[
            "Full",
            "Partial"
        ],
        weights=[95, 5],
        k=1
    )[0]


def generate_payment_date(
    booking_date: datetime,
    payment_method: str
) -> datetime:
    """
    Generate a realistic payment date
    based on the payment method.
    """

    if payment_method == "Corporate Billing":
        delay = random.randint(5, 15)

    elif payment_method == "Cash":
        delay = random.randint(0, 1)

    else:
        delay = random.randint(0, 3)

    return booking_date + timedelta(
        days=delay
    )


def determine_settlement_days(
    payment_gateway: str
) -> int:
    """
    Return settlement period
    for the selected payment gateway.
    """

    return SETTLEMENT_DAYS[
        payment_gateway
    ]


def determine_processing_fee_percentage(
    payment_gateway: str
) -> float:
    """
    Return gateway processing fee percentage.
    """

    return PAYMENT_GATEWAY_FEES[
        payment_gateway
    ]

# ---------------------------------------------------------------------
# Section 3 - Payment Calculation Engine
# ---------------------------------------------------------------------


def calculate_gross_amount(
    booking: dict[str, Any]
) -> float:
    """
    Return the gross booking amount.

    This represents the total room charge before
    any payment gateway deductions or refunds.
    """

    return round(
        booking["gross_amount"],
        2
    )


def calculate_discount_amount(
    booking: dict[str, Any]
) -> float:
    """
    Return the discount applied
    to the booking.
    """

    return round(
        booking["discount_amount"],
        2
    )


def calculate_tax_amount(
    booking: dict[str, Any]
) -> float:
    """
    Return the tax charged
    for the booking.
    """

    return round(
        booking["tax_amount"],
        2
    )


def calculate_processing_fee(
    gross_amount: float,
    gateway_fee_percentage: float
) -> float:
    """
    Calculate payment gateway processing fee.

    Processing Fee =
        Gross Amount × Gateway Fee %
    """

    return round(
        gross_amount *
        gateway_fee_percentage / 100,
        2
    )


def calculate_refund_amount(
    booking: dict[str, Any],
    payment_status: str
) -> float:
    """
    Calculate customer refund.

    Refunded Amount =
        Gross Amount - Cancellation Fee
    """

    if payment_status != "Refunded":
        return 0.0

    refund_amount = (
        booking["gross_amount"] -
        booking["net_amount"]
    )

    return round(
        max(refund_amount, 0),
        2
    )


def calculate_final_amount(
    booking: dict[str, Any],
    payment_status: str
) -> float:
    """
    Calculate the final amount retained
    after payment processing.

    Successful
        -> Gross Amount

    Refunded
        -> Cancellation Fee retained

    Failed
        -> 0

    Pending
        -> 0
    """

    if payment_status == "Successful":
        return round(
            booking["gross_amount"],
            2
        )

    if payment_status == "Refunded":
        refund_amount = round(
            booking["net_amount"] * random.uniform(0.3, 1.0),
            2
        )
    else:
        refund_amount = 1.0

    return 0.0


def determine_currency() -> str:
    """
    Return default payment currency.
    """

    return DEFAULT_CURRENCY


def calculate_payment_settlement(
    payment_date: datetime,
    settlement_days: int
) -> datetime:
    """
    Calculate payment settlement date.
    """

    return calculate_settlement_date(
        payment_date,
        settlement_days
    )

# ---------------------------------------------------------------------
# Section 4 - Payment Record Builder
# ---------------------------------------------------------------------


def build_payment_record(
    payment_number: int,
    booking: dict[str, Any],
    customer_lookup: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    """
    Build a complete payment record.

    This function orchestrates the payment generation process by
    combining customer information, payment behaviour, financial
    calculations, and audit information into a single payment record.

    Parameters
    ----------
    payment_number : int
        Sequential payment number.

    booking : dict
        Booking record.

    customer_lookup : dict
        Customer lookup keyed by customer_id.

    Returns
    -------
    dict
        Complete payment record.
    """

    # -------------------------------------------------------------
    # Customer Information
    # -------------------------------------------------------------

    customer = customer_lookup[
        booking["customer_id"]
    ]

    # -------------------------------------------------------------
    # Payment Identifiers
    # -------------------------------------------------------------

    payment_id = generate_payment_id(
        payment_number
    )

    transaction_reference = (
        generate_transaction_reference()
    )

    # -------------------------------------------------------------
    # Payment Behaviour
    # -------------------------------------------------------------

    payment_method = determine_payment_method(
        customer
    )

    payment_provider = determine_payment_provider(
        payment_method
    )

    payment_gateway = determine_payment_gateway()

    payment_status = determine_payment_status(
        booking
    )

    payment_type = determine_payment_type(
        customer
    )

    payment_date = generate_payment_date(
        booking_date=booking["booking_date"],
        payment_method=payment_method
    )

    settlement_days = determine_settlement_days(
        payment_gateway
    )

    gateway_fee_percentage = (
        determine_processing_fee_percentage(
            payment_gateway
        )
    )

    # -------------------------------------------------------------
    # Financial Calculations
    # -------------------------------------------------------------

    gross_amount = calculate_gross_amount(
        booking
    )

    discount_amount = calculate_discount_amount(
        booking
    )

    tax_amount = calculate_tax_amount(
        booking
    )

    processing_fee = calculate_processing_fee(
        gross_amount=gross_amount,
        gateway_fee_percentage=(
            gateway_fee_percentage
        )
    )

    refund_amount = calculate_refund_amount(
        booking=booking,
        payment_status=payment_status
    )

    final_amount = calculate_final_amount(
        booking=booking,
        payment_status=payment_status
    )

    currency = determine_currency()

    settlement_date = calculate_payment_settlement(
        payment_date=payment_date,
        settlement_days=settlement_days
    )

    # -------------------------------------------------------------
    # Audit Information
    # -------------------------------------------------------------

    audit_timestamp = datetime.now()

    # -------------------------------------------------------------
    # Build Payment Record
    # -------------------------------------------------------------

    return create_payment_record(

        payment_id=payment_id,

        booking_id=booking["booking_id"],

        customer_id=booking["customer_id"],

        payment_date=payment_date,

        payment_method=payment_method,

        payment_provider=payment_provider,

        payment_gateway=payment_gateway,

        payment_status=payment_status,

        payment_type=payment_type,

        currency=currency,

        transaction_reference=transaction_reference,

        gross_amount=gross_amount,

        discount_amount=discount_amount,

        tax_amount=tax_amount,

        processing_fee=processing_fee,

        refund_amount=refund_amount,

        final_amount=final_amount,

        settlement_days=settlement_days,

        settlement_date=settlement_date,

        created_at=audit_timestamp,

        updated_at=audit_timestamp
    )

# ---------------------------------------------------------------------
# Section 5 - Validation Engine
# ---------------------------------------------------------------------



def validate_payments(
    payments_df: pd.DataFrame,
    bookings_df: pd.DataFrame,
    customers_df: pd.DataFrame
) -> dict[str, Any]:
    """
    Validate generated payment dataset.

    Parameters
    ----------
    payments_df : pd.DataFrame

    bookings_df : pd.DataFrame

    customers_df : pd.DataFrame

    Returns
    -------
    dict
        Validation summary.

    Raises
    ------
    ValueError
        If any validation fails.
    """

    print("\nRunning Payment Validation...")

    # -------------------------------------------------------------
    # Primary Key Validation
    # -------------------------------------------------------------

    if payments_df["payment_id"].duplicated().any():
        raise ValueError(
            "Duplicate payment IDs found."
        )

    if payments_df["transaction_reference"].duplicated().any():
        raise ValueError(
            "Duplicate transaction references found."
        )

    if payments_df["booking_id"].duplicated().any():
        raise ValueError(
            "Multiple payments found for the same booking."
        )

    # -------------------------------------------------------------
    # Foreign Key Validation
    # -------------------------------------------------------------

    booking_ids = set(
        bookings_df["booking_id"]
    )

    customer_ids = set(
        customers_df["customer_id"]
    )

    if not payments_df["booking_id"].isin(
        booking_ids
    ).all():
        raise ValueError(
            "Invalid booking IDs found."
        )

    if not payments_df["customer_id"].isin(
        customer_ids
    ).all():
        raise ValueError(
            "Invalid customer IDs found."
        )

    # -------------------------------------------------------------
    # Date Validation
    # -------------------------------------------------------------

    booking_dates = (
        bookings_df
        .set_index("booking_id")
        ["booking_date"]
    )

    merged = payments_df.copy()

    merged["booking_date"] = (
        merged["booking_id"]
        .map(booking_dates)
    )

    invalid_payment_dates = merged[
        merged["payment_date"] <
        merged["booking_date"]
    ]

    if not invalid_payment_dates.empty:
        raise ValueError(
            "Payment date cannot be earlier than booking date."
        )

    invalid_settlement = payments_df[
        payments_df["settlement_date"] <
        payments_df["payment_date"]
    ]

    if not invalid_settlement.empty:
        raise ValueError(
            "Settlement date cannot be earlier than payment date."
        )

    # -------------------------------------------------------------
    # Financial Validation
    # -------------------------------------------------------------

    money_columns = [
        "gross_amount",
        "discount_amount",
        "tax_amount",
        "processing_fee",
        "refund_amount",
        "final_amount"
    ]

    for column in money_columns:

        if (payments_df[column] < 0).any():
            raise ValueError(
                f"Negative values found in '{column}'."
            )

    invalid_refund = payments_df[
        payments_df["refund_amount"] >
        payments_df["gross_amount"]
    ]

    if not invalid_refund.empty:
        raise ValueError(
            "Refund amount exceeds gross amount."
        )

    # -------------------------------------------------------------
    # Payment Status Validation
    # -------------------------------------------------------------

    successful = payments_df[
        payments_df["payment_status"] == "Successful"
    ]

    if (successful["final_amount"] <= 0).any():
        raise ValueError(
            "Successful payments must have a positive final amount."
        )

    failed = payments_df[
        payments_df["payment_status"] == "Failed"
    ]

    if (failed["final_amount"] != 0).any():
        raise ValueError(
            "Failed payments must have zero final amount."
        )

    pending = payments_df[
        payments_df["payment_status"] == "Pending"
    ]

    if (pending["final_amount"] != 0).any():
        raise ValueError(
            "Pending payments must have zero final amount."
        )

    refunded = payments_df[
        payments_df["payment_status"] == "Refunded"
    ]

    invalid_refunded = refunded[
        refunded["refund_amount"] < 0
    ]

    if not invalid_refunded.empty:
        raise ValueError(
            "Refunded payments must have a refund amount."
        )

    # -------------------------------------------------------------
    # Null Validation
    # -------------------------------------------------------------

    required_columns = [
        "payment_id",
        "booking_id",
        "customer_id",
        "payment_date",
        "payment_method",
        "payment_provider",
        "payment_gateway",
        "payment_status",
        "payment_type",
        "currency",
        "transaction_reference",
        "gross_amount",
        "discount_amount",
        "tax_amount",
        "processing_fee",
        "refund_amount",
        "final_amount",
        "settlement_days",
        "settlement_date",
        "created_at",
        "updated_at"
    ]

    for column in required_columns:

        if payments_df[column].isnull().any():
            raise ValueError(
                f"Null values found in '{column}'."
            )

    # -------------------------------------------------------------
    # Validation Summary
    # -------------------------------------------------------------

    summary = {

        "total_payments": len(
            payments_df
        ),

        "successful": len(
            successful
        ),

        "refunded": len(
            refunded
        ),

        "pending": len(
            pending
        ),

        "failed": len(
            failed
        ),

        "total_amount": round(
            payments_df["final_amount"].sum(),
            2
        ),

        "total_refund": round(
            payments_df["refund_amount"].sum(),
            2
        )

    }

    print("Payment Validation Successful.")

    return summary

# ---------------------------------------------------------------------
# Section 6 - Payment Generator
# ---------------------------------------------------------------------


def generate_payments(
    bookings_df: pd.DataFrame,
    customers_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate payment records for all bookings.

    Parameters
    ----------
    bookings_df : pd.DataFrame
        Booking dataset.

    customers_df : pd.DataFrame
        Customer dataset.

    Returns
    -------
    pd.DataFrame
        Payment dataset.
    """

    print("\nStarting Payment Generation...")

    # -------------------------------------------------------------
    # Build Lookup Tables
    # -------------------------------------------------------------

    customer_lookup = build_customer_lookup(
        customers_df
    )

    # -------------------------------------------------------------
    # Generate Payment Records
    # -------------------------------------------------------------

    payment_records = []

    for payment_number, (_, booking) in enumerate(
        bookings_df.iterrows(),
        start=1
    ):

        payment_records.append(

            build_payment_record(
                payment_number=payment_number,
                booking=booking.to_dict(),
                customer_lookup=customer_lookup
            )

        )

    # -------------------------------------------------------------
    # Create DataFrame
    # -------------------------------------------------------------

    payments_df = pd.DataFrame(
        payment_records
    )

    # -------------------------------------------------------------
    # Standardize Data Types
    # -------------------------------------------------------------

    date_columns = [
        "payment_date",
        "settlement_date",
        "created_at",
        "updated_at"
    ]

    for column in date_columns:

        payments_df[column] = pd.to_datetime(
            payments_df[column]
        )

    numeric_columns = [
        "gross_amount",
        "discount_amount",
        "tax_amount",
        "processing_fee",
        "refund_amount",
        "final_amount",
        "settlement_days"
    ]

    for column in numeric_columns:

        payments_df[column] = pd.to_numeric(
            payments_df[column]
        )

    # -------------------------------------------------------------
    # Sort Dataset
    # -------------------------------------------------------------

    payments_df = (

        payments_df

        .sort_values(
            by=[
                "payment_date",
                "payment_id"
            ]
        )

        .reset_index(
            drop=True
        )

    )

    # -------------------------------------------------------------
    # Validate Dataset
    # -------------------------------------------------------------

    print(
        payments_df.loc[
            (payments_df["payment_status"] == "Refunded") &
            (
                    payments_df["refund_amount"].isna() |
                    (payments_df["refund_amount"] == 0)
            )
            ][[
            "payment_id",
            "booking_id",
            "payment_status",
            "refund_amount",
            "final_amount"
        ]]
    )

    validation_summary = validate_payments(
        payments_df=payments_df,
        bookings_df=bookings_df,
        customers_df=customers_df
    )

    # -------------------------------------------------------------
    # Print Summary
    # -------------------------------------------------------------

    print("\nPayment Generation Summary")
    print("-" * 45)

    print(
        f"Total Payments : "
        f"{validation_summary['total_payments']:,}"
    )

    print(
        f"Successful     : "
        f"{validation_summary['successful']:,}"
    )

    print(
        f"Refunded       : "
        f"{validation_summary['refunded']:,}"
    )

    print(
        f"Pending        : "
        f"{validation_summary['pending']:,}"
    )

    print(
        f"Failed         : "
        f"{validation_summary['failed']:,}"
    )

    print(
        f"Revenue        : ₹"
        f"{validation_summary['total_amount']:,.2f}"
    )

    print(
        f"Refund Amount  : ₹"
        f"{validation_summary['total_refund']:,.2f}"
    )

    print("-" * 45)

    return payments_df