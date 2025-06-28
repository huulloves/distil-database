''' 
    1. drops all user tables in the database for a clean test run.
    2. creates 3nf tables: country, city, location, and a main table (with dynamic columns).
    returns success boolean.
'''

def drop_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS "{table}"')
    conn.commit()
    print("\n[drop_tables()] all tables dropped.")

def create_tables(conn, headers, main_table_name):
    success = False
    try:
        cursor = conn.cursor()
        print("\n[create_tables()] creating tables...")
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
        print(f"    main table '{main_table_name}' and supporting tables created.")
        success = True
    except Exception as e:
        print(f"    [warning] {e}")
    return success
