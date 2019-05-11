import sqlite3

conn = sqlite3.connect("users.db")

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS users')

cur.execute('CREATE TABLE users (name1 TEXT, buy1 INTEGER, buy2 INTEGER, clicks INTEGER, stat1 INTEGER )')

conn.close()
