import sqlite3

conn = sqlite3.connect("users.db")

curr = conn.cursor()

curr.execute("CREATE TABLE users (ip TEXT, buy1 INTEGER, buy2 INTEGER)")

conn.close()