import sqlite3
import csv
import controller as ctrl
def clean_data(filename):
    """
    reads csv, cleans data, and returns normalized headers, cleaned rows, and a success boolean.
    """
    norm_headers = []
    cleaned_rows = []
    success = False
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)
            if not headers:
                print("[clean_data] error: no headers found in CSV.")
                return norm_headers, cleaned_rows, success
            norm_headers = [h.strip().lower().replace(' ', '_') for h in headers]
            for row in reader:
                cleaned_row = [cell.strip() if isinstance(cell, str) else '' for cell in row]
                cleaned_rows.append(cleaned_row)
        if not cleaned_rows:
            print("[clean_data] warning: no data rows found in CSV.")
        else:
            success = True
            print(f"[debug] identified headers: {norm_headers}")
            print(f"[debug] number of data rows: {len(cleaned_rows)}")
        return norm_headers, cleaned_rows, success
    except Exception as e:
        print(f"[clean_data] error: {e}")
        return norm_headers, cleaned_rows, success

def create_tables(conn, headers):
    """
    creates 3nf tables: state, city, location, and passengers (with dynamic columns).
    returns success boolean.
    """
    success = False
    try:
        cursor = conn.cursor()
        print("[debug] creating tables...")
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
        # passengers table: all columns except city and state
        passenger_headers = [h for h in headers if h not in ('city', 'state')]
        passenger_cols_sql = ', '.join([f'"{col}" TEXT' for col in passenger_headers])
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY,
            location_id INTEGER,
            {passenger_cols_sql},
            FOREIGN KEY(location_id) REFERENCES location(location_id)
        )''')
        print("[debug] tables created.")
        success = True
    except Exception as e:
        print(f"[create_tables] error: {e}")
    return success

def inject(conn, headers, rows):
    """
    injects cleaned data into the normalized tables.
    returns success boolean.
    """
    try:
        cursor = conn.cursor()
        city_idx = headers.index('city') if 'city' in headers else None
        state_idx = headers.index('state') if 'state' in headers else None
        passenger_indices = [i for i in range(len(headers)) if i not in (city_idx, state_idx)]
        passenger_headers = [headers[i] for i in passenger_indices]

        for row in rows:
            city = row[city_idx]
            state = row[state_idx]
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
            passenger_values = [row[i] for i in passenger_indices]
            placeholders = ', '.join(['?'] * (1 + len(passenger_headers)))
            columns_str = ', '.join(['location_id'] + passenger_headers)
            cursor.execute(f'INSERT INTO passengers ({columns_str}) VALUES ({placeholders})', [location_id] + passenger_values)

        conn.commit()
        print(f"[inject] injected {len(rows)} rows into state, city, location, and passengers tables (3NF).")
        return True
    except Exception as e:
        print(f"[inject] error: {e}")
        return False

def inject_dataset(conn, filename):
    """
    main orchestrator: clean data, create/alter tables, and inject.
    returns success boolean.
    """
    print("[database] inject_dataset called.")
    headers, rows, success = clean_data(filename)
    if not success:
        print("[database] error: cleaning data failed.")
        return False

    print("[database] creating tables create_tables(conn, headers)")
    success = create_tables(conn, headers)
    if not success:
        print("[database] error: creating tables failed.")
        return False
    
    print("[database] tables created successfully, now injecting data.")

    print("[database] injecting inject(conn, headers, rows)")
    success = inject(conn, headers, rows)
    return success

def query_all_data():
    """
    placeholder for SELECT * from dataset.
    queries all data from dataset table and prints it.
    """
    db_path = 'database-content.db'
    conn = sqlite3.connect(db_path)
    print("[query_all_data] connecting to database.")
    if not conn:
        print("[query_all_data] error: could not connect to database.")
        return False
    else:
        cursor = conn.cursor()
        print("[query_all_data] querying all data.")

        cursor.execute('SELECT * from dataset')
        rows = cursor.fetchall()
        if not rows:
            print("[query_all_data] no data found in main dataset.")
            return False
        else:
            print(f"[query_all_data] found {len(rows)} rows in dataset table.")
            for row in rows:
                print(row)
    conn.close()

def query_table(table_name):
    """
    placeholder for SELECT * from table.
    queries all data from desired table and prints it.
    """
    db_path = 'database-content.db'
    conn = sqlite3.connect(db_path)
    print("[query_all_data] connecting to database.")
    if not conn:
        print("[query_all_data] error: could not connect to database.")
        return False
    else:
        cursor = conn.cursor()
        print("[query_all_data] querying all data from selected table.")

        cursor.execute('SELECT * FROM passengers')
        rows = cursor.fetchall()
        if not rows:
            print("[query_all_data] no data found in passengers table.")
            return False
        else:
            print(f"[query_all_data] found {len(rows)} rows in passengers table.")
            for row in rows:
                print(row)
    conn.close()


def main():
    # for cli testing
    import sys
    if len(sys.argv) < 2:
        print("usage: python database.py <csv_filename>")
        return
    filename = sys.argv[1]
    db_path = 'database-content.db'
    conn = sqlite3.connect(db_path)
    success = inject_dataset(conn, filename)
    conn.close()

    print(f"[main] successful?: {success}")

if __name__ == "__main__":
    main()