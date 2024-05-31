import pandas as pd
import numpy as np
from datetime import datetime
from survey import *
import warnings
warnings.filterwarnings('ignore')

#############################################
# This script processes survey data into a CSV file where each row corresponds to a response to a survey question, 
# and each column represents different demographic categories across all survey tabs.
#############################################

# path to your Excel file
excel_path = '../data/Percentage Project Example.xlsx'

# load the Excel file to list all sheet names
xls = pd.ExcelFile(excel_path)
all_sheets = xls.sheet_names

# filter out the 'Summary' sheet
sheets_to_read = [sheet for sheet in all_sheets if sheet != 'Summary']

# create an exmpty dictionary to store dataframe from each sheet with the corersponding sheet name
dict_all_sheets = {}
for sheet_name in sheets_to_read:
    # print(f'----{sheet_name}----')
    # read in one sheet at a time
    data_groups = extract_data_groups(excel_path, sheet_name)

    # transform the data in this sheet
    for key in data_groups.keys():
        data_groups[key] = transform_and_transpose(data_groups[key])

    # assign question number to each option
    dict_df = data_groups.copy()
    dict_df = prepend_question_number_to_df(dict_df)

    # for each question, a desired dataframe is done
    for key in dict_df.keys():
        dict_df[key] = combine_question_number(dict_df[key])
    
    # collect all DataFrames from the dictionary
    dataframes_list = list(dict_df.values())  

    # concat all dataframes vertically
    combined_df = pd.concat(dataframes_list, axis=0, ignore_index=True)
    questoin_df = combined_df[['Questions']]
    combined_df = combined_df.drop(columns=['Questions'])
    # print(combined_df.shape)

    # save the processed dataframe with the corresponding sheet name
    dict_all_sheets[sheet_name] = combined_df

# add a new level to the column of the question_df
new_level = ''
questoin_df.columns = pd.MultiIndex.from_tuples([(new_level, col) for col in questoin_df.columns])
questoin_df.reset_index(inplace=True)

# concat all the dataframe in all the sheetnames
res_df = pd.concat(dict_all_sheets.values(), axis=1, keys=dict_all_sheets.keys())
res_df.reset_index(inplace=True)

# merge the question and responce together
final_df = questoin_df.merge(res_df, how='left', on='index')
final_df.drop(columns=[('index','')], inplace=True)

# export the data
current_year = datetime.now().year
final_df.to_csv(f'../results/survey_percentage[{current_year}].csv', index=True)