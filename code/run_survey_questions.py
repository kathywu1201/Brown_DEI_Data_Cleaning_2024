import pandas as pd
import numpy as np
from datetime import datetime
import argparse
from utils_survey import *
import warnings
warnings.filterwarnings('ignore')

#############################################
# Outputs a text file that contains the full text of each survey question, providing clarity on the data processed in other scripts.
#############################################

# example command line of running this script
# python run_survey_questions.py 'input_path' 'output_path' 'desired_label'
# python run_survey_questions.py '../data/Percentage Project Example.xlsx' '../results' 'ver06.2024'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The path to the input file')
    parser.add_argument('output_file', type=str, help='The path to the output file')
    parser.add_argument('desired_label', type=str, help='Desired label of the extracted questions, e.g. data, version')
    
    args = parser.parse_args()
    
    input_path = args.input_file
    output_path = args.output_file
    label = args.desired_label

    print(f"Reading data from {input_path}")
    print(f"Output will be saved to {output_path}")


    # load the Excel file to list all sheet names
    xls = pd.ExcelFile(input_path)
    all_sheets = xls.sheet_names

    # filter out the 'Summary' sheet
    sheets_to_read = [sheet for sheet in all_sheets if sheet != 'Summary']

    # since the questions from different sheets are the same, we will only use the first sheet

    # read in one sheet at a time
    data_groups = extract_data_groups(input_path, sheets_to_read[0])

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

    with open(f'{output_path}/survey_questions[{label}].txt', 'w') as file:
        for line in formatted_lines:
            file.write(line + '\n')


if __name__ == '__main__':
    main()