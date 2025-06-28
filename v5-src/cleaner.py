"""
    IN-PROGRESS
    reads a CSV file, cleans the data, and normalizes it.
"""

import csv

def clean_data(filename):
    ''' 
        cleaning header data    
    '''
    norm_headers = []
    cleaned_rows = []
    success = False

    try:
        print("\n[cleaner] starting data cleaning")
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)
            if not headers:
                print("    no headers found in CSV.")
                return norm_headers, cleaned_rows, success
            
            norm_headers = clean_header(headers)
            rows, success = clean_phonenumbers(rows)

            for row in reader:
                cleaned_row = [cell.strip() if isinstance(cell, str) else '' for cell in row]
                cleaned_rows.append(cleaned_row)
        if not cleaned_rows:
            print("    no data rows found in CSV.")
        else:
            success = True
            print(f"    identified headers: {norm_headers}")
            print(f"    number of data rows: {len(cleaned_rows)}")
            print("    data cleaning complete")
        return norm_headers, cleaned_rows, success
    except Exception as e:
        print(f"    [warning] {e}")
        return norm_headers, cleaned_rows, success
    
def clean_header(headers):

    norm_headers = [h.strip().lower().replace(' ', '_') for h in headers]

    return norm_headers

def clean_phonenumbers(rows):
    ''' 
        clean phone numbers
    '''
    norm_numbers = []
    cleaned_numbers = []
    success = False



    return