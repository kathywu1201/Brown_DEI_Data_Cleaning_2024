# Brown_DEI_Data_Cleaning_2024

## Description
This repository includes the data processing and cleaning scripts for various surveys conducted by the Equity & Diversity Committee at Brown University. The primary goal of this project is to handle and refine data collected from different departmental surveys, ensuring it is cleaned and formatted for further analysis and decision-making.

## Usage
The repository consists of a series of Python scripts located within the 'code' directory. The files prefixed with run_{} are the main scripts that process the raw data into structured CSV files. Supporting utility scripts prefixed with utils_{} are also provided to assist with specific functions needed for data output.

__run_concentration.py:__ This script outputs a CSV file listing the concentrations within the Computer Science Department. Each row represents a concentration, and each column shows the percentage of students in various categories. The script concludes with a summary row that calculates the average percentage for each category.

__run_demographics_individual.py:__ This script generates a CSV file for a selected semester, detailing the courses offered in the Computer Science Department along with their course levels. Each column represents different demographic categories, with the sum of percentages under each category totaling 100%. This script also calculates the average percentage across all courses at each course level.

__run_demographics.py:__ Similar to run_demographics_individual.py, but this script aggregates data across multiple semesters into a single CSV file, providing a broader overview of the demographics over time.

__run_survey.py:__ This script processes survey data into a CSV file where each row corresponds to a response to a survey question, and each column represents different demographic categories across all survey tabs.

__run_survey_questions.py:__ Outputs a text file that contains the full text of each survey question, providing clarity on the data processed in other scripts.

## Built With
- __Python__ - Main programming languge used

### Dependencies
- __Pandas__ - For data manipulation and analysis.
- __NumPy__ - For numerical data processing.

## Contact
If you have any questions about this project, please feel free to contact me using the following email address.\
Yanfeiyun Wu (Kathy), Email: yanfeiyun_wu@brown.edu
