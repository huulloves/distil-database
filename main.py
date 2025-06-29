''' 
    handles setup, database setup, calls to pipeline, and closing
'''
import sys
import os
import sqlite3

import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

from src.cli import cli_menu, prompt_main_table_name
from src.prepare import drop_tables
from src.input_pipeline import dataset_pipeline

def main():
    """
        main entry point: handles argument parsing, database connection, 
        prompts for main table name, runs the input pipeline, and launches the CLI menu.
    """

    if len(sys.argv) < 2:
        logging.error("[main] usage: python main.py <csv_filename>")
        return
    filename = sys.argv[1]

    db_path = input("\nenter database name (default: database-content.db): ").strip().lower()
    if not db_path:
        db_path = 'database-content.db'

    try:
        conn = sqlite3.connect(db_path)
        logging.info(f"[main] connected to database at {db_path}.")
    except Exception as e:
        logging.error(f"[main] connecting to database --> {e}")
        return

    # drop tables to prepare for injection
    try:
        logging.info("[main] dropping all tables for a clean test run.")
        drop_tables(conn)
    except Exception as e:
        logging.error(f"[main] dropping tables --> {e}")
        conn.close()
        return

    # prompt for main table name
    default_table = "table1"
    try:
        main_table_name = prompt_main_table_name(default_table)
    except Exception as e:
        logging.error(f"[main] prompting for main table name --> {e}")
        conn.close()
        return

    # inject dataset
    logging.info(f"[main] injecting dataset from {filename} into database {db_path}.")
    success = dataset_pipeline(conn, filename, main_table_name)

    if not success:
        conn.close()
        return

    logging.info(f"[main] data injection successful?: {success}")
    cli_menu(conn, main_table_name)
    conn.close()

if __name__ == "__main__":
    main()
