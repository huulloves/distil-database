"""
    backend business logic for distil-database
    handles dataset processing, database operations, etc.
"""
import os
import sqlite3
import logging

from src.prepare import drop_tables
from src.input_pipeline import dataset_pipeline

logger = logging.getLogger(__name__)
DEFAULT_DB_PATH = "distil-database-content.db"

class DistilBackend:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        logger.info(f"connected to database: {db_path}")
    
    def close(self):
        """close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("database connection closed")

    def list_tables(self) -> list[str]:
        """get list of all tables in database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in cursor.fetchall()]
    
    def query_table(self, table_name: str) -> tuple[bool, list | str]:
        """
            query all data from a table
            returns: (success, data_or_error_message)
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(f'SELECT * FROM "{table_name}"')
            rows = cursor.fetchall()
            return True, rows
        except Exception as e:
            return False, str(e)
    
    def add_dataset(self, csv_file: str, table_name: str = "table1") -> tuple[bool, str]:
        """
            add dataset from CSV file to database
            returns: (success, message)
        """
        # validate file exists
        if not os.path.exists(csv_file):
            return False, f"file not found: {csv_file}"
        
        try:
            # clean slate - drop existing tables
            logger.info("dropping existing tables for clean injection")
            drop_tables(self.conn)
            
            # process the dataset
            logger.info(f"processing {csv_file} into table '{table_name}'")
            success = dataset_pipeline(self.conn, csv_file, table_name)
            
            if success:
                return True, f"dataset successfully added to table '{table_name}'"
            else:
                return False, "failed to process dataset"
                
        except Exception as e:
            logger.error(f"error adding dataset: {e}")
            return False, f"error: {e}"
    
    def get_table_summary(self, table_name: str) -> tuple[bool, dict | str]:
        """
            get summary statistics for a table
            returns: (success, summary_dict_or_error)
        """
        try:
            cursor = self.conn.cursor()
            
            # get row count
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            row_count = cursor.fetchone()[0]

            # get column info
            cursor.execute(f'PRAGMA table_info("{table_name}")')
            columns = cursor.fetchall()
            
            summary = {
                "table_name": table_name,
                "row_count": row_count,
                "column_count": len(columns),
                "columns": [col[1] for col in columns]  # column names
            }
            
            return True, summary
            
        except Exception as e:
            return False, str(e)
