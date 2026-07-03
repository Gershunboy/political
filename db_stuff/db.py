import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "politicians.db")

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = OFF")  # off during migration
cur = conn.cursor()




conn.execute("")
conn.commit()
conn.close()

print("Migration complete.")