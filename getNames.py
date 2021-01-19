import sqlite3

conn = sqlite3.connect('names.db')
c = conn.cursor()

#c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS lastname USING fts5(name);")
#c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS firstname USING fts5(name);")
c.execute("CREATE TABLE IF NOT EXISTS firstname (name TEXT PRIMARY KEY COLLATE NOCASE);")
c.execute("CREATE TABLE IF NOT EXISTS lastname (name TEXT PRIMARY KEY COLLATE NOCASE);")


c.execute("BEGIN TRANSACTION;")

with open("first_names.all.txt") as fil:
    for line in fil:
        c.execute("INSERT OR IGNORE INTO firstname (name) VALUES (?)", (line.strip(" \n"),))
with open("last_names.all.txt") as fil:
    for line in fil:
        c.execute("INSERT OR IGNORE INTO lastname (name) VALUES (?)", (line.strip(" \n"),))
conn.commit()
conn.close()