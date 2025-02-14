# This script adds columns to make some sorting and comparisons easier and faster:
# One column having only the year of each incident (from incident_date)
# Four converting dispatch_times, enroute_times, arrive_times and time_in_service times to seconds.
#
# This script will emit a csv file with the following columns:
#     incident_date
#     incident_date_year_only
#     response_unit
#     call_type
#     dispatch_time
#     dispatch_time_in_seconds
#     enroute_time
#     enroute_time_in_seconds
#     arrive_time
#     arrive_time_in_seconds
#     time_in_service
#     time_in_service_in_seconds

from pathlib import Path
import sys
import os
import pandas as pd
from pandas import DataFrame
import datetime
import pathlib
import tempfile
import string
import random
import logging


# provide both local time and UTC time to better support
# distributed operations
start = datetime.datetime.now()
start_utc = datetime.datetime.now(datetime.timezone.utc)
dir_path = os.getcwd()

_LOGGER = logging.getLogger(__name__)


def create_target_csv_data_file(csvfile_suffix: str) -> object:
    """
    Creates a path/file object with filename day-month-year
    Builds the filename with {date}_{csvfile_suffix}.
    Appends the filename to the current directory.
    :param csvfile_suffix: str
    :rtype: object
    """
    #
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


def print_separator_line() -> str:
    print_separator = f'- - - - - - - - - - - - - - - - - - - - - - - -'
    return print_separator


def report_start(dirpath: str) -> str:
    """
    Documenting the report start time.

    Provides both local time and UTC time for distributed operations.
    Assumes "start" and "start_utc" are set at the top of the script.
    :param dirpath: root of target filesystem
    :type  dirpath: str
    :return report_start_msg: start of report message content
    """
    report_start_msg = f"\n\n{print_separator_line()}\n"
    report_start_msg = report_start_msg + f"{__file__}\n"
    report_start_msg = report_start_msg + f"Report started at: {start} local, {start_utc} UTC\n"
    report_start_msg = report_start_msg + f"Root of target filesystem: {dirpath}\n"
    report_start_msg = report_start_msg + f"{print_separator_line()}"
    return report_start_msg


def report_end(csvfile: str) -> str:
    """
    Documenting the report end time.
    Provides both local time and UTC time for distributed operations.
    :param csvfile: the report's full path + filename
    :type csvfile: str
    :return report_end_msg: end of report message content
    """
    script_ended = datetime.datetime.now()
    script_ended_utc = datetime.datetime.now(datetime.timezone.utc)
    report_end_msg = f"\n\n{print_separator_line()}\n"
    report_end_msg = report_end_msg + f"{__file__}\n"
    report_end_msg = report_end_msg + f"Report started at: {start} local, {start_utc} UTC\n"
    report_end_msg = report_end_msg + f"Report ended at: {script_ended} local, {script_ended_utc} UTC\n"
    report_end_msg = report_end_msg + f"Report took: {(script_ended - start)}\n"
    report_end_msg = report_end_msg + f"Reporting processed {length} input records and output {outputfilelength} records\n"
    report_end_msg = report_end_msg + f"Report Output Files: {csvfile}\n"
    report_end_msg = report_end_msg + f"{print_separator_line()}"
    return report_end_msg


def data_description(data_frame):
    """ 
    Overview of the data.
    Support for debugging.
    """
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
    """
    Remove the bogus time from the incident_date column, then 
    Convert the incident_date column to <class 'pandas._libs.tslibs.timestamps.Timestamp'>
    which is also datetime64[ns].
    :param data_frame: DataFrame
    :type csvfile: str
    :return: DataFrame
    """
    for index in data_frame.index:
        # Remove the bogus time from the incident_date column
        # For a discussion about the reasons for using df.loc[] see:
        # https://stackoverflow.com/questions/48409128/what-is-the-difference-between-using-loc-and-using-just-square-brackets-to-filte/48411543#48411543
        # and https://stackoverflow.com/questions/76766136/pandas-pd-to-datetime-assigns-object-dtype-instead-of-datetime64ns
        temp_incident_date = f"{data_frame.loc[index, 'incident_date']}"
        data_frame.loc[index, 'incident_date'] = temp_incident_date.split(' ', 1)[0]
    # Pandas issue helped parse the dates correctly:
    # https://github.com/pandas-dev/pandas/issues/52167
    data_frame['incident_date'] = pd.to_datetime(data_frame.loc[:, 'incident_date'], format='mixed')
    return data_frame


def convert_date_column_to_year(data_frame, date_column: str):
    """
    convert the data in a pandas dataframe datetime column in-place
    from YYYY-mm-dd hh:mm:ss format into just YYYY-mm-dd
    :type data_frame: object
    :type date_column: str
    :param data_frame: object
    :param date_column: datetime64[ns]
    :return: object
    """
    # Convert the 'date_column' column to datetime if it's not already
    data_frame[date_column] = pd.to_datetime(data_frame[date_column])
    # Convert the 'date_column' column to just YYYY-mm-dd in-place
    data_frame[date_column] = data_frame[date_column].dt.date

    # How many rows & columns are there?
    print(f'There are {data_frame.shape[0]} records and {data_frame.shape[1]} columns in {e_data_file}')

    return data_frame


def add_year_column_from_date_column(data_frame, date_column: str):
    year = str(date_column) + "_year_only"
    # Convert 'date' column to datetime if it's not already
    data_frame[date_column] = pd.to_datetime(data_frame[date_column])
    # Extract the year and create a new column 'year'
    data_frame[year] = data_frame[date_column].dt.year
    return data_frame


def add_seconds_column_from_time_column(data_frame: pd.DataFrame, column: str ):
    """
    Convert Pandas datetime 'datetime64[ns]' to seconds 'int'
    Columns: "dispatch_time","enroute_time","arrive_time","time_in_service"
    :type data_frame: object
    :type column: pd.Int64Dtype
    """
    # Create 'time_in_seconds' column name
    time_in_seconds = str(column) + "_in_seconds"
    # Assume DataFrame time column is in hh:mm:ss format
    # Convert the 'time' column to timedelta
    data_frame[column] = pd.to_timedelta(data_frame[column])
    # Convert timedelta to seconds
    data_frame[time_in_seconds] = data_frame[column].dt.total_seconds().astype(int)
    # print(f"{data_frame}")
    # Convert the 'date_column' column to just hh:mm:ss format in-place
    data_frame[column] = data_frame[column].astype(str).str.replace('0 days ', '')
    return data_frame


def get_only_dates(data_frame):
    dates = data_frame['incident_date']
    for date in dates:
        date.split(' ')


def file_write(path: str, data: any, mode: str = 'w'):
    with open(path, mode) as f:
        f.write(data)
        f.close()


def file_read(path: str, mode='r') -> any:
    with open(path, mode) as f:
        output = f.read()
        f.close()
    return output


def rand_temp_file() -> str:
    """
    Creates tempfile with a random-enough alpha-num name of given length.
    FROM: https://github.com/talhasch/aparat/blob/main/aparat/io.py
    """
    length = 16
    tf = os.path.join(tempfile.gettempdir(), random_alphanum(length) + '.tmp')
    file_write(tf, '')
    return tf


def random_alphanum(length: int) -> str:
    """
    Creates a random-enough alphanumeric string of given length.
    FROM: https://github.com/talhasch/aparat/blob/main/aparat/io.py
    """
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars)) for x in range(length))


def remove_tmp_file(tmpfile: str):
    try:
        # os.remove(tmpfile)
        # Reference: https://pynative.com/python-delete-files-and-directories/
        # approach below assumes Python 3.8 or above
        pathlib.Path(tmpfile).unlink(missing_ok=True)
        _LOGGER.info("Deleted file {}".format(tmpfile))
    except Exception as e:
        # this exception handling is only for dev & debugging
        print(f'{e}')
        _LOGGER.warning("Problem deleting file {}: Exception message: {}".format(tmpfile, e))
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f"{report_start(dir_path)}")
    # Enforce a minimum Python version
    min_major_version = 3
    min_minor_version = 10
    minimum_py(min_major_version, min_minor_version)
    # Use a set: collection of unordered unique elements without duplicates {}
    emergency_data_list = []
    csv_data_filename_suffix: str = 'emerg_data_date_is_now_year_new_time_in_seconds_columns_optimized.csv'
    csv_data_filename: object = create_target_csv_data_file(csv_data_filename_suffix)
    # Get the source csv file and assign it to a dataframe called emergency_data
    # Enter the path to the raw data file here:
    ## e_data_file = Path("./data/rvfd-calls-for-service-Jan-2010.csv")
    e_data_file = Path("./2024-12-11_emerg_data_organized.csv")
    # Read the data into a Pandas dataframe
    if e_data_file.exists():
        emergency_data: DataFrame = pd.read_csv(e_data_file, sep=',')

    # Start removing code here


    # We need the .copy() below to stop Pandas from complaining with
    # "SettingWithCopyWarning" for the pd.to_datetime/timedelta in functions called below
    # See: https://stackoverflow.com/questions/71458707/pandas-settingwithcopywarning-for-pd-to-datetime

    # convert the data in a pandas dataframe datetime column from YYYY-mm-dd format
    # into just YYYY and append the new column to the dataframe
    temp_data_frame_w_dates: DataFrame = pd.DataFrame(
        add_year_column_from_date_column(emergency_data.copy(), "incident_date"))
   # convert the data in a pandas dataframe datetime column from YYYY-mm-dd hh:mm:ss format
    # into just YYYY-mm-dd and append the new column to the dataframe
    temp_data_frame_w_dates: DataFrame = pd.DataFrame(convert_date_column_to_year(temp_data_frame_w_dates.copy(), "incident_date"))
    # convert a datetime column in a Pandas DataFrame from the hh:mm:ss format
    # into just seconds and append the new column to the dataframe
    temp_data_frame_w_dates = pd.DataFrame(
        add_seconds_column_from_time_column(temp_data_frame_w_dates.copy(), "time_in_service"))
    temp_data_frame_w_dates = pd.DataFrame(
        add_seconds_column_from_time_column(temp_data_frame_w_dates.copy(), "dispatch_time"))
    temp_data_frame_w_dates = pd.DataFrame(
        add_seconds_column_from_time_column(temp_data_frame_w_dates.copy(), "enroute_time"))
    temp_data_frame_w_dates = pd.DataFrame(
        add_seconds_column_from_time_column(temp_data_frame_w_dates.copy(), "arrive_time"))

    """
    print(f'Overview of the temp_data_frame_w_dates DataFrame data:')
    print(f'{temp_data_frame_w_dates.info()}')
    print_separator_line()
    """

    counter = 0
    length = len(temp_data_frame_w_dates)
    while length > counter:
        # Now using date format for SQLite: YYYY-MM-DD
        # For a discussion about the reasons for using df.loc[] see:
        # https://stackoverflow.com/questions/48409128/what-is-the-difference-between-using-loc-and-using-just-square-brackets-to-filte/48411543#48411543

        csv_string: str = (f"\"{temp_data_frame_w_dates.loc[counter, 'incident_date']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'incident_date_year_only']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'response_unit']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'call_type'].strip()}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'dispatch_time']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'dispatch_time_in_seconds']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'enroute_time']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'enroute_time_in_seconds']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'arrive_time']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'arrive_time_in_seconds']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'time_in_service']}\","
                           f"\"{temp_data_frame_w_dates.loc[counter, 'time_in_service_in_seconds']}\"\n")
        emergency_data_list.append(csv_string)
        counter += 1

    # Header row for csv file:
    csv_header_string = f"\"incident_date\",\"incident_date_year_only\",\"response_unit\",\"call_type\",\"dispatch_time\",\"dispatch_time_in_seconds\",\"enroute_time\",\"enroute_time_in_seconds\",\"arrive_time\",\"arrive_time_in_seconds\",\"time_in_service\",\"time_in_service_in_seconds\"\n"
    # create a text file for writing
    outputfilelength = len(emergency_data_list)
    with open(csv_data_filename, "a+") as f:
        f.writelines(csv_header_string)
        f.writelines(emergency_data_list)

    print(f"{report_end(str(csv_data_filename))}")
