from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "interview.db"
SCHEMA_PATH = BASE_DIR / "schema" / "schema.sql"
LOAD_DATA_PATH = BASE_DIR / "sql" / "07_advanced.sql"
CUSTOMERS_CSV = BASE_DIR / "data" / "customers.csv"

conn = duckdb.connect(str(DATABASE_PATH))

with open(SCHEMA_PATH, "r") as file:
    schema_sql = file.read()

conn.execute(schema_sql)

print("Tables created successfully!")

with open(LOAD_DATA_PATH, "r", encoding="utf-8") as file:
    sql = file.read()

sql = sql.replace(
    "{{CUSTOMERS_CSV}}",
    CUSTOMERS_CSV.as_posix()
)

conn.execute(sql)

conn.close()