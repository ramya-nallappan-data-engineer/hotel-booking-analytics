from pathlib import Path

import duckdb

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

DATABASE_FILE = Path("database/hotel_booking.duckdb")
SCHEMA_FILE = Path("database/schema.sql")
DATA_FOLDER = Path("data")

# ------------------------------------------------------------------
# Database Connection
# ------------------------------------------------------------------

def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Create DuckDB connection.
    """

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return duckdb.connect(
        DATABASE_FILE
    )

# ------------------------------------------------------------------
# Schema
# ------------------------------------------------------------------

def create_schema(
    connection: duckdb.DuckDBPyConnection
) -> None:
    """
    Execute schema.sql.
    """

    print("\nCreating database schema...")

    sql = SCHEMA_FILE.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)

    print("Schema created.")

# ------------------------------------------------------------------
# CSV Loader
# ------------------------------------------------------------------

def load_table(
    connection: duckdb.DuckDBPyConnection,
    table_name: str
) -> int:
    """
    Load CSV into DuckDB table.

    Returns
    -------
    int
        Rows loaded.
    """

    csv_file = DATA_FOLDER / f"{table_name}.csv"

    connection.execute(
        f"""
        INSERT INTO {table_name}
        SELECT *
        FROM read_csv_auto(
            '{csv_file.as_posix()}',
            HEADER=TRUE
        )
        """
    )

    row_count = connection.execute(
        f"""
        SELECT COUNT(*)
        FROM {table_name}
        """
    ).fetchone()[0]

    print(
        f"{table_name:<15} {row_count:>10,} rows"
    )

    return row_count

# ------------------------------------------------------------------
# Load Data
# ------------------------------------------------------------------

def load_all_tables(
    connection: duckdb.DuckDBPyConnection
) -> dict:
    """
    Load all datasets.
    """

    print("\nLoading datasets...\n")

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

    for table in tables:

        summary[table] = load_table(
            connection,
            table
        )

    return summary

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

def print_summary(
    summary: dict
) -> None:
    """
    Print loading summary.
    """

    print("\n")
    print("=" * 55)
    print("DATABASE LOAD SUMMARY")
    print("=" * 55)

    total = 0

    for table, rows in summary.items():

        print(
            f"{table:<15} {rows:>10,}"
        )

        total += rows

    print("-" * 55)

    print(
        f"{'TOTAL':<15} {total:>10,}"
    )

    print("=" * 55)

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():

    print("=" * 55)
    print("HOTEL BOOKING DATABASE LOADER")
    print("=" * 55)

    connection = get_connection()

    create_schema(connection)

    summary = load_all_tables(
        connection
    )

    print_summary(
        summary
    )

    connection.close()

    print("\nDatabase created successfully.")


if __name__ == "__main__":
    main()