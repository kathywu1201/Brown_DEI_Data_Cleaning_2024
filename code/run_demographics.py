import pandas as pd
import numpy as np
import argparse
import os
from utils_course_demographics import *
import warnings
warnings.filterwarnings('ignore')

#############################################
'''
This script generates a CSV file for a selected semester, detailing the courses offered in the Computer Science Department along with their course levels. 
Each column represents different demographic categories, with the sum of percentages under each category totaling 100%. 
This script also calculates the average percentage across all courses at each course level.
- return demographics.csv

Note: The output files will be in the same directory as the input file.
'''
#############################################

# example command line of running this script
# python run_demographics.py 'input_file_path'
# python run_demographics.py '../data/Course Demographics Example.xlsx'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The path to the input file')
    
    args = parser.parse_args()
    
    input_file_path = args.input_file
    input_directory = os.path.dirname(input_file_path)
    
    print(f"Reading data from {input_file_path}")

    # load spreadsheet
    df, all_sheets = load_spreadsheet(input_file_path)

    # assume that there is only a single semester in the input file
    for year, data in all_sheets:
        print(f">>> Loading spreadsheet for '{year}'")
        data = df[year]

        # rename the columns
        data = rename_column(data)

        # apply course_level
        data = apply_courselevel(data)

        # calculate the column percentage
        data = calculate_percentage_new(data)

        # there might occur a column that is prefer not to say in the sex tab
        data.rename(columns={'[Sex] Male.1': '[Sex] Prefer Not to Say'}, inplace=True)

        # add the rows with the calcualted average
        data = calculate_average(data)

        # print(data)

        # export the data
        data.to_csv(f'{input_directory}/demographics[{year}].csv', index=True)


if __name__ == '__main__':
    main()