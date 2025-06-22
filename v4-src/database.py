import sqlite3
import csv

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

def create_tables(conn, headers, main_table_name):
    """
    creates 3nf tables: country, city, location, and a main table (with dynamic columns).
    returns success boolean.
    """
    success = False
    try:
        cursor = conn.cursor()
        print("[debug] creating tables...")
        cursor.execute('CREATE TABLE IF NOT EXISTS country (country_id INTEGER PRIMARY KEY, country_name TEXT UNIQUE)')
        cursor.execute('CREATE TABLE IF NOT EXISTS city (city_id INTEGER PRIMARY KEY, city_name TEXT UNIQUE)')
        cursor.execute('''CREATE TABLE IF NOT EXISTS location (
            location_id INTEGER PRIMARY KEY,
            city_id INTEGER,
            country_id INTEGER,
            UNIQUE(city_id, country_id),
            FOREIGN KEY(city_id) REFERENCES city(city_id),
            FOREIGN KEY(country_id) REFERENCES country(country_id)
        )''')
        # main table: all columns except city and country
        main_headers = [h for h in headers if h not in ('city', 'country')]
        cols_sql = ', '.join([f'"{col}" TEXT' for col in main_headers])
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{main_table_name}" (
            {main_table_name}_id INTEGER PRIMARY KEY,
            location_id INTEGER,
            {cols_sql},
            FOREIGN KEY(location_id) REFERENCES location(location_id)
        )''')
        print(f"[debug] main table '{main_table_name}' and supporting tables created.")
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
        country_idx = headers.index('country') if 'country' in headers else None
        # verify headers for debug
        if city_idx is None or country_idx is None:
            print("[inject] error: 'city' or 'country' column not found in headers.")
            return False
        passenger_indices = [i for i in range(len(headers)) if i not in (city_idx, country_idx)]
        passenger_headers = [headers[i] for i in passenger_indices]

        for row in rows:
            city = row[city_idx]
            country = row[country_idx]
            # country
            cursor.execute('INSERT OR IGNORE INTO country (country_name) VALUES (?)', (country,))
            cursor.execute('SELECT country_id FROM country WHERE country_name=?', (country,))
            country_id = cursor.fetchone()[0]
            # city
            cursor.execute('INSERT OR IGNORE INTO city (city_name) VALUES (?)', (city,))
            cursor.execute('SELECT city_id FROM city WHERE city_name=?', (city,))
            city_id = cursor.fetchone()[0]
            # location
            cursor.execute('INSERT OR IGNORE INTO location (city_id, country_id) VALUES (?, ?)', (city_id, country_id))
            cursor.execute('SELECT location_id FROM location WHERE city_id=? AND country_id=?', (city_id, country_id))
            location_id = cursor.fetchone()[0]
            # passengers
            passenger_values = [row[i] for i in passenger_indices]
            placeholders = ', '.join(['?'] * (1 + len(passenger_headers)))
            columns_str = ', '.join(['location_id'] + [f'"{col}"' for col in passenger_headers])            
            cursor.execute(f'INSERT INTO passengers ({columns_str}) VALUES ({placeholders})', [location_id] + passenger_values)

        conn.commit()
        print(f"[inject] injected {len(rows)} rows into country, city, location, and passengers tables (3NF).")
        return True
    except Exception as e:
        print(f"[inject] error: {e}")
        return False

def inject_dataset(conn, filename, main_table_name):
    """
    main orchestrator: clean data, create/alter tables, and inject.
    returns success boolean.
    """
    print("[database] inject_dataset called.")
    print(f"[database] cleaning data from {filename}.")
    headers, rows, success = clean_data(filename)
    if not success:
        print("[database] error: cleaning data failed.")
        return False

    print("[database] creating tables create_tables(conn, headers, main_table_name)")
    success = create_tables(conn, headers, main_table_name)
    if not success:
        print("[database] error: creating tables failed.")
        return False
    
    print("[database] tables created successfully, now injecting data.")

    print("[database] injecting inject(conn, headers, rows)")
    success = inject(conn, headers, rows)
    return success

def drop_all_tables(conn):
    """
    drops all user tables in the database for a clean test run.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS "{table}"')
    conn.commit()
    print("[debug] all tables dropped.")

def main():
    # for cli testing, database.py can be run directly
    import sys
    import os
    succcess = False

    try:
        if len(sys.argv) < 2:
            print("[main] usage: python database.py <csv_filename>")
            success = False
            return success
        filename = sys.argv[1]
        db_path = 'database-content.db'
        conn = sqlite3.connect(db_path)

        if conn is None:
            print("[main] error: could not connect to database.")
            success = False
            return success
        else:
            print(f"[main] connected to database at {db_path}.")
            

        try:
            # Drop all tables for a clean test run
            print("[main] dropping all tables for a clean test run.")
            drop_all_tables(conn)
        except Exception as e:
            print(f"[main] error dropping tables: {e}")
            success = False
            return success

        try:
             # prompt user to name main tables of dataset
            default_table = os.path.splitext(os.path.basename(filename))[0]
            user_table = input(f"enter main table name (default: {default_table}): ").strip()
            main_table_name = user_table if user_table else default_table
        except Exception as e:
            print(f"\n[main] name not provided or error: {e}")
        finally:
             # code for injecting dataset
            print(f"[main] injecting dataset from {filename} into database {db_path}.")
            success = inject_dataset(conn, filename, main_table_name)
            print(f"[main] data injection successful?: {success}")
            
    except Exception as e:
        print(f"[main] error: {e}")
        succcess = False
        return

    # menu options for CLI interaction
    while succcess is True:
        print("\nchoose an option:")
        print("1. list all tables")
        print("2. query a specific table")
        print("3. list all tables")
        print("4. quit")
        choice = input("enter option number: ").strip()
        if choice == "1":
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            print("[main] tables in database:", tables)
        elif choice == "2":
            table_name = input("[main] Enter table name: ").strip()
            cursor = conn.cursor()
            try:
                cursor.execute(f'SELECT * FROM "{table_name}"')
                rows = cursor.fetchall()
                if not rows:
                    print(f"[main] no data found in table '{table_name}'.")
                else:
                    print(f"[main] rows in '{table_name}':")
                    for row in rows:
                        print(row)
            except Exception as e:
                print(f"[main] error querying table '{table_name}': {e}")
        elif choice == "3":
            cursor = conn.cursor()
            print("[main] listing all tables in database.")
            try:
                cursor.execute("SELECT * FROM dataset;")
                rows = cursor.fetchall()
                if not rows:
                    print("[main] no data found in dataset table.")
                else:
                    print("[main] rows in dataset table:")
                    for row in rows:
                        print(row)
            except Exception as e:
                print(f"[main] error querying dataset table: {e}")
        elif choice == "4":
            print("[main] exiting.")
            break
        else:
            print("[main] invalid option. Try again.")

    conn.close()

if __name__ == "__main__":
    # run main function as script executed directly
    print("[main] running database.py.")
    main()