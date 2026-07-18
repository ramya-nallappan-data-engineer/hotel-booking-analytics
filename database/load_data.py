from pathlib import Path
import duckdb

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_ROOT / "database" / "interview.db"
SCHEMA_FILE = PROJECT_ROOT / "schema" / "schema.sql"
DATA_FOLDER = PROJECT_ROOT / "data" / "raw"

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection() -> duckdb.DuckDBPyConnection:
    """Create DuckDB connection."""
    return duckdb.connect(str(DATABASE_FILE))

# ============================================================
# LOAD SINGLE TABLE
# ============================================================

def load_table(connection: duckdb.DuckDBPyConnection, table_name: str) -> int:
    """
    Load CSV into DuckDB using COPY.
    """

    csv_file = DATA_FOLDER / f"{table_name}.csv"

    if not csv_file.exists():
        raise FileNotFoundError(f"CSV not found: {csv_file}")

    connection.execute(f"DELETE FROM {table_name}")

    connection.execute(f"""
        COPY {table_name}
        FROM '{csv_file.as_posix()}'
        (
            AUTO_DETECT TRUE,
            HEADER TRUE
        )
    """)

    row_count = connection.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]

    print(f"✓ {table_name:<15} {row_count:>10,} rows loaded")

    return row_count

# ============================================================
# LOAD ALL TABLES
# ============================================================

def load_all_tables(connection):

    tables = [
        "customers",
        "hotels",
        "products",
        "bookings",
        "payments",
        "reviews",
        "order_items"
    ]

    summary = {}

    print("\nLoading datasets...\n")

    for table in tables:
        summary[table] = load_table(connection, table)

    return summary

# ============================================================
# SUMMARY
# ============================================================

def print_summary(summary):

    print("\n" + "=" * 60)
    print("DATABASE LOAD SUMMARY")
    print("=" * 60)

    total = 0

    for table, rows in summary.items():

        print(f"{table:<20}{rows:>10,}")

        total += rows

    print("-" * 60)
    print(f"{'TOTAL':<20}{total:>10,}")
    print("=" * 60)

# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("HOTEL BOOKING DATABASE LOADER")
    print("=" * 60)

    connection = get_connection()

    summary = load_all_tables(connection)

    print_summary(summary)

    connection.close()

    print("\n✅ Database is ready for SQL practice.")

if __name__ == "__main__":
    main()