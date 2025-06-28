'''
    cli logic: handles all user interaction and menu display
'''

from summary import print_database_summary

def prompt_main_table_name(default_table):
    """
    prompt the user to enter a main table name, or use the default if left blank.
    """
    print("\n[prompt_main_table_name] prompting for main table name.")
    user_table = input(f"   enter main table name (default: {default_table}):\n    ").strip().lower()
    return user_table if user_table else default_table

def cli_menu(conn, main_table_name):
    """
    main cli menu loop for interacting with the database.
    """
    while True:
        print("\nchoose an option:")
        print("     1. list all tables")
        print("     2. query a specific table")
        print("     3. query main table")
        print("     4. database summary")
        print("     5. quit")
        choice = input("\nenter option number: ").strip()
        cursor = conn.cursor()

        if choice == "1":
            print("listing all tables in database.")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            print("     tables:", tables)
        elif choice == "2":
            table_name = input("enter table name: ").strip()
            if not table_name:
                print("    table name cannot be empty.")
                continue
            print(f"querying table '{table_name}'.")
            try:
                cursor.execute(f'SELECT * FROM "{table_name}"')
                rows = cursor.fetchall()
                if not rows:
                    print(f"no data found in table '{table_name}'.")
                else:
                    print(f"rows in '{table_name}':")
                    for row in rows:
                        print(f"    {row}")
            except Exception as e:
                print(f"error querying table '{table_name}' --> {e}")
        elif choice == "3":
            print(f"listing all rows in main table '{main_table_name}'.")
            try:
                cursor.execute(f'SELECT * FROM "{main_table_name}";')
                rows = cursor.fetchall()
                if not rows:
                    print(f"    no data found in {main_table_name} table.")
                else:
                    print(f"    rows in {main_table_name} table:")
                    for row in rows:
                        print(f"        {row}")
            except Exception as e:
                print(f"error querying {main_table_name} table --> {e}")
        elif choice == "4":
            print("printing database summary.")
            print_database_summary(conn, main_table_name)
        elif choice == "5":
            print("exiting.")
            break
        else:
            print("invalid option. try again.")