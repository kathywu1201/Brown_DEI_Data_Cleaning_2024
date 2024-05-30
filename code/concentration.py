import pandas as pd
import numpy as np
from datetime import datetime

def load_spreadsheet(file_path):
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names[:-1] # exclude the summary
    all_sheets = {}

    for sheet_name in sheet_names:
        # print(f"--------Processing sheet: {sheet_name}--------")
        all_sheets[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1, header=[2])

    print('Total number of concentrations:', len(all_sheets))
    return all_sheets

def concat_sheets(all_sheets):
    for sheet_name, df in all_sheets.items():
        # Add a new column to each DataFrame with the name of the sheet
        df['SheetName'] = sheet_name
    
    # combined the dataframes
    data = pd.concat(all_sheets.values(), ignore_index=True)
    data = data.set_index('SheetName')
    # fill all the nan values
    data['Sex'] = data['Sex'].replace('F','Female')
    data['Sex'] = data['Sex'].replace('M','Male')
    data['HUG?'] = data['HUG?'].replace('Y','Yes')
    data['HUG?'] = data['HUG?'].fillna('Yes')
    data['HUG?'] = data['HUG?'].replace('Y','Yes')
    data['First Gen?'] = data['First Gen?'].fillna('No/Unreported')
    data['First Gen?'] = data['First Gen?'].replace('Y','Yes')
    data['Confidentiality Ind?'] = data['Confidentiality Ind?'].fillna('N')
    data['Combined or Concurrent Degree'] = data['Combined or Concurrent Degree'].fillna('None')
    data['Concentration 2'] = data['Concentration 2'].fillna('None')
    data['Concentration 3'] = data['Concentration 3'].fillna('None')
    data['Certificate Program Name'] = data['Certificate Program Name'].fillna('None')
    return data

def adjust_year(year):
    # current year
    current_year = datetime.now().year
    if year != current_year:
        diff = year-current_year
        return f'{current_year}+{diff}'
    else:
        return f'{year}'

def relative_year(data):
    data[['Term', 'Year']] = data['Intended Completion Term'].str.split(' ', expand=True)
    data['Year'] = data['Year'].astype(int)
        
    data['Year'] = data['Year'].apply(adjust_year)
    data['Intended Completion Term'] = data['Term'] + " " + data['Year']
    data = data.drop(['Term', 'Year'], axis=1)
    return data

def count_category(data):
    category_counts = {}
    for col in ['Status', 'Combined or Concurrent Degree', 'Degree', 'Sem Level', 'Sex',
        'Race/Ethnicity ', 'HUG?', 'First Gen?', 'Concentration 2',
        'Intended Completion Term']:
        pivot_df = data.pivot_table(index=['SheetName', col],aggfunc='size', fill_value=0).reset_index(name='Count')
        pivot_df = pd.DataFrame(pivot_df).reset_index()
        pivot_df = pivot_df.pivot_table(index=['SheetName'], columns=[col], values='Count', fill_value=0)
        new_column_tuples = [(col, col_name) for col_name in pivot_df.columns]
        multi_index = pd.MultiIndex.from_tuples(new_column_tuples)

        pivot_df.columns = multi_index
        pivot_df.reset_index(inplace=True)
        category_counts[col] = pivot_df
    
    # combine the different categories into one dataframe
    # Start with an empty DataFrame or initialize with the first DataFrame
    combined_df = None

    for name, df in category_counts.items():
        if combined_df is None:
            combined_df = df
        else:
            # Merge each DataFrame on the 'Key' column
            combined_df = pd.merge(combined_df, df, on='SheetName', how='left')

    return combined_df

def calculate_total_enrollment(data):
    result = data.groupby(axis=1, level=0).sum()
    data['Total Enrollment'] = result.iloc[:,-1]
    data = data.fillna(0)
    return data

def rename_columns(data):
    new_header = [f'{[i]} {j}' if i != j else f'{i}' for i, j in data.columns]
    data.columns = new_header
    data.columns = data.columns.str.replace("'","")
    data.rename(columns={'[SheetName] ': 'Concentration'}, inplace=True)
    data.rename(columns={'[Total Enrollment] ': 'Total Enrollment'}, inplace=True)
    return data

def calculate_percentage(data):
    data.columns = data.columns.str.replace(r"[\[\]']", "")
    percentage_columns = data.select_dtypes(include=['number']).drop('Total Enrollment', axis=1).apply(lambda x: 100 * x / x.sum()).round(2)
    percentage_columns['Total Enrollment Percentage'] = (100 * data['Total Enrollment'] / data['Total Enrollment'].sum()).round(2)
    result_data = pd.concat([data[['Concentration']], percentage_columns], axis=1)
    result_data = pd.concat([result_data, data[['Total Enrollment']]], axis=1)
    return result_data

def calculate_percentage_new(data):
    for column in data.columns:
        if column != 'Total Enrollment' and column != 'Concentration':
            data[column] = ((data[column] / data['Total Enrollment']) * 100).round(4)
    return data

def check_sum_100(data):
    column_sums = data.set_index(['Concentration', 'Total Enrollment']).sum().round(2)
    is_close_to_100 = np.isclose(column_sums, 100, atol=0.01)
    for i in is_close_to_100:
        if not i:
            print('summation error')
            return False
    print('Columns sum up to 100')
    return True