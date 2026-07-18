from pathlib import Path
import duckdb

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_ROOT / "database" / "interview.db"

# ============================================================
# CONNECTION
# ============================================================

def get_connection():
    return duckdb.connect(str(DATABASE_FILE))

# ============================================================
# ROW COUNTS
# ============================================================

def validate_row_counts(connection):

    print("\n📊 Row Count Validation")
    print("-" * 60)

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
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"✓ {table:<15}{rows:>10,}")

# ============================================================
# PRIMARY KEYS
# ============================================================

def validate_primary_keys(connection):

    print("\n🔑 Primary Key Validation")
    print("-" * 60)

    validations = {

        "customers": "customer_id",
        "hotels": "hotel_id",
        "products": "product_id",
        "bookings": "booking_id",
        "payments": "payment_id",
        "reviews": "review_id",
        "order_items": "order_item_id"

    }

    for table, key in validations.items():

        duplicates = connection.execute(f"""
            SELECT COUNT(*)
            FROM (
                SELECT {key}
                FROM {table}
                GROUP BY {key}
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        if duplicates == 0:
            print(f"✓ {table:<15}No duplicates")
        else:
            print(f"✗ {table:<15}{duplicates} duplicate keys")

# ============================================================
# FOREIGN KEYS
# ============================================================

def validate_foreign_keys(connection):

    print("\n🔗 Foreign Key Validation")
    print("-" * 60)

    checks = [

        ("bookings", "customer_id", "customers", "customer_id"),
        ("bookings", "hotel_id", "hotels", "hotel_id"),
        ("payments", "booking_id", "bookings", "booking_id"),
        ("payments", "customer_id", "customers", "customer_id"),
        ("reviews", "booking_id", "bookings", "booking_id"),
        ("reviews", "hotel_id", "hotels", "hotel_id"),
        ("order_items", "booking_id", "bookings", "booking_id"),
        ("order_items", "product_id", "products", "product_id")

    ]

    for child, fk, parent, pk in checks:

        orphans = connection.execute(f"""
            SELECT COUNT(*)
            FROM {child} c
            LEFT JOIN {parent} p
            ON c.{fk}=p.{pk}
            WHERE p.{pk} IS NULL
        """).fetchone()[0]

        if orphans == 0:
            print(f"✓ {child}.{fk:<20}OK")
        else:
            print(f"✗ {child}.{fk:<20}{orphans} orphan rows")

# ============================================================
# NULL KEYS
# ============================================================

def validate_nulls(connection):

    print("\n🚫 Null Primary Keys")
    print("-" * 60)

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

        nulls = connection.execute(f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE {column} IS NULL
        """).fetchone()[0]

        if nulls == 0:
            print(f"✓ {table:<15}No null keys")
        else:
            print(f"✗ {table:<15}{nulls} null keys")

# ============================================================
# BUSINESS RULES
# ============================================================

def validate_business_rules(connection):

    print("\n🏨 Business Rule Validation")
    print("-" * 60)

    completed_without_payment = connection.execute("""
        SELECT COUNT(*)
        FROM bookings b
        LEFT JOIN payments p
        ON b.booking_id = p.booking_id
        WHERE b.booking_status='Completed'
        AND p.booking_id IS NULL
    """).fetchone()[0]

    negative_amounts = connection.execute("""
        SELECT COUNT(*)
        FROM payments
        WHERE gross_amount < 0
        OR final_amount < 0
        OR refund_amount < 0
    """).fetchone()[0]

    invalid_reviews = connection.execute("""
        SELECT COUNT(*)
        FROM reviews
        WHERE rating NOT BETWEEN 1 AND 5
    """).fetchone()[0]

    print(f"{'Completed bookings without payment':40}: {completed_without_payment}")
    print(f"{'Negative payment amounts':40}: {negative_amounts}")
    print(f"{'Invalid review ratings':40}: {invalid_reviews}")

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("DATABASE VALIDATION REPORT")
    print("=" * 60)

    connection = get_connection()

    validate_row_counts(connection)
    validate_primary_keys(connection)
    validate_foreign_keys(connection)
    validate_nulls(connection)
    validate_business_rules(connection)

    connection.close()

    print("\n" + "=" * 60)
    print("✅ ALL VALIDATIONS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()