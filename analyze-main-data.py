# This is a rough problem-solving script.
# I knew almost nothing about the data and needed to poke at it 
#    for a while.  The *_time columns are a mess.
#  incident_date --> remove bogus time, convert date to pd.date
#  response_level
#  call_type
#  Unit_Dispatch_Times --> isolate "team" and "time" components
#  Unit_Enroute_Times --> isolate "team" and "time" components
#  Unit_Arrive_Times --> isolate "team" and "time" components
#  Unit_At_Patient_Times --> isolate "team" and "time" components
#  Unit_Enroute_To_Hospital_Times --> isolate "team" and "time" components
#  Unit_Arrive_At_Hospital_Times --> isolate "team" and "time" components
#  Unit_Staging_Times --> isolate "team" and "time" components
#  Unit_Fire_Out_Times --> isolate "team" and "time" components
#  Unit_Clear_Times --> isolate "team" and "time" components
#  Time_In_Service --> isolate "team" and "time" components

from pathlib import Path
import ast
import sys
import os
import pandas as pd
import datetime
import numpy as np
import shutil
import re

start = datetime.datetime.now()
dir_path = os.getcwd()


def create_target_csv_data_file(csvfile_suffix: object) -> object:
    # create a file with date as a name day-month-year
    filename_suffix = csvfile_suffix
    filename_prefix = start.strftime('%Y-%m-%d')
    filename = f"{filename_prefix}_{filename_suffix}"
    # Put the new file in the current directory
    csv_file_name: str = os.path.join(dir_path, filename)
    return csv_file_name


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def minimum_py(min_python_major_version=3, min_python_minor_version=10):
    # Use a breakpoint in the code line below to debug your script.
    if sys.version_info < (int(min_python_major_version), int(min_python_minor_version)):
        raise Exception("Use only with Python {min_python_major_version}.{min_python_minor_version} or higher")
    else:
        return True


def print_separator_line():
    print(f'- - - - - - - - - - - - - - - - - - - - - - - -')


def report_start(dirpath):
    # Documenting the start & end time
    print("\r\n")
    print_separator_line()
    # print("-------------------------------------------------------------")
    print(__file__ + " Report started at: %s" % start)
    print("Root of target filesystem: %s" % dirpath)
    print_separator_line()
    # print("-------------------------------------------------------------")
    ## print("\r\n")


def report_end(csvfile):
    script_ended = datetime.datetime.now()
    print_separator_line()
    # print("-------------------------------------------------------------")
    print(__file__ + " Report ended at: %s" % script_ended)
    print("Search Report took: %s " % str(script_ended - start))
    print("Target Report Files: %s" % csvfile)
    print_separator_line()
    # print("-------------------------------------------------------------")
    print("\r\n")

def data_description(data_frame):
    # Overview of the data:
    # print_separator_line()
    # print(f'Overview of the data {data_frame.info()}')
    print_separator_line()
    # How many rows & columns are there?
    print(f'There are {data_frame.shape[0]} records and {data_frame.shape[1]} columns in {e_data_file}')
    print_separator_line()
    # What are the column names & types?
    print(f'Column names and Python data types include: ')
    for column_name in data_frame.columns:
        print(f'\t{column_name} type is {data_frame.dtypes[column_name]}')
    print_separator_line()
    # percentile list
    perc = [.10, .20, .40, .60, .80, .90]
    # list of dtypes to include
    include = ['object', 'float', 'int', 'datetime64[ns]']
    # calling describe method
    desc = temp_data_frame_w_dates.describe(percentiles=perc, include=include, datetime_is_numeric=True)
    # display
    print(desc)
    print_separator_line()
    # Now describe each column
    # calling describe method
    desc = temp_data_frame_w_dates["incident_date"].describe(percentiles=perc, include=include, datetime_is_numeric=True)
    # display
    print(f"{desc}")
    print_separator_line()
    #
    desc = temp_data_frame_w_dates["response_unit"].describe(percentiles=perc, include=include, datetime_is_numeric=True)
    # desc = temp_data_frame_w_dates.response_unit.describe(percentiles=perc, include=include, datetime_is_numeric=True)
    # per: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html
    print(f"{desc}")
    print_separator_line()
    #
    desc = temp_data_frame_w_dates["dispatch_time"].describe(percentiles=perc, include=include, datetime_is_numeric=True)
    print(f"{desc}")
    print_separator_line()
    #
    desc = temp_data_frame_w_dates["time_in_service"].describe(percentiles=perc, include=include, datetime_is_numeric=True)
    print(f"{desc}")
    print_separator_line()


def convert_column_to_date(data_frame):
    for index in data_frame.index:
        # Remove the bogus time from the incident_date column
        temp_incident_date = f"{data_frame.loc[index, 'incident_date']}"
        data_frame.loc[index, 'incident_date'] = temp_incident_date.split(' ', 2)[0]
        # Remove the bogus date from the dispatch_time column
        temp_dispatch_time = f"{data_frame.loc[index, 'dispatch_time']}"
        data_frame.loc[index, 'dispatch_time'] = temp_dispatch_time.split(' ', 1)[0]
        # Remove the bogus date from the time_in_service column
        temp_time_in_service = f"{data_frame.loc[index, 'time_in_service']}"
        data_frame.loc[index, 'time_in_service'] = temp_time_in_service.split(' ', 1)[0]
        ### data_frame.loc[index, 'incident_date'] = pd.to_datetime(data_frame.loc[index, 'incident_date']) # # datetime.datetime.strptime(data_frame.loc[index, 'incident_date'], "%m/%d/%y")
        # print(f'Overview of the data {data_frame.info()}')
        # print(f"{(data_frame.loc[index, 'incident_date']).strftime('%d/%m/%y')}")
        # print(f"{(data_frame.loc[index, 'incident_date'])}")
        # print(f"{type(data_frame.loc[index, 'incident_date'])}")
        # print(temp_incident_date_slice[0])
        # date[temp_incident_date_slice[0]] = datetime.strptime(date['incident_date'], "%Y-%m-%d hh:mm [am|pm]")
    # Convert the incident_date column to <class 'pandas._libs.tslibs.timestamps.Timestamp'>
    #   which is also datetime64[ns]
    # Either of the following approaches works, but pandas barks about it.
    # raw_data['Mycol'] = pd.to_datetime(raw_data['Mycol'], format='%d%b%Y:%H:%M:%S.%f')
    # Format strings: https://strftime.org/
    # https://stackoverflow.com/questions/26763344/convert-pandas-column-to-datetime
    # data_frame['incident_date'] = pd.to_datetime(data_frame['incident_date'], format='%m/%d/%y')
    # data_frame['dispatch_time'] = pd.to_datetime(data_frame['dispatch_time'], format='%H:%M:%S')
    # data_frame['time_in_service'] = pd.to_datetime(data_frame['time_in_service'], format='%H:%M:%S')
    # This is the second way:
    data_frame['incident_date'] = pd.to_datetime(data_frame.loc[:, 'incident_date'], format='%m/%d/%y')
    data_frame['dispatch_time'] = pd.to_datetime(data_frame.loc[:, 'dispatch_time'], format='%H:%M:%S')
    data_frame['time_in_service'] = pd.to_datetime(data_frame.loc[:, 'time_in_service'], format='%H:%M:%S')
    # Check the data type:
    print(f"incident_date type is: {type(data_frame.loc[index,'incident_date'])}")
    print(f"dispatch_time type is: {type(data_frame.loc[index,'dispatch_time'])}")
    print(f"time_in_service type is: {type(data_frame.loc[index,'time_in_service'])}")
    # Sanity check the columns of data
    # print(f'Overview of the data {data_frame.info()}')
    return data_frame


def convert_date_string_to_date(data_frame):
    # From: https://stackoverflow.com/questions/36753868/python-convert-dictionary-of-string-times-to-date-times
    dates = data_frame['incident_date']
    for date in dates:
        date['incident_date'] = datetime.strptime(date['incident_date'], "%Y-%m-%d hh:mm [am|pm]")
    data_description(data_frame)


def get_only_dates(data_frame):
    dates = data_frame['incident_date']
    for date in dates:
        date.split(' ')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Enforce a minimum Python version
    min_major_version = 3
    min_minor_version = 10
    minimum_py(min_major_version, min_minor_version)
    # Use a set: collection of unordered unique elements without duplicates {}
    emergency_data_list = []
    report_start(dir_path)
    #csv_data_filename_suffix: str = 'emerg_data_organized.csv'
    #csv_data_filename: str = create_target_csv_data_file(csv_data_filename_suffix)
    # Get the source csv file and assign it to a dataframe called emergency_data
    # Enter the path to the raw data file here:
    e_data_file = Path("./2023-01-21_emerg_data_organized.csv")
    # Read the data into a Pandas dataframe
    if e_data_file.exists():
        emergency_data_all = pd.read_csv(e_data_file, sep=',')
        emergency_data = emergency_data_all  # .head(10)
    print_separator_line()
    # Overview of the data
    # print(f"Overview of the data {emergency_data.info()}")
    # print_separator_line()
    # How many rows & columns are there? What are the column names & types?
    # print(f"Initial data_description of the data: ")
    # data_description(emergency_data)
    # print_separator_line()
    temp_data_frame = emergency_data.head(10)
    ## temp_data_frame = emergency_data
    # We need the .copy() below to stop Pandas from complaining with
    # "SettingWithCopyWarning" for the pd.to_datetime in convert_column_to_date()
    # See: https://stackoverflow.com/questions/71458707/pandas-settingwithcopywarning-for-pd-to-datetime
    temp_data_frame_w_dates = pd.DataFrame(convert_column_to_date(temp_data_frame.copy()))
    # Silencing: FutureWarning: Treating datetime data as categorical rather than
    # numeric in `.describe` is deprecated...
    datetime_is_numeric = True
    # removing null values to avoid errors
    temp_data_frame_w_dates.dropna(inplace=True)
    # print(f"Overview of the data {temp_data_frame_w_dates.info()}")
    data_description(temp_data_frame_w_dates)
    print_separator_line()
    # 
    # https://stackabuse.com/reading-and-writing-csv-files-in-python-with-pandas/
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.get.html
    # https://www.geeksforgeeks.org/python-pandas-dataframe-describe-method/
    # 

