from pathlib import Path
import sys
import time
import duckdb
import pandas as pd

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "database" / "interview.db"

DEFAULT_QUERY = PROJECT_ROOT / "sql" / "03_aggregations.sql"

# ============================================================
# EXECUTE QUERY
# ============================================================

def execute_sql(query_file: Path):

    if not query_file.exists():
        print(f"\n❌ SQL file not found:\n{query_file}")
        return

    print("=" * 70)
    print(f"Executing : {query_file.name}")
    print("=" * 70)

    with open(query_file, "r", encoding="utf-8") as f:
        query = f.read()

    connection = duckdb.connect(str(DATABASE_PATH))

    start = time.perf_counter()

    try:

        result = connection.execute(query).fetchdf()

        elapsed = time.perf_counter() - start

        print(result)

        print("\n" + "-" * 70)
        print(f"Rows Returned : {len(result):,}")
        print(f"Execution Time: {elapsed:.4f} seconds")
        print("-" * 70)

    except Exception as ex:

        print("\n❌ Query Failed")
        print(ex)

    finally:

        connection.close()

# ============================================================
# MAIN
# ============================================================

def main():

    if len(sys.argv) > 1:

        sql_file = PROJECT_ROOT / sys.argv[1]

    else:

        sql_file = DEFAULT_QUERY

    execute_sql(sql_file)

if __name__ == "__main__":
    main()