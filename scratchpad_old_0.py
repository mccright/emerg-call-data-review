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

import ast
import sys
import pandas as pd
import datetime
import numpy as np
import shutil


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


def data_description(data_frame):
    # Overview of the data:
    print_separator_line()
    print(f'Overview of the data {data_frame.info()}')
    print_separator_line()
    # How many rows & columns are there?
    print(f'There are {data_frame.shape[0]} records and {data_frame.shape[1]} columns in {e_data_file}')
    print_separator_line()
    # What are the column names & types?
    print(f'Column names and Python data types include: ')
    for column_name in data_frame.columns:
        print(f'\t{column_name} type is {data_frame.dtypes[column_name]}')
    print_separator_line()


def convert_column_to_date(data_frame):
    for index in data_frame.index:
        # Remove the bogus time from the incident_date column
        temp_incident_date = f"{data_frame.loc[index, 'incident_date']}"
        data_frame.loc[index, 'incident_date'] = temp_incident_date.split(' ', 1)[0]
        ### data_frame.loc[index, 'incident_date'] = pd.to_datetime(data_frame.loc[index, 'incident_date']) # # datetime.datetime.strptime(data_frame.loc[index, 'incident_date'], "%m/%d/%y")
        # print(f'Overview of the data {data_frame.info()}')
        # print(f"{(data_frame.loc[index, 'incident_date']).strftime('%d/%m/%y')}")
        # print(f"{(data_frame.loc[index, 'incident_date'])}")
        # print(f"{type(data_frame.loc[index, 'incident_date'])}")
        # print(temp_incident_date_slice[0])
        # date[temp_incident_date_slice[0]] = datetime.strptime(date['incident_date'], "%Y-%m-%d hh:mm [am|pm]")
    # Convert the incident_date column to datetime64[ns]
    data_frame['incident_date'] = pd.to_datetime(data_frame['incident_date'])
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
    # Get the csv file and assign it to a dataframe called emergency_data
    # Enter the path to the raw data file here:
    e_data_file = './rawdata/rvfd-calls-for-service-2010-2020.csv'
    # Read the data into a Pandas dataframe
    emergency_data = pd.read_csv(e_data_file, sep=',')
    # replacing nan values in Unit_Dispatch_Times with "None"
    # From: https://www.geeksforgeeks.org/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
    emergency_data["Unit_Dispatch_Times"].fillna("None", inplace=True)
    # How many rows & columns are there? What are the column names & types?
    # data_description(emergency_data)
    temp_data_frame = emergency_data.head(10)
    temp_data_frame_w_dates = pd.DataFrame(convert_column_to_date(temp_data_frame))
    # print(f'Overview of the data {temp_data_frame_w_dates.info()}')
    # data_description(temp_data_frame)
    counter = 0
    length = len( temp_data_frame_w_dates)
    while length > counter:
        # map each to a dictionary
        temp_values = ""
        stringified_unit_dispatch_times = ""
        unit_dispatch_times_dict = {}
        temp_str_dict = {}
        # Unit_Dispatch_Times is column 8
        temp_str_dict = temp_data_frame_w_dates.values[counter][8]
        stringified_unit_dispatch_times = str(temp_str_dict)
        if temp_data_frame_w_dates.values[counter][8] == "None":
            # Skip the nulls
            counter += 1
            continue
            # using strip() and split()  methods
        else:
            try:
                unit_dispatch_times_dict = dict((a.strip(), b.strip())
                                                for a, b in (element.split('=')
                                                             for element in stringified_unit_dispatch_times.split(', ')))
            except Exception as e:
                print(f'{e}')
            print(f'Record: {counter}')
            for i in sorted(unit_dispatch_times_dict.keys()):
                print(f"{datetime.datetime.strftime(temp_data_frame_w_dates.loc[counter, 'incident_date'], '%m/%d/%y')}\t{i} -> {unit_dispatch_times_dict[i]}")
            # print("The resultant dictionary is: ", unit_dispatch_times_dict)
            counter += 1

        """
        for key in temp_dict:
            print(f'{type(key)}')
        counter += 1
    """
    # print(f'{emergency_data.head()}')



