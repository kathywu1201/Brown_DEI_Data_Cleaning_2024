import pandas as pd
import numpy as np
import argparse
from utils_course_demographics import *
import warnings
warnings.filterwarnings('ignore')

#############################################
# Similar to run_demographics_individual.py, but this script aggregates data across multiple semesters into a single CSV file, 
# providing a broader overview of the demographics over time.
#############################################

# example command line of running this script
# python run_demographics.py 'input_path' 'output_path'
# python run_demographics.py '../data/Course Demographics Example.xlsx' '../results'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='The path to the input file')
    parser.add_argument('output_file', type=str, help='The path to the output file')
    
    args = parser.parse_args()
    
    input_path = args.input_file
    output_path = args.output_file
    
    print(f"Reading data from {input_path}")
    print(f"Output will be saved to {output_path}")


    # load spreadsheet
    df, all_sheets = load_spreadsheet(input_path)

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
        data = calculate_percentage_new(data)

        # rename [Sex] Male.1 to undefined, which appears in Spring 2023
        data.rename(columns={'[Sex] Male.1': '[Sex] Prefer Not to Say'}, inplace=True)

        # add the rows with the calcualted average
        data = calculate_average(data)

        # export the data
        data.to_csv(f'../results/demographic[{year}].csv', index=True)

        # save the dataframe to a dictionary with the correspoding year
        dict_processed_data[year] = data
        # print(data)

    # In Spring 2024, the spreadsheet has one more column '[Race/Ethnicity' Native Hawaiian or Other Pacific Islander], so I have to add this column to the precious dataframes
    # In Spring 2023, the spredsheet has one more column '[Sex]  Male.1' which is renamed to '[Sex] Prefer Not to Say',
    # so I have to add this column to the other dataframes
    all_columns = set()
    for df in dict_processed_data.values():
        all_columns.update(df.columns)

    desired_order = ['Semester Year', 'CourseLevel', 'CourseName', '[Sex] Female', '[Sex] Male', '[Sex] Prefer Not to Say', '[First Gen?] Yes',
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

    # print(final_data)

    final_data.to_csv(f'{output_path}/results_demographic.csv', index=True)


if __name__ == '__main__':
    main()