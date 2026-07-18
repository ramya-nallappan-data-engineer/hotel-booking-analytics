from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "interview.db"

conn = duckdb.connect(str(DATABASE_PATH))

QUERY_PATH = BASE_DIR / "sql" / "06_ctes.sql"

with open(QUERY_PATH, "r", encoding="utf-8") as file:
    query = file.read()

result = conn.execute(query).fetchdf()

print(result)

conn.close()