import pandas as pd
import numpy as np

def extract_data_groups(excel_path, sheet_name):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    groups = {}
    current_key = None
    start_index = None
    
    # iterate through the dataframe to find rows with 'Q'
    for index, row in df.iterrows():
        # check if any cell in the row contains 'Q' and number 0-9 right after
        if row.astype(str).str.contains(r'Q\d').any():
            # if we have a previous key, extract the DataFrame slice up to the current row
            if current_key is not None:
                # extract the group and remove rows/columns with all nan values
                group_df = df.iloc[start_index:index].dropna(how='all').dropna(axis=1, how='all')
                groups[current_key] = group_df
            
            current_key = row[row.astype(str).str.contains(r'Q\d')].values[0]  
            start_index = index + 1
    
    if current_key is not None and start_index < len(df):
        # extract the group and remove rows/columns with all nan values
        group_df = df.iloc[start_index:].dropna(how='all').dropna(axis=1, how='all')
        groups[current_key] = group_df
    
    return groups

def transform_and_transpose(df):
    # remove the first row and reset the column headers with the next row
    new_header = df.iloc[0]  # this row will become the header.
    df = df[1:]  # take the data less the header row
    df.columns = new_header  # set the header row as the df header
    df = df.reset_index(drop=True)

    # transpose the datatrame
    df_transposed = df.T  # transpose the dataframe
    new_header = df_transposed.iloc[0]  # grab the first row for the header
    df_transposed = df_transposed[1:]  # take the data less the header row
    df_transposed.columns = new_header  # set the header row as the df header
    df_transposed.index.name = None # remove the index name

    return df_transposed

def prepend_question_number_to_df(data_dict):
    # iterate through each item in the dictionary
    for key, df in data_dict.items():
        # extract the question number from the key
        question_number = key.split('.')[0]  # splits on the dot and takes the first part 'Q3', 'Q4', etc.
        
        # prepend the question number to the first column of the dataframe
        df.insert(0, 'Question Number', question_number)  # inserts the question number as the first column
    
    return data_dict

def combine_question_number(df):
    df.reset_index(inplace=True)
    df['Questions'] = df['Question Number'] + '. ' + df['index']
        
    df.drop(['Question Number', 'index'], axis=1, inplace=True)
    return df

