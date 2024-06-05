import pandas as pd
import numpy as np
import argparse
from datetime import datetime
import os
from utils_concentration import *
import warnings
warnings.filterwarnings('ignore')

#############################################
'''
(1) This script outputs a CSV file listing the concentrations within the Computer Science Department. 
Each row represents a concentration, and each column shows the percentage of students in various categories. 
The script concludes with a summary row that calculates the average percentage for each category.
- return concentration.csv

Note: The output files will be in the same directory as the input file.
'''
#############################################

# example command line of running this script
# python run_concentration.py 'input_file_path'
# python run_concentration.py '../data/Concentration Demographics Example.xlsx'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The path to the input file')
    
    args = parser.parse_args()
    
    input_file_path = args.input_file
    input_directory = os.path.dirname(input_file_path)
    
    print(f"Reading data from {input_file_path}")

    # concentration abbrev.
    concentration_dict = {
        "Applied Math.-Computer Sci.": 'APMA-CS' ,
        "Computational Biology": 'Comp Bio' ,
        "Computer Science": 'CS',
        "Computer Science-Economics": 'CS-Econ',
        "Mathematics-Computer Science": 'Math-CS',
        'Cybersecurity' : "Cybersecurity" ,
    }
    current_year = datetime.now().year

    # load all sheets
    all_sheets = load_spreadsheet(input_file_path)

    # concat all sheets into one dataframe + filling the nan with 'N' or 'None'
    data = concat_sheets(all_sheets)

    # change the 'Intended Completion Term' to the years with respect to the current year
    data = relative_year(data)

    # count the number of students in each category and concat all
    data = count_category(data)

    # calculate the total Enrollment for each concentration
    data = calculate_total_enrollment(data)

    # raname the columns and turn to desired format
    data = rename_columns(data)

    # calculate the percentage of each category in each concentration with respect to the column sum
    data = calculate_percentage_new(data)

    # add the rows with the calcualted average
    data = calculate_average(data)

    # change the full concentration name to its abbreviation
    data['Concentration'] = data['Concentration'].replace(concentration_dict)
    # print(data)

    data.to_csv(f'{input_directory}/concentration[{current_year}].csv', index=True)


if __name__ == '__main__':
    main()
