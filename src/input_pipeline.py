"""
    main orchestrator: clean data, create/alter tables, and inject.
    returns success boolean.
"""
from src.cleaner import clean_data
from src.prepare import create_tables
from src.inject import inject

def dataset_pipeline(conn, filename, main_table_name):
    """
    orchestrates the data pipeline: cleaning, table creation, and data injection.
    returns True on success, False on error.
    """
    print("\n[dataset_pipeline()] starting...")
    headers, rows, success = clean_data(filename)
    if not success:
        print("     [warning] cleaning data failed.")
        return False

    success = create_tables(conn, headers, main_table_name)
    if not success:
        print("     [warning] creating tables failed.")
        return False
    
    print("    tables created successfully, now injecting data.")
    success = inject(conn, headers, rows, main_table_name)
    if success:
        print("    data injection complete.")
    else:
        print("    [warning] data injection failed.")
    return success