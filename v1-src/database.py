import sqlite3
import pandas as pd

def clean_dataframe(df):
    # Example cleaning: strip whitespace, drop duplicates, fill NaN, etc.
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.drop_duplicates()
    df = df.fillna('')
    return df

def inject_dataset(filename, db_path='database-content.db'):
    try:
        # Read CSV with pandas
        df = pd.read_csv(filename)
        df = clean_dataframe(df)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Explicitly define columns based on your dataset
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dataset (
                setID INTEGER PRIMARY KEY AUTOINCREMENT,
                "Index" INTEGER,
                "Customer_Id" TEXT,
                "First_Name" TEXT,
                "Last_Name" TEXT,
                "Company" TEXT,
                "City" TEXT,
                "Country" TEXT,
                "Phone_1" TEXT,
                "Phone_2" TEXT,
                "Email" TEXT,
                "Subscription_Date" TEXT,
                "Website" TEXT
            )
        ''')

        # Rename DataFrame columns to match the table columns
        df = df.rename(columns={
            'Index': 'Index',
            'Customer Id': 'Customer_Id',
            'First Name': 'First_Name',
            'Last Name': 'Last_Name',
            'Company': 'Company',
            'City': 'City',
            'Country': 'Country',
            'Phone 1': 'Phone_1',
            'Phone 2': 'Phone_2',
            'Email': 'Email',
            'Subscription Date': 'Subscription_Date',
            'Website': 'Website'
        })

        # Insert cleaned data row by row
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO dataset (
                    "Index", "Customer_Id", "First_Name", "Last_Name", "Company",
                    "City", "Country", "Phone_1", "Phone_2", "Email",
                    "Subscription_Date", "Website"
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Index'],
                row['Customer_Id'],
                row['First_Name'],
                row['Last_Name'],
                row['Company'],
                row['City'],
                row['Country'],
                row['Phone_1'],
                row['Phone_2'],
                row['Email'],
                row['Subscription_Date'],
                row['Website']
            ))

        conn.commit()
        conn.close()
        print(f"[inject] Cleaned dataset from {filename} injected into database.")
    except Exception as e:
        print(f"[inject] Error injecting dataset: {e}")