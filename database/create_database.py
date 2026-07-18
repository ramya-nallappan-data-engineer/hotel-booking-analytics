import duckdb

conn = duckdb.connect("interview.db")

print("Connected Successfully!")

conn.close()