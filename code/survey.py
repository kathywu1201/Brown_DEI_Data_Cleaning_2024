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

def transform_and_transpose(df):
    # Remove the first row and reset the column headers with the next row
    new_header = df.iloc[0]  # This row will become the header.
    df = df[1:]  # Take the data less the header row
    df.columns = new_header  # Set the header row as the df header
    df = df.reset_index(drop=True)

    # Transpose the DataFrame
    df_transposed = df.T  # Transpose the DataFrame
    new_header = df_transposed.iloc[0]  # Grab the first row for the header
    df_transposed = df_transposed[1:]  # Take the data less the header row
    df_transposed.columns = new_header  # Set the header row as the df header
    df_transposed.index.name = None # Remove the index name

    return df_transposed

def prepend_question_number_to_df(data_dict):
    # Iterate through each item in the dictionary
    for key, df in data_dict.items():
        # Extract the question number from the key
        question_number = key.split('.')[0]  # Splits on the dot and takes the first part 'Q3', 'Q4', etc.
        
        # Prepend the question number to the first column of the DataFrame
        df.insert(0, 'Question Number', question_number)  # Inserts the question number as the first column
    
    return data_dict

def combine_question_number(df):
    df.reset_index(inplace=True)
    df['Questions'] = df['Question Number'] + '. ' + df['index']
        
    df.drop(['Question Number', 'index'], axis=1, inplace=True)
    return df