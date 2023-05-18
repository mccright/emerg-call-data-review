# This is a rough problem-solving script.
# I knew almost nothing about the data and needed to poke at it 
#    for a while.  The *_time columns are a mess.
#  incident_date --> remove bogus time, convert date to pd.date
#  response_level
#  call_type --> See: https://en.wikipedia.org/wiki/Medical_Priority_Dispatch_System
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
    # Convert the incident_date column to <class 'pandas._libs.tslibs.timestamps.Timestamp'>
    #   which is also datetime64[ns]
    # Either of the following approaches works, but pandas barks about it.
    # data_frame['incident_date'] = pd.to_datetime(data_frame['incident_date'])
    # This is the second way:
    data_frame['incident_date'] = pd.to_datetime(data_frame.loc[:, 'incident_date'])
    # Check the data type:
    #   print(f"{type(data_frame.loc[index,'incident_date'])}")
    # Sanity check the columns of data
    #   print(f'Overview of the data {data_frame.info()}')
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
    csv_data_filename_suffix: str = 'emerg_data_organized.csv'
    csv_data_filename: str = create_target_csv_data_file(csv_data_filename_suffix)
    # Get the source csv file and assign it to a dataframe called emergency_data
    # Enter the path to the raw data file here:
    e_data_file = Path("./rawdata/rvfd-calls-for-service-2010-2020.csv")
    # e_data_file = './rawdata/rvfd-calls-for-service-2010-2020.csv'
    # Read the data into a Pandas dataframe
    if e_data_file.exists():
        emergency_data = pd.read_csv(e_data_file, sep=',')
    # replacing nan values in call_type and Unit_Dispatch_Times with "None"
    # From: https://www.geeksforgeeks.org/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
    emergency_data["call_type"].fillna("None", inplace=True)
    emergency_data["Unit_Dispatch_Times"].fillna("None", inplace=True)
    ## ToDo: Add the following two columns:
    #  Unit_Enroute_Times --> isolate "team" and "time" components
    #  Unit_Arrive_Times --> isolate "team" and "time" components
    ##
    # How many rows & columns are there? What are the column names & types?
    # data_description(emergency_data)
    # temp_data_frame = emergency_data.head(10)
    temp_data_frame = emergency_data
    # We need the .copy() below to stop Pandas from complaining with
    # "SettingWithCopyWarning" for the pd.to_datetime in convert_column_to_date()
    # See: https://stackoverflow.com/questions/71458707/pandas-settingwithcopywarning-for-pd-to-datetime
    temp_data_frame_w_dates = pd.DataFrame(convert_column_to_date(temp_data_frame.copy()))
    # print(f'Overview of the data {temp_data_frame_w_dates.info()}')
    # data_description(temp_data_frame)
    counter = 0
    length = len(temp_data_frame_w_dates)
    while length > counter:
        ## ToDo: Add the following two columns:
        #  Unit_Enroute_Times --> Column 9; isolate "team" and "time" components
        #  Unit_Arrive_Times --> Column 10; isolate "team" and "time" components
        ##
        # map each to a dictionary
        temp_values = ""
        # call_type is column 7
        call_type_dict = {}
        temp_str_call_type_dict = temp_data_frame_w_dates.values[counter][7]
        # stringified_call_type_times: str = ""
        # stringified_call_type_times = str(temp_str_call_type_dict)
        stringified_unit_dispatch_times: str = ""
        # stringified_unit_dispatch_times = ""
        stringified_unit_time_in_service_times_dict: str = ""
        unit_dispatch_times_dict = {}
        unit_time_in_service_times_dict = {}
        # Unit_Dispatch_Times is column 8
        temp_str_unit_dispatch_dict = temp_data_frame_w_dates.values[counter][8]
        stringified_unit_dispatch_times = str(temp_str_unit_dispatch_dict)
        # Time_In_Service is column 17
        temp_str_unit_time_in_service_dict = temp_data_frame_w_dates.values[counter][17]
        stringified_unit_time_in_service_dict = str(temp_str_unit_time_in_service_dict)
        # Up to four prints for debugging
        # print(f"temp_str_unit_dispatch_dict = {temp_str_unit_dispatch_dict}")
        # print(f"stringified_unit_dispatch_times = {stringified_unit_dispatch_times}")
        # print(f"temp_str_unit_time_in_service_dict = {temp_str_unit_time_in_service_dict}")
        # print(f"stringified_unit_time_in_service_dict = {stringified_unit_time_in_service_dict}")
        #
        # Need data in the 'Unit_Dispatch_Times column', the 8th column
        # Checking the eighth column for 'none' - not very portable
        if temp_data_frame_w_dates.values[counter][8] == "None":
            # Skip the nulls
            counter += 1
            continue
            # using strip() and split()  methods
        # Also need data in the 'Time_In_Service column', the 17th column
        # Checking the seventeenth column for 'none' - not very portable
        ## ToDo: Add the following two columns:
        #  Unit_Enroute_Times --> Column 9; isolate "team" and "time" components
        #  Unit_Arrive_Times --> Column 10; isolate "team" and "time" components
        ##
        if temp_data_frame_w_dates.values[counter][17] == "None":
            # Skip the nulls
            counter += 1
            continue
        # We confirmed 'Unit_Dispatch_Time' and 'Time_In_Service' data
        else:
            # get 'response_team=time' pairs from column 8 unit_dispatch_times
            try:
                unit_dispatch_times_dict = dict((a.strip(), b.strip())
                                                for a, b in (element.split('=')
                                                             for element in stringified_unit_dispatch_times.split(', ')))
            except Exception as e:
                print(f'{e}')
            # Now 17
            try:
                unit_time_in_service_times_dict = dict((a.strip(), b.strip())
                                                for a, b in (element.split('=')
                                                             for element in stringified_unit_time_in_service_dict.split(', ')))
            except Exception as e:
                print(f'{e}')
            # Print what we learned for debugging
            print(f'Record: {counter}')
            ## print("The resultant dictionary is: ", unit_dispatch_times_dict)
            for i in sorted(unit_dispatch_times_dict.keys()):
                ## print(f"{datetime.datetime.strftime(temp_data_frame_w_dates.loc[counter, 'incident_date'], '%m/%d/%y')}\t{i} -> {unit_dispatch_times_dict[i]} and time_in_service was {unit_time_in_service_times_dict[i]}")
                csv_string = f"\"{datetime.datetime.strftime(temp_data_frame_w_dates.loc[counter, 'incident_date'], '%m/%d/%y')}\",\"{i}\",\"{temp_data_frame_w_dates.loc[counter, 'call_type'].strip()}\",\"{unit_dispatch_times_dict[i]}\",\"{unit_time_in_service_times_dict[i]}\"\n"
                emergency_data_list.append(csv_string)
                # print(f"The type for {unit_dispatch_times_dict[i]} is {type(unit_dispatch_times_dict[i])}")
                diff = unit_dispatch_times_dict[i] + unit_time_in_service_times_dict[i]
                # Print the difference in days, hours, minutes, and seconds
                ## print(f"The difference is {diff}")
            # print("The resultant dictionary is: ", unit_dispatch_times_dict)
            counter += 1

    # Header row for csv file:
    ## ToDo: Add the following two columns:
    #  Unit_Enroute_Times --> Column 9; isolate "team" and "time" components
    #  Unit_Arrive_Times --> Column 10; isolate "team" and "time" components
    ##
    csv_header_string = f"\"incident_date\",\"response_unit\",\"call_type\",\"dispatch_time\",\"time_in_service\"\n"
    # create a text file for writing
    with open(csv_data_filename, 'a') as f:
        f.writelines(csv_header_string)
        f.writelines(emergency_data_list)

        """
        for key in temp_dict:
            print(f'{type(key)}')
        counter += 1
    """
    # print(f'{emergency_data.head()}')
    target_file = 'headers.py'
    try:
        fprUtil = shutil.which(target_file)
    except shutil.Error as err:
        raise Exception(f'{err}')
    if fprUtil is None:
        print(f'Did not find {target_file} in the path. Returned: {fprUtil}')
    else:
        print(f'Found: {fprUtil}')
    report_end(dir_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
