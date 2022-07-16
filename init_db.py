import sqlite3
import sys
import os

database_name = sys.argv[1]

if os.path.exists(database_name):
    os.remove(database_name)

connection = sqlite3.connect(database_name)

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()

