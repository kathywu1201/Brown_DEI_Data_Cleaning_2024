import pandas as pd
import numpy as np
from data_cleaning_DEI_2024.code.utils_course_demographics import *
from utils import *

#############################################
# This script generates a CSV file for a selected semester, detailing the courses offered in the Computer Science Department along with their course levels. 
# Each column represents different demographic categories, with the sum of percentages under each category totaling 100%. 
# This script also calculates the average percentage across all courses at each course level.
#############################################

# fill out the path to the spreadsheets and select the specific semester year we want
file_path = '../data/Course Demographics Example.xlsx'
year = 'Spring 2024'

# load spreadsheet
df, all_sheets = load_spreadsheet(file_path)

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

data.rename(columns={'[Sex] Male.1': '[Sex] Prefer Not to Say'}, inplace=True)

# add the rows with the calcualted average
data = calculate_average(data)

# print(data)

# export the data
data.to_csv(f'../results/demographic[{year}].csv', index=True)
