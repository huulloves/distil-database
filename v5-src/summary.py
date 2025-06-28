''' 
    prints a summary of the database.
'''

def print_database_summary(conn, main_table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("\n[summary] database contains the following tables:")
    for table in tables:
        print(f"\ntable: {table}")
        # get columns
        cursor.execute(f'PRAGMA table_info("{table}")')
        columns = [info[1] for info in cursor.fetchall()]
        print(f"    columns: {columns}")
        # get row count
        cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
        count = cursor.fetchone()[0]
        print(f"    row count: {count}")
        # print first 3 rows as a sample
        cursor.execute(f'SELECT * FROM "{table}" LIMIT 3')
        rows = cursor.fetchall()
        if rows:
            print("    sample rows:")
            for row in rows:
                print(f"      {row}")
        else:
            print("\n[warning] no data")

    # aggregates from main table
    print("\naggregates from main table:")
    if main_table_name and main_table_name in tables:
        # total number of customers (rows in main table)
        cursor.execute(f'SELECT COUNT(*) FROM "{main_table_name}"')
        total_customers = cursor.fetchone()[0]
        print(f"    total number of customers is {total_customers}")

        # most common country of origin
        # joining main table -> location -> country
        try:
            cursor.execute(f'''
                SELECT country.country_name, COUNT(*) as cnt
                FROM "{main_table_name}"
                JOIN location ON "{main_table_name}".location_id = location.location_id
                JOIN country ON location.country_id = country.country_id
                GROUP BY country.country_name
                ORDER BY cnt DESC
                LIMIT 1
            ''')
            result = cursor.fetchone()
            if result:
                print(f"    most common country of origin is {result[0]} with {result[1]} customers")
            else:
                print("     [warning] could not determine most common country.")
        except Exception as e:
            print(f"    [warning] {e}")
