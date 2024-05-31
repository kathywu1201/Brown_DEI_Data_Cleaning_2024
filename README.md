# Brown_DEI_Data_Cleaning_2024

## Description
This project is under the Equity & Diversity Committe at Brown University. The main purpose of this project is to do data processing and cleanning for various survey done in the department.

## Usage
The scripts that need to be run is in the code file. The file names start with 'run_{}.py' are the scripts that we need to run and output processed and cleaned csv files. Other pthon files are the utils that include the necessary functions that need to be used in outputing each csv files.

__run_concentration.py:__ returns a csv file where each row are the concentrations under the Computer Science Department and columns indicates the percentage in various categories. In the end of this file, there also includes a summary row that calculate the average percentage of each column categories.

__run_demographics_indivisual.py:__ returns a csv file of a selected semester that you want to take a look. Each row are the courses offered in the Computer Science Department and the corresponding course level; each columns indicates the parcentage in various categories, under the same tag [], the sum of the percentage is 100%. The percentages are calculated with respect to the total enrollment of each course offered in the department in the selected semester. Additionally, for each course level and all courses, there is a row that calculate the average percentage along each column.

__run_demographics.py:__ return a csv file of all the semester. The output of this scripts is similar to the indivisual one but is an aggreation of a bunch of semesters.

__run_survey.py:__ 
## Contact
If you have any questions about this project, please feel free to contact me using the following email address.\
Yanfeiyun Wu (Kathy), Email: yanfeiyun_wu@brown.edu
