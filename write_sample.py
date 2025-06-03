import sqlite3
import time
import random
import os

DB_PATH = "sqlite-data/sample.db"
MAX_ROWS = 100

# Ensure the database and table exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS table_sample (
            timestamp INTEGER NOT NULL,
            value REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert a new row every second
def insert_loop():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        while True:
            # Check current number of rows
            cursor.execute('SELECT COUNT(*) FROM table_sample')
            row_count = cursor.fetchone()[0]

            # Delete the oldest row if over the limit
            if row_count >= MAX_ROWS:
                cursor.execute('''
                    DELETE FROM table_sample
                    WHERE timestamp = (
                        SELECT timestamp FROM table_sample
                        ORDER BY timestamp ASC
                        LIMIT 1
                    )
                ''')

            # Insert new row
            ts = int(time.time())
            val = round(random.uniform(0, 10), 3)
            cursor.execute('INSERT INTO table_sample (timestamp, value) VALUES (?, ?)', (ts, val))
            conn.commit()
            print(f"Inserted: {ts}, {val}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    insert_loop()
