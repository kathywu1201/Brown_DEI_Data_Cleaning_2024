import numpy as np
import pandas as pd

# read in the data
def load_spreadsheet(file_path):
    all_sheets = pd.read_excel(file_path, sheet_name=None, skiprows=1, header=[0, 1])
    processed_dataframe = {}

    for sheet_name, data in all_sheets.items():
        # print(f"--------Processing sheet: {sheet_name}--------")
        processed_dataframe[sheet_name] = data
    
    print('Total number of spreadsheets:', len(processed_dataframe))
    return processed_dataframe

def rename_column(data):
    new_header = [f'{[i]} {j}' if i != j else f'{i}' for i, j in data.columns]
    data.columns = new_header
    data.columns = data.columns.str.replace("'","")
    data.columns.values[0] = 'CourseName'
    data.columns.values[-1] = 'Total Enrollment'
    data = data.drop(data.index[-1])
    return data

# categorize courses
def categorize_course(course_id):
    # Extract the numeric part of the CourseID assuming the format is always the same
    # and the number is at the end
    #course_number = int(course_id.split()[-1])
    
    # Define the conditions for categorizing courses
    if course_id <= 200:
        return 'Introductory'
    elif 220 <= course_id <= 1010:
        return 'Intermediate'
    elif 1010 < course_id < 2000:
        return 'Advanced'
    else:
        return 'Grad'
    
def apply_courselevel(data):
    data['courseID'] = data['CourseName'].str.extract(r'(\d+)').astype(int)
    data['CourseLevel'] = data['courseID'].apply(categorize_course)
    CourseLevel_order = ['Introductory', 'Intermediate', 'Advanced', 'Grad']
    data['CourseLevel'] = pd.Categorical(data['CourseLevel'], categories=CourseLevel_order, ordered=True)
    data = data.sort_values('CourseLevel')
    data = data.drop(['courseID'], axis=1)
    return data

def calculate_percentage(data):
    data.columns = data.columns.str.replace(r"[\[\]']", "")
    percentage_columns = data.select_dtypes(include=['number']).drop('Total Enrollment', axis=1).apply(lambda x: 100 * x / x.sum()).round(4)
    percentage_columns['Total Enrollment Percentage'] = (100 * data['Total Enrollment'] / data['Total Enrollment'].sum()).round(4)
    result_data = pd.concat([data[['CourseLevel', 'CourseName']], percentage_columns], axis=1)
    result_data = pd.concat([result_data, data[['Total Enrollment']]], axis=1)
    return result_data

def check_sum_100(data):
    column_sums = data.set_index(['CourseName', 'Total Enrollment', 'CourseLevel']).sum().round(4)
    is_close_to_100 = np.isclose(column_sums, 100, atol=0.01)
    for i in is_close_to_100:
        if not i:
            print('summation error')
            return False
    print('Columns sum up to 100')
    return True
