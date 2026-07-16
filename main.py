import duckdb

connection = duckdb.connect("database/interview.db")

print("Database Created Successfully!")

print(connection.execute("SELECT 10+20").fetchall())

connection.close()