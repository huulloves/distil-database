import sqlite3
import csv

def clean_value(value):
    return value.strip() if isinstance(value, str) else ('' if value is None else value)

def inject_dataset(filename, db_path='database-content.db'):
    """
    injects data from a CSV file into the SQLite database in 3NF:
    - state(state_id, state_name)
    - city(city_id, city_name)
    - location(location_id, city_id, state_id)
    - passengers(passenger_id, location_id, ...other columns...)
    """
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            # find city and state columns, all others go to passengers
            norm_headers = [h.strip().lower().replace(' ', '_') for h in headers]
            city_idx = norm_headers.index('city') if 'city' in norm_headers else None
            state_idx = norm_headers.index('state') if 'state' in norm_headers else None
            if city_idx is None or state_idx is None:
                print("[inject] error: CSV must have 'city' and 'state' columns.")
                return
            passenger_indices = [i for i in range(len(headers)) if i not in (city_idx, state_idx)]
            passenger_headers = [headers[i].strip().replace(' ', '_') for i in passenger_indices]

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # create normalized tables
            cursor.execute('CREATE TABLE IF NOT EXISTS state (state_id INTEGER PRIMARY KEY, state_name TEXT UNIQUE)')
            cursor.execute('CREATE TABLE IF NOT EXISTS city (city_id INTEGER PRIMARY KEY, city_name TEXT UNIQUE)')
            cursor.execute('''CREATE TABLE IF NOT EXISTS location (
                location_id INTEGER PRIMARY KEY,
                city_id INTEGER,
                state_id INTEGER,
                UNIQUE(city_id, state_id),
                FOREIGN KEY(city_id) REFERENCES city(city_id),
                FOREIGN KEY(state_id) REFERENCES state(state_id)
            )''')
            passenger_cols_sql = ', '.join([f'"{col}" TEXT' for col in passenger_headers])
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS passengers (
                passenger_id INTEGER PRIMARY KEY,
                location_id INTEGER,
                {passenger_cols_sql},
                FOREIGN KEY(location_id) REFERENCES location(location_id)
            )''')

            for row in reader:
                city = clean_value(row[city_idx])
                state = clean_value(row[state_idx])
                # state
                cursor.execute('INSERT OR IGNORE INTO state (state_name) VALUES (?)', (state,))
                cursor.execute('SELECT state_id FROM state WHERE state_name=?', (state,))
                state_id = cursor.fetchone()[0]
                # city
                cursor.execute('INSERT OR IGNORE INTO city (city_name) VALUES (?)', (city,))
                cursor.execute('SELECT city_id FROM city WHERE city_name=?', (city,))
                city_id = cursor.fetchone()[0]
                # location
                cursor.execute('INSERT OR IGNORE INTO location (city_id, state_id) VALUES (?, ?)', (city_id, state_id))
                cursor.execute('SELECT location_id FROM location WHERE city_id=? AND state_id=?', (city_id, state_id))
                location_id = cursor.fetchone()[0]
                # passengers
                passenger_values = [clean_value(row[i]) for i in passenger_indices]
                placeholders = ', '.join(['?'] * (1 + len(passenger_headers)))
                columns_str = ', '.join(['location_id'] + passenger_headers)
                cursor.execute(f'INSERT INTO passengers ({columns_str}) VALUES ({placeholders})', [location_id] + passenger_values)

            conn.commit()
            conn.close()
            print(f"[inject] data from {filename} injected into state, city, location, and passengers tables (3NF).")
    except Exception as e:
        print(f"[inject] error injecting dataset: {e}")

def query_all_data(db_path='database-content.db'):
    """
    queries all data from the passengers table and formats it for display.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(passengers)')
        columns = [info[1] for info in cursor.fetchall() if info[1] != 'passenger_id']
        if not columns:
            conn.close()
            return "[query] no columns found."
        columns_str = ', '.join([f'"{col}"' for col in columns])
        cursor.execute(f'SELECT {columns_str} FROM passengers')
        rows = cursor.fetchall()
        conn.close()
        # simple formatting
        output = ', '.join(columns) + '\n'
        for row in rows:
            output += ', '.join(str(cell) for cell in row) + '\n'
        return output if rows else "[query] no data found."
    except Exception as e:
        return f"[query] error: {e}"