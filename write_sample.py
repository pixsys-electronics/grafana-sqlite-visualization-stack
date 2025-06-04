import sqlite3
import time
import random
import os

DB_PATH = "sqlite-data/sample.db"
MAX_ROWS = 100
DB_TABLE_DEFAULT = "table_sample"
VALUE_MIN = 0
VALUE_MAX = 10

# Ensure the database and table exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {DB_TABLE_DEFAULT} (
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
            cursor.execute(f'SELECT COUNT(*) FROM {DB_TABLE_DEFAULT}')
            row_count = cursor.fetchone()[0]

            # Delete the oldest row if over the limit
            if row_count >= MAX_ROWS:
                cursor.execute(f'''
                    DELETE FROM {DB_TABLE_DEFAULT}
                    WHERE timestamp = (
                        SELECT timestamp FROM {DB_TABLE_DEFAULT}
                        ORDER BY timestamp ASC
                        LIMIT 1
                    )
                ''')

            # Insert new row
            ts = int(time.time())
            val = round(random.uniform(VALUE_MIN, VALUE_MAX), 3)
            cursor.execute(f'INSERT INTO {DB_TABLE_DEFAULT} (timestamp, value) VALUES (?, ?)', (ts, val))
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
