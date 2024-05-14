import pandas as pd
import numpy as np

def extract_data_groups(excel_path, sheet_name):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    groups = {}
    current_key = None
    start_index = None
    
    # Iterate through the DataFrame to find rows with 'Q'
    for index, row in df.iterrows():
        # Check if any cell in the row contains 'Q'
        if row.astype(str).str.contains('Q').any():
            # If we have a previous key, extract the DataFrame slice up to the current row
            if current_key is not None:
                # Extract the group and remove rows/columns with all NaN values
                group_df = df.iloc[start_index:index].dropna(how='all').dropna(axis=1, how='all')
                groups[current_key] = group_df
            
            current_key = row[row.astype(str).str.contains('Q')].values[0]  
            start_index = index + 1
    
    if current_key is not None and start_index < len(df):
        # Extract the group and remove rows/columns with all NaN values
        group_df = df.iloc[start_index:].dropna(how='all').dropna(axis=1, how='all')
        groups[current_key] = group_df
    
    return groups