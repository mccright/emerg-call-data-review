import csv
import datetime
import os
import sys
from pathlib import Path
import statistics
import string

# from ts_plot_2 import response_time

start = datetime.datetime.now()
dir_path = os.getcwd()
allowed_characters = set(r'{0}{1}~ []><()$%-_/., * $'.format(string.ascii_letters, string.digits))
# set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
separator = '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'


def create_target_csv_data_file(csvfile_suffix: str) -> object:
    """Creates a path/file object with filename day-month-year
    Builds the filename with {date}_{csvfile_suffix}.
    Appends the filename to the current directory.
    :param csvfile_suffix: str
    :rtype: object
    """
    filename_suffix = csvfile_suffix
    filename_prefix = start.strftime('%Y-%m-%d')
    filename = f"{filename_prefix}_{filename_suffix}"
    # Put the new file in the current directory
    csv_file_name: str = os.path.join(dir_path, filename)
    return csv_file_name

def clean_the_list_for_statistics(numbers: list) -> list:
    # Check: is the numbers list empty
    if not numbers:
        print(f"Error: The numbers list is empty.")
        sys.exit(1)
    # We have data, so now filter out non-numeric values
    numeric_data = [x for x in numbers if isinstance(x, (int, float))]
    # Check: are there no numeric values
    if not numeric_data:
        print(f"Error: No numeric values in the numbers list.")
        sys.exit(1)
    return numeric_data

def calculate_mean_statistics(numbers: list) -> int:
    my_list = clean_the_list_for_statistics(numbers)
    try:
        mean_val = statistics.mean(my_list)
        # print(f"inside calculate_median_statistics() and median_val = {mean_val}")
    except statistics.StatisticsError as e:
        print(f"StatisticsError: {e}")
        sys.exit(1)
    except TypeError as e:
        print(f"TypeError: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"ValueError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Generic Exception in calculate_median_statistics(): {str(e)}")
        sys.exit(1)
    return mean_val


def calculate_median_statistics(numbers: list) -> int:
    my_list = clean_the_list_for_statistics(numbers)
    try:
        median_val = statistics.median(my_list)
        # print(f"inside calculate_median_statistics() and median_val = {median_val}")
    except statistics.StatisticsError as e:
        print(f"StatisticsError: {e}")
        sys.exit(1)
    except TypeError as e:
        print(f"TypeError: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"ValueError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Generic Exception in calculate_median_statistics(): {str(e)}")
        sys.exit(1)
    return median_val


def calculate_median_math(numbers: list) -> int:
    numbers.sort()  # Sort the list
    n = len(numbers)
    mid = n // 2

    if n % 2 == 0:  # If even number of elements
        return (numbers[mid - 1] + numbers[mid]) / 2
    else:  # If odd number of elements
        return numbers[mid]


def do_medians_for_ru_all_ct_sc(csv_raw_data: csv.DictReader) -> int:
    # Assume there is a header row, so move to the next row for data
    csv_raw_data.__next__()
    # For all response_units, all sub_categories
    # rows = list(csv_raw_data)
    # row_count = len(rows)
    row_count, rows = how_many_rows(csv_raw_data)
    print(f"row_count[] list includes {row_count} rows inside do_medians_for_ru_all_ct_sc()")
    median_list: list = list()
    index = 15  # index 15 == response_time_in_seconds
    for row in rows:
        # print(f"response_time_in_seconds is:")
        # print(row.get('response_time_in_seconds'))
        # The dictionary.get() method is safer than dictionary[key] because
        # it returns None if the key does not exist, instead of raising an error.
        # print(f"RT = {row.get('response_time_in_seconds').strip()}")
        median_list.append(int(row.get('response_time_in_seconds')))
        # print(f"response_time_in_seconds is {0}.".format(row['response_time_in_seconds']))
        # print(f"row includes: {row}")
        # break
        #if row[index]:
        #    median_list.append(row[index])
    #print(f"median_list is {len(median_list)} long.")
    ##median_int = calculate_median_statistics(median_list)
    ##print(f"row = {row}")
    median_int = calculate_median_statistics(median_list)
    # median_int = 7
    return median_int

def do_means_for_ru_all_ct_sc(csv_raw_data: csv.DictReader) -> int:
    # Assume there is a header row, so move to the next row for data
    csv_raw_data.__next__()
    # For all response_units, all sub_categories
    # rows = list(csv_raw_data)
    # row_count = len(rows)
    row_count, rows = how_many_rows(csv_raw_data)
    print(f"row_count[] list includes {row_count} rows inside do_means_for_ru_all_ct_sc()")
    mean_list: list = list()
    index = 15  # index 15 == response_time_in_seconds
    for row in rows:
        mean_list.append(int(row.get('response_time_in_seconds')))
    mean_int = calculate_mean_statistics(mean_list)
    # median_int = 7
    return mean_int


def do_medians_for_tis_all_ct_sc(csv_raw_data: csv.DictReader) -> int:
    # Assume there is a header row, so move to the next row for data
    csv_raw_data.__next__()
    # For each response_units, all sub_categories
    # rows: list = list(csv_raw_data)
    # row_count: int = len(rows)
    row_count, rows = how_many_rows(csv_raw_data)
    print(f"row_count[] list includes {row_count} rows inside do_medians_for_tis_all_ct_sc()")
    median_list: list = list()
    for row in rows:
        # The dictionary.get() method is safer than dictionary[key] because
        # it returns None if the key does not exist, instead of raising an error.
        #print(f"TiS = {row.get('time_in_service_in_seconds').strip()}")
        median_list.append(int(row.get('time_in_service_in_seconds')))
    median_int = calculate_median_statistics(median_list)
    return median_int


def do_means_for_tis_all_ct_sc(csv_raw_data: csv.DictReader) -> int:
    # Assume there is a header row, so move to the next row for data
    csv_raw_data.__next__()
    # For all response_units, all sub_categories
    #rows: list = list(csv_raw_data)
    #row_count: int = len(rows)
    row_count, rows = how_many_rows(csv_raw_data)
    print(f"row_count[] list includes {row_count} rows inside do_means_for_ru_all_ct_sc()")
    mean_list: list = list()
    index = 15  # index 15 == response_time_in_seconds
    for row in rows:
        mean_list.append(int(row.get('time_in_service_in_seconds')))
    mean_int = calculate_mean_statistics(mean_list)
    # median_int = 7
    return mean_int


def do_median_for_response_unit(csv_raw_data: csv.DictReader, column_name: str, response_unit: str) -> int:
    print(f".", end="")
    # Assume we want the median for the specified response unit, column name and
    # for all or their rows (the whole date range).
    col_name: str = f"\'{str(column_name).lower().strip()}\'"
    # print(f"col_name = {col_name}")
    # Assume there is a header row, so move to the next row for data
    csv_raw_data.__next__()
    # For each response_units, all sub_categories
    # rows: list = list(csv_raw_data)
    # row_count: int = len(rows)
    row_count, rows = how_many_rows(csv_raw_data)
    # print(f"row_count[] list includes {row_count} rows inside do_median_for_response_unit()")
    median_list: list = list()
    # print(f"Going into the for loop: ")  #, end="")
    for row in rows:
        ## print(f"{row.get('response_unit').lower().strip()}:", end="")
        response_unit_var: str = row.get('response_unit').lower().strip()
        ## print(f"{response_unit_var},", end="")
        try:
            # if row.get('response_unit').lower().strip() is not None and row.get('response_unit').lower().strip() == response_unit.lower().strip():
            if response_unit_var is not None and response_unit_var == response_unit.lower().strip():
                # The dictionary.get() method is safer than dictionary[key] because
                # it returns None if the key does not exist, instead of raising an error.
                # print(f"ru {response_unit_var}.{column_name} = {row.get(column_name)}")  # {row.get('time_in_service_in_seconds').strip()}")
                if f"{row.get('col_name')}" is not None:
                    append_var: int = int(row.get(column_name).strip())
                    median_list.append(append_var)
                    # print(f"added a value for {response_unit_var}: {row.get(column_name).strip()}")
        except Exception as e:
            print(f"ATTENTION! Exception inside do_median_for_response_unit(): {e}")
    # print(f"out of for loop")
    # print(f"median_list = {median_list}")
    median_int = calculate_median_statistics(median_list)
    return median_int


def how_many_rows(csv_data: csv.DictReader) -> tuple[int, list]:
    """
    Purpose: Convert the csv.DictReader to a list
    then count the items in the list
    input: csv.DictReader
    return: row_count: int, rows: list
    """
    rows: list = list(csv_data)
    row_count: int = len(rows)
    # print(f"row_count[] list includes {row_count} tis rows")
    return row_count, rows

def build_overall_means_dict(filename: Path) -> tuple[int, int]:
    # do_means_for_ru_all_ct_sc():
    try:
        with filename.open('r', newline='', encoding='utf-8') as csvfile:
            csv_ru_raw_data = csv.DictReader(csvfile)
            my_ru_mean: int = do_means_for_ru_all_ct_sc(csv_ru_raw_data)
            csv_ru_raw_data = csv.DictReader(csvfile)
            csvfile.seek(0)
            my_tis_mean: int = do_means_for_tis_all_ct_sc(csv_ru_raw_data)
    except FileNotFoundError:
        print("Error: File not found")
    except UnicodeDecodeError:
        print("UnicodeDecodeError: Try different encoding")
    except Exception as e:
        print(f"Error: {str(e)}")
        # REFERENCE:
        # ['response_unit', 'incident_year_range_start', 'incident_year_range_end', \
        # 'time_period_length', 'response_level', 'call_type', 'sub_category', \
        # 'determinant_description', \
        # 'median_dispatch_2_enroute_time', 'median_dispatch_2_enroute_time_in_seconds', \
        # 'median_response_time', 'median_response_time_in_seconds', \
        # 'median_time_in_service', 'median_time_in_service_in_seconds']

    return my_ru_mean, my_tis_mean


def build_overall_medians_dict(filename: Path) -> tuple[int, int]:
    try:
        with filename.open('r', newline='', encoding='utf-8') as csvfile:
            csv_ru_raw_data = csv.DictReader(csvfile)
            # print(f"row_count[] csv_ru_raw_data includes {how_many_rows(csv_ru_raw_data)} rows")
            # csvfile.seek(0)
            my_ru_median: int = do_medians_for_ru_all_ct_sc(csv_ru_raw_data)
            #print(f"row_count[] csv_tis_raw_data includes {how_many_rows(csv_tis_raw_data)} rows")
            #csv_tis_raw_data = csv.DictReader(csvfile)
            csv_ru_raw_data = csv.DictReader(csvfile)
            csvfile.seek(0)
            # print(f"row_count[] csv_tis_raw_data includes {how_many_rows(csv_ru_raw_data)} rows")
            csvfile.seek(0)
            my_tis_median: int = do_medians_for_tis_all_ct_sc(csv_ru_raw_data)
    except FileNotFoundError:
        print("Error: File not found")
    except UnicodeDecodeError:
        print("UnicodeDecodeError: Try different encoding")
    except Exception as e:
        print(f"Generic Exception Error inside build_overall_medians_dict(): {str(e)}")
        """ 
        #The following section is just for debugging
        #num_columns = len(csv_raw_data.fieldnames)  # Get the first row
        #rows = []
        #print(f"The number of columns in \"{filename}\" is: {num_columns}")
        #print(f"csv_raw_data type = {type(csv_raw_data)}")  # Confirm csv.DictReader type
        #print(f"{separator}")
        #print(f" input header fields/columns: {csv_raw_data.fieldnames}") # Show column names
        """
        #found_counter: int = 0  # Track the matches
        #missing_counter: int = 0  # Track those not found
        ##for row in csv_raw_data:
            # For each response_unit, all sub_categories
        # sub_category column value = 'all'
        ##for resp_unit in csv_raw_data['response_unit']:
            # do something
        # For each response_unit, all sub_categories, all years
        # sub_category column value = 'all'
        # sub_category column value = 'all'

        # For each response_unit, all sub_categories, each year


        # For each response_unit_sub_category

        # REFERENCE:
        # ['response_unit', 'incident_year_range_start', 'incident_year_range_end', \
        # 'time_period_length', 'response_level', 'call_type', 'sub_category', \
        # 'determinant_description', \
        # 'median_dispatch_2_enroute_time', 'median_dispatch_2_enroute_time_in_seconds', \
        # 'median_response_time', 'median_response_time_in_seconds', \
        # 'median_time_in_service', 'median_time_in_service_in_seconds']

    return my_ru_median, my_tis_median


def get_response_unit_list(csv_ru_raw_data) -> list:
    # Assume there is a header row, so move to the next row for data
    csv_ru_raw_data.__next__()
    # For all response_units, all sub_categories
    # rows = list(csv_ru_raw_data)
    # row_count = len(rows)
    row_count, rows = how_many_rows(csv_ru_raw_data)
    print(f"row_count[] list includes {row_count} rows inside get_response_unit_list()")
    response_unit_list: list = list()
    response_unit_list_w_dups: list = list()
    for row in rows:
        response_unit_list.append(str(row.get('response_unit')).lower().strip())
    # remove duplicates from a list:
    # convert the list to a set and then back to a list.
    # For example: no_dups_unsorted_list = list(set(no_dups_unsorted_list)).
    response_unit_list = list(set(response_unit_list))
    response_unit_list_count = len(response_unit_list)
    print(f"response_unit_list_count[] list includes {response_unit_list_count} rows after duplicate removal inside get_response_unit_list()")
    response_unit_list_sorted: list = sorted(response_unit_list)
    return response_unit_list_sorted


def build_response_unit_medians_dict(filename: Path) -> dict:
    response_unit_medians_dict: dict = {}
    response_unit_response_time_medians_dict: dict = {}
    try:
        with filename.open('r', newline='', encoding='utf-8') as csvfile:
            csv_ru_raw_data = csv.DictReader(csvfile)
            # print(f"row_count[] csv_ru_raw_data includes {how_many_rows(csv_ru_raw_data)} rows")
            # csvfile.seek(0)
            response_unit_list: list = []
            response_unit_list = get_response_unit_list(csv_ru_raw_data)
            # print(f"response_unit_list: {response_unit_list} inside build_response_unit_medians_dict()")
            csvfile.seek(0)
            column_to_get = 'response_time_in_seconds' #'response_unit'
            # response_unit_to_get = "WAVE1"
            for ru in response_unit_list:
                # print(f"response unit from response_unit_list = {ru}")
                # print(f"column_to_get = {column_to_get}")
                tmp_median: int = do_median_for_response_unit(csv_ru_raw_data, column_to_get, str(ru).lower().strip())
                # print(f"tmp_median = {tmp_median}")
                response_unit_response_time_medians_dict[ru] = tmp_median
                csvfile.seek(0)
            #my_ru_median: int = do_medians_ru_rt_all_time(csv_ru_raw_data)
    except FileNotFoundError:
        print("Error: File not found")
    except UnicodeDecodeError:
        print("UnicodeDecodeError: Try different encoding")
    except Exception as e:
        print(f"Generic Exception Error inside build_response_unit_medians_dict(): {str(e)}")

    return response_unit_response_time_medians_dict # response_unit_medians_dict


if __name__ == "__main__":
    # below specify the output file filename suffix
    csv_data_filename_suffix: str = 'emerg_data_medians_step_six.csv'
    csv_data_filename: object = create_target_csv_data_file(csv_data_filename_suffix)

    # below specify the latest data filename
    production_input_file = Path('./2025-08-02_emerg_data_organized_step_four.csv')
    production_output_file = Path(str(csv_data_filename))
    input_file = production_input_file
    output_file = production_output_file


    ru_median, tis_median = build_overall_medians_dict(input_file)
    ru_mean, tis_mean = build_overall_means_dict(input_file)
    print(f"{separator}")
    print(f"response_time median for all response_times: {ru_median}")
    print(f"response_time average/mean for all response_times: {ru_mean:.1f}\r\n")
    print(f"time_in_service median for all time_in_service_times: {tis_median}")
    print(f"time_in_service average/mean for all time_in_service_times: {tis_mean:.1f}")

    # Do calculations by response_unit / team.
    # Get a dict containing the median response_time for each response_unit.
    response_unit_medians: dict = build_response_unit_medians_dict(input_file)
    # print(f"\r\nresponse_unit_medians: {response_unit_medians}")
    print(f"\r\n")
    for k, v in response_unit_medians.items():
        print(f"{k} median is {v}")
    # Get a dict containing the mean response_time for each response_unit.
    ### response_unit_means: dict = build_response_unit_means_dict(input_file)

    # Get a dict containing the median time_in_service_time for each response_unit.

    # Get a dict containing the mean time_in_service_time for each response_unit.


    sys.exit()
    """
    # Write the processed data to a new CSV file for response_units
    fieldnames = ['response_unit', 'incident_year_range_start', 'incident_year_range_end', 'time_period_length', 'response_level', 'call_type', 'sub_category', 'determinant_description', 'median_dispatch_2_enroute_time', 'median_dispatch_2_enroute_time_in_seconds', 'median_response_time', 'median_response_time_in_seconds', 'median_time_in_service', 'median_time_in_service_in_seconds']
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_file_rows)
    
    --------------------------------------------
    
    input header fields/columns: ['incident_date', 'incident_date_year_only', 'incident_num', 'response_unit', 'response_level', 'call_type', 'sub_category', 'determinant_description', 'dispatch_time', 'dispatch_time_in_seconds', 'enroute_time', 'enroute_time_in_seconds', 'arrive_time', 'arrive_time_in_seconds', 'response_time', 'response_time_in_seconds', 'time_in_service', 'time_in_service_in_seconds']
    # Write the processed data to a new CSV file
    fieldnames = ['incident_date', 'incident_date_year_only', 'incident_num', 'response_unit', 'response_level', 'call_type', 'sub_category', 'determinant_description', 'dispatch_time', 'dispatch_time_in_seconds', 'enroute_time', 'enroute_time_in_seconds', 'arrive_time', 'arrive_time_in_seconds', 'response_time', 'response_time_in_seconds', 'time_in_service', 'time_in_service_in_seconds']
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_file_rows)
    
    """

