""" 
    injects cleaned data into the normalized tables. returns success boolean. 
"""

import logging

def inject(conn, headers, rows, main_table_name):
    """
        inserts cleaned data into country, city, location, and main tables (3NF).
        returns True on success, False on error.
    """

    try:
        logging.info("[inject()] starting...")
        cursor = conn.cursor()
        city_idx = headers.index('city') if 'city' in headers else None
        country_idx = headers.index('country') if 'country' in headers else None

        # verify headers for debug
        if city_idx is None or country_idx is None:
            logging.warning("    'city' or 'country' column not found in headers.")
            return False

        main_indices = [i for i in range(len(headers)) if i not in (city_idx, country_idx)]
        main_headers = [headers[i] for i in main_indices]

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

            # main table
            main_values = [row[i] for i in main_indices]
            placeholders = ', '.join(['?'] * (1 + len(main_headers)))
            columns_str = ', '.join(['location_id'] + [f'"{col}"' for col in main_headers])
            cursor.execute(
                f'INSERT INTO "{main_table_name}" ({columns_str}) VALUES ({placeholders})',
                [location_id] + main_values
            )

        conn.commit()
        logging.info(f"    injected {len(rows)} rows into country, city, location, and main tables (3NF).")
        return True
    except Exception as e:
        logging.warning(f"    [warning] {e}")
        return False
    