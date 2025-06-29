import pandas as pd
import re

def clean_data(filename):
    """
    read, clean, and normalize a CSV dataset using pandas.
    detects extensions in phone columns and creates separate ext columns.
    """

    try:
        print("\n[clean_data()] starting...")

        df = pd.read_csv(filename, encoding='utf-8')
        df.drop_duplicates(inplace=True)

        # normalize column headers
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

        # find phone columns
        phone_cols = [col for col in df.columns if 'phone' in col]
        ext_cols = []

        # regex to find extension patterns like x123, ext123, ext.123, extension 123, etc.
        ext_pattern = re.compile(r'(?:ext\.?|x|extension)\s*\.?:?\s*(\d{1,5})', re.IGNORECASE)

        for col in phone_cols:
            ext_col_name = f"{col}_ext"
            ext_cols.append(ext_col_name)

            # extract extensions into new column
            def extract_extension(phone_str):
                if not isinstance(phone_str, str):
                    return ''
                match = ext_pattern.search(phone_str)
                return match.group(1) if match else ''

            df[ext_col_name] = df[col].apply(extract_extension)

            # clean phone number by removing non-digit chars and extension text
            def clean_phone(phone_str):
                if not isinstance(phone_str, str):
                    return ''
                # remove extension part from phone string
                phone_str = ext_pattern.sub('', phone_str)
                # keep only digits
                digits = re.sub(r'\D', '', phone_str)
                return digits

            df[col] = df[col].apply(clean_phone)

        # append extension columns to headers
        final_headers = list(df.columns)

        print(f"    columns after processing extensions: {final_headers}")
        print(f"    number of rows: {len(df)}")
        print("    data cleaning complete")

        return final_headers, df.values.tolist(), True

    except Exception as e:
        print(f"    [error] {e}")
        return [], [], False
