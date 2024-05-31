import pandas as pd
import numpy as np
from datetime import datetime
from data_cleaning_DEI_2024.code.utils_survey import *
import warnings
warnings.filterwarnings('ignore')

#############################################
# Outputs a text file that contains the full text of each survey question, providing clarity on the data processed in other scripts.
#############################################

# path to your Excel file
excel_path = '../data/Percentage Project Example.xlsx'

# any text you want to put to label the questions
label = '06.2024'

# load the Excel file to list all sheet names
xls = pd.ExcelFile(excel_path)
all_sheets = xls.sheet_names

# filter out the 'Summary' sheet
sheets_to_read = [sheet for sheet in all_sheets if sheet != 'Summary']

# since the questions from different sheets are the same, we will only use the first sheet

# read in one sheet at a time
data_groups = extract_data_groups(excel_path, sheets_to_read[0])

# return a document that pair the question numbers and corresponding questions.

# create a list to store formatted strings
formatted_lines = []

# loop through the dictionary keys
for key in data_groups.keys():
    # split the key into question number and question text
    question_number, question_text = key.split('.', 1)

    # format the line
    formatted_line = f"{question_number}: {question_text}"

    # Append to the list
    formatted_lines.append(formatted_line)

with open(f'../results/survey_questions[{label}].txt', 'w') as file:
    for line in formatted_lines:
        file.write(line + '\n')