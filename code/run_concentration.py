import pandas as pd
import numpy as np
import argparse
from datetime import datetime
from utils_concentration import *
import warnings
warnings.filterwarnings('ignore')

#############################################
# This script outputs a CSV file listing the concentrations within the Computer Science Department. 
# Each row represents a concentration, and each column shows the percentage of students in various categories. 
# The script concludes with a summary row that calculates the average percentage for each category.
#############################################

# example command line of running this script
# python run_concentration.py 'input_path' 'output_path'
# python run_concentration.py '../data/Concentration Demographics Example.xlsx' '../results'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The path to the input file')
    parser.add_argument('output_file', type=str, help='The path to the output file')
    
    args = parser.parse_args()
    
    input_path = args.input_file
    output_path = args.output_file
    
    print(f"Reading data from {input_path}")
    print(f"Output will be saved to {output_path}")


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
    all_sheets = load_spreadsheet(input_path)

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

    data.to_csv(f'{output_path}/concentration[{current_year}].csv', index=True)


if __name__ == '__main__':
    main()
