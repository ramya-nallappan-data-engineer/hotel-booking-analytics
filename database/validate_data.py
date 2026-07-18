from pathlib import Path

import duckdb

DATABASE_FILE = Path("database/hotel_booking.duckdb")

def get_connection():
    """
    Connect to DuckDB.
    """

    return duckdb.connect(DATABASE_FILE)

def validate_row_counts(connection):

    print("\nRow Count Validation")

    tables = [

        "customers",
        "hotels",
        "products",
        "bookings",
        "payments",
        "reviews",
        "order_items"

    ]

    for table in tables:

        rows = connection.execute(
            f"""
            SELECT COUNT(*)
            FROM {table}
            """
        ).fetchone()[0]

        print(
            f"{table:<15}{rows:>10,}"
        )

def validate_primary_keys(connection):

    print("\nPrimary Key Validation")

    validations = {

        "customers":
            "customer_id",

        "hotels":
            "hotel_id",

        "products":
            "product_id",

        "bookings":
            "booking_id",

        "payments":
            "payment_id",

        "reviews":
            "review_id",

        "order_items":
            "order_item_id"

    }

    for table, key in validations.items():

        duplicates = connection.execute(
            f"""
            SELECT COUNT(*)

            FROM

            (

            SELECT
                {key},
                COUNT(*)

            FROM {table}

            GROUP BY {key}

            HAVING COUNT(*) > 1

            )

            """
        ).fetchone()[0]

        print(
            f"{table:<15}{duplicates} duplicates"
        )

def validate_foreign_keys(connection):

    print("\nForeign Key Validation")

    checks = [

        (
            "bookings",
            "customer_id",
            "customers",
            "customer_id"
        ),

        (
            "bookings",
            "hotel_id",
            "hotels",
            "hotel_id"
        ),

        (
            "payments",
            "booking_id",
            "bookings",
            "booking_id"
        ),

        (
            "payments",
            "customer_id",
            "customers",
            "customer_id"
        ),

        (
            "reviews",
            "booking_id",
            "bookings",
            "booking_id"
        ),

        (
            "reviews",
            "hotel_id",
            "hotels",
            "hotel_id"
        ),

        (
            "order_items",
            "booking_id",
            "bookings",
            "booking_id"
        ),

        (
            "order_items",
            "product_id",
            "products",
            "product_id"
        )

    ]

    for child, fk, parent, pk in checks:

        orphans = connection.execute(
            f"""
            SELECT COUNT(*)

            FROM {child} c

            LEFT JOIN {parent} p

            ON c.{fk}=p.{pk}

            WHERE p.{pk} IS NULL
            """
        ).fetchone()[0]

        print(
            f"{child}.{fk:<20}{orphans}"
        )

def validate_nulls(connection):

    print("\nNull Validation")

    columns = [

        ("customers", "customer_id"),

        ("hotels", "hotel_id"),

        ("products", "product_id"),

        ("bookings", "booking_id"),

        ("payments", "payment_id"),

        ("reviews", "review_id"),

        ("order_items", "order_item_id")

    ]

    for table, column in columns:

        nulls = connection.execute(
            f"""
            SELECT COUNT(*)

            FROM {table}

            WHERE {column} IS NULL
            """
        ).fetchone()[0]

        print(
            f"{table:<15}{nulls} null keys"
        )

def validate_business_rules(connection):

    print("\nBusiness Rule Validation")

    completed_without_payment = connection.execute(
        """
        SELECT COUNT(*)

        FROM bookings b

        LEFT JOIN payments p

        ON b.booking_id=p.booking_id

        WHERE

        b.booking_status='Completed'

        AND

        p.booking_id IS NULL
        """
    ).fetchone()[0]

    print(
        f"Completed bookings without payment : {completed_without_payment}"
    )

    negative_amounts = connection.execute(
        """
        SELECT COUNT(*)

        FROM payments

        WHERE

        gross_amount < 0

        OR final_amount < 0

        OR refund_amount < 0
        """
    ).fetchone()[0]

    print(
        f"Negative payment amounts : {negative_amounts}"
    )

    invalid_reviews = connection.execute(
        """
        SELECT COUNT(*)

        FROM reviews

        WHERE rating NOT BETWEEN 1 AND 5
        """
    ).fetchone()[0]

    print(
        f"Invalid review ratings : {invalid_reviews}"
    )

def main():

    print("="*60)
    print("DATABASE VALIDATION")
    print("="*60)

    connection = get_connection()

    validate_row_counts(connection)

    validate_primary_keys(connection)

    validate_foreign_keys(connection)

    validate_nulls(connection)

    validate_business_rules(connection)

    connection.close()

    print("\nValidation Completed Successfully.")


if __name__ == "__main__":
    main()