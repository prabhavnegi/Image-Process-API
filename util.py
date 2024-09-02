import pandas as pd
import re

def validate_csv_format(file): 
    expected_headers = ['S. No.', 'Product Name', 'Input Image Urls']
    try:
        df = pd.read_csv(file)

        if list(df.columns) != expected_headers:
            raise Exception(f"Expected headers {expected_headers}, but got {list(df.columns)}")
        
        if df.shape[1] != len(expected_headers):
            raise Exception(f"Expected {len(expected_headers)} columns, but found {df.shape[1]}")
        
        for idx, row in df.iterrows():
            if pd.isna(row['Product Name']) or not isinstance(row['Product Name'], str):
                raise Exception(f"Row {idx + 1}: 'Product Name' empty")
            
            if pd.isna(row['Input Image Urls']) or not isinstance(row['Input Image Urls'], str):
                raise Exception(f"Row {idx + 1}: 'Input Image Urls' should be a non-empty string.")
            
            else:
                urls = row['Input Image Urls'].split(',')
                for url in urls:
                    if not re.match(r'^https?://', url.strip()):
                        raise Exception(f"Row {idx + 1}: Invalid URL in 'Input Image Urls': {url.strip()}")

    except Exception as e:
        print("CSV validation error")
        print(e)
        return (False, str(e))
    
    return (True,"")