import pandas as pd
import numpy as np
from course_demographics import *
from utils import *

# fill out the path to the spreadsheets and select the specific semester year we want
file_path = '../data/Course Demographics Example.xlsx'
year = 'Spring 2023'

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

print(data)

# check is the sum of the columns are equal to 100
# if check_sum_100(data):
#     # export the data
#     data.to_csv(f'../results/demographic[{year}].csv', index=True)

# export the data
data.to_csv(f'../results/demographic[{year}].csv', index=True)
