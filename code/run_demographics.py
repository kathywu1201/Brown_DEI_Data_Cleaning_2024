import pandas as pd
import numpy as np
from course_demographics import *
from utils import *

#############################################
# Similar to run_demographics_individual.py, but this script aggregates data across multiple semesters into a single CSV file, 
# providing a broader overview of the demographics over time.
#############################################

# fill out the path to the spreadsheets and select the specific semester year we want
file_path = '../data/Course Demographics Example.xlsx'
year = 'Fall 2023'

# load spreadsheet
df, all_sheets = load_spreadsheet(file_path)

# initialize an empty dictionary that stores the processed dataframes
dict_processed_data = {}

for year, data in all_sheets:
    print(f">>> Loading spreadsheet for '{year}'")
    data = df[year]

    # rename the columns
    data = rename_column(data)

    # apply course_level
    data = apply_courselevel(data)
    # print(data)

    # calculate the column percentage
    # data = calculate_percentage(data)
    data = calculate_percentage_new(data)

    # add the rows with the calcualted average
    data = calculate_average(data)

    # save the dataframe to a dictionary with the correspoding year
    dict_processed_data[year] = data
    # print(data)

# In Spring 2024, the spreadsheet has one more column '[Race/Ethnicity' Native Hawaiian or Other Pacific Islander], so I have to add this column to the precious dataframes
# In Spring 2023, the spredsheet has one more clumn '[Sex]  Male.1', so I have to add this column to the other dataframes
all_columns = set()
for df in dict_processed_data.values():
    all_columns.update(df.columns)

desired_order = ['Semester Year', 'CourseLevel', 'CourseName', '[Sex] Female', '[Sex] Male', '[Sex] Male.1', '[First Gen?] Yes',
       '[First Gen?] No/Unreported', '[HUG?] Yes', '[HUG?] No',
       '[Race/Ethnicity] American Indian or Alaska Native',
       '[Race/Ethnicity] Asian', '[Race/Ethnicity] Black or African American',
       '[Race/Ethnicity] Hispanic or Latino',
       '[Race/Ethnicity] Native Hawaiian or Other Pacific Islander',
       '[Race/Ethnicity] Non-Resident Alien',
       '[Race/Ethnicity] Race/Ethnicity Unknown',
       '[Race/Ethnicity] Two or More Races', '[Race/Ethnicity] White',
       'Total Enrollment']

# initialize an empty list to hold the dataframes
df_list = []

# aoop through the dictionary
for year, df in dict_processed_data.items():
    # add the 'Semester Year' column
    df['Semester Year'] = year

    # add any missing columns with 0 values
    for col in all_columns:
        if col not in df.columns:
            df[col] = 0.0000

    df = df[desired_order]

    # append the dataframe to the list
    df_list.append(df)

# concat all dataframes
final_data = pd.concat(df_list, ignore_index=True)

# rename [Sex] Male.1 to undefined
final_data.rename(columns={'[Sex] Male.1': '[Sex] Prefer Not to Say'}, inplace=True)

print(final_data)

# check is the sum of the columns are equal to 100
# if check_sum_100(data):
#     # export the data
#     data.to_csv(f'../results/demographic[{year}].csv', index=True)

# export the data
# final_data.to_csv(f'../results/demographic[{year}].csv', index=True)

final_data.to_csv(f'../results/results_demographic.csv', index=True)