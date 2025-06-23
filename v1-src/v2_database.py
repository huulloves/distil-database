import sqlite3
import csv

def clean_value(value):
    # Strip whitespace and handle None
    if value is None:
        return ''
    return value.strip()

def inject_dataset(filename, db_path='database-content.db'):
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            print(f"[debug] CSV headers: {headers}")

            # Clean headers for SQL (replace spaces with underscores, etc.)
            db_headers = [h.strip().replace(' ', '_') for h in headers]

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Dynamically create table with columns from headers
            columns_sql = ', '.join([f'"{col}" TEXT' for col in db_headers])
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS dataset (
                    setID INTEGER PRIMARY KEY AUTOINCREMENT,
                    {columns_sql}
                )
            ''')

            row_count = 0
            for row in reader:
                # Clean and map each value
                values = [clean_value(val) for val in row]
                # Pad values if row is short
                while len(values) < len(db_headers):
                    values.append('')
                # Truncate values if row is long
                values = values[:len(db_headers)]
                placeholders = ', '.join(['?'] * len(db_headers))
                columns_str = ', '.join([f'"{col}"' for col in db_headers])
                sql = f'INSERT INTO dataset ({columns_str}) VALUES ({placeholders})'
                cursor.execute(sql, values)
                row_count += 1
                if row_count <= 5:  # Print first 5 rows for debugging
                    print(f"[debug] Inserted row: {values}")

            conn.commit()
            conn.close()
            print(f"[inject] {row_count} rows from {filename} injected into database.")
    except Exception as e:
        print(f"[inject] Error injecting dataset: {e}")