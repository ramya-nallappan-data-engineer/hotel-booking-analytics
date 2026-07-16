import duckdb

conn = duckdb.connect("../database/interview.db")

print("Connected Successfully!")

conn.close()