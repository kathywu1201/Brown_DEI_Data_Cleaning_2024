import pandas as pd
import numpy as np
import argparse
from utils_course_demographics import *
import warnings
warnings.filterwarnings('ignore')

#############################################
# This script generates a CSV file for a selected semester, detailing the courses offered in the Computer Science Department along with their course levels. 
# Each column represents different demographic categories, with the sum of percentages under each category totaling 100%. 
# This script also calculates the average percentage across all courses at each course level.
#############################################

# example command line of running this script
# python run_demographics_individual.py 'input_path' 'output_path' 'desired_semester'
# python run_demographics_individual.py '../data/Course Demographics Example.xlsx' '../results' 'Fall 2023'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The path to the input file')
    parser.add_argument('output_file', type=str, help='The path to the output file')
    parser.add_argument('desired_semester', type=str, help='The semester name of the spreadsheet')
    
    args = parser.parse_args()
    
    input_path = args.input_file
    output_path = args.output_file
    year = args.desired_semester
    
    print(f"Reading data from {input_path}")
    print(f"from semester {year}")
    print(f"Output will be saved to {output_path}")


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


if __name__ == '__main__':
    main()