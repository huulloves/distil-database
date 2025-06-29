'''
    cli logic: handles all user interaction and menu display
'''

import logging
from src.summary import print_database_summary

def prompt_main_table_name(default_table):
    """
    prompt the user to enter a main table name, or use the default if left blank.
    """
    logging.info("\n[prompt_main_table_name] prompting for main table name.")
    user_table = input(f"enter main table name (default: {default_table}):\n      ").strip().lower()
    return user_table if user_table else default_table

def cli_menu(conn, main_table_name):
    """
    main cli menu loop for interacting with the database.
    """
    while True:
        print("choose an option:")
        print("     1. list all tables")
        print("     2. query a specific table")
        print("     3. main table summary")
        print("     4. quit")
        choice = input("\nenter option number: ").strip()
        cursor = conn.cursor()

        if choice == "1":
            print("listing all tables in database.")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"tables: {tables}")
        elif choice == "2":
            table_name = input("enter table name: ").strip()
            if not table_name:
                logging.warning("table name cannot be empty.")
                continue
            logging.info(f"querying table '{table_name}'.")
            try:
                cursor.execute(f'SELECT * FROM "{table_name}"')
                rows = cursor.fetchall()
                if not rows:
                    logging.warning(f"no data found in table '{table_name}'.")
                else:
                    print(f"rows in '{table_name}':")
                    for row in rows:
                        print(f"    {row}")
            except Exception as e:
                logging.error(f"error querying table '{table_name}' --> {e}")
        elif choice == "3":
            print("printing database summary.")
            print_database_summary(conn, main_table_name)
        elif choice == "4":
            logging.info("exiting.")
            break
        else:
            logging.warning("invalid option. try again.")