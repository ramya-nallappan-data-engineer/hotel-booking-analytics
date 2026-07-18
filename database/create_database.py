from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "database" / "interview.db"
SCHEMA_PATH = PROJECT_ROOT / "schema" / "schema.sql"


def create_database():
    print("Connecting to DuckDB...")

    conn = duckdb.connect(str(DB_PATH))

    print("Connected Successfully!")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    conn.execute(schema)

    print("Schema and tables created successfully!")

    conn.close()

    print("Database ready for loading.")


if __name__ == "__main__":
    create_database()