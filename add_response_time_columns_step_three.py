import pandas as pd
import types
import matplotlib.pyplot as plt
import datetime
import numpy

SECONDS_IN_A_DAY: int = (24 * 60 * 60)

# Python Program to Convert seconds
# into hours, minutes and seconds
# https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/
def seconds_to_time(secs):
    return str(datetime.timedelta(seconds=secs))


def calc_time_to_arrival(arrive_seconds: int, dispatch_seconds: int):
    if arrive_seconds > dispatch_seconds:
        inner_time_to_arrival: int = arrive_seconds - dispatch_seconds
    else:
        inner_time_to_arrival: int = (arrive_seconds + SECONDS_IN_A_DAY) - dispatch_seconds
    return inner_time_to_arrival

# Read CSV data into a DataFrame
# df = pd.read_csv('data/test_emerg_data2.csv')
# df = pd.read_csv('./2025-02-14_emerg_data_date_is_now_year_new_time_in_seconds_columns_optimized.csv')
# Small dataset:
# df = pd.read_csv('./timestamp_testing.csv')
# Full dataset:
df = pd.read_csv('./2025-02-14_emerg_data_date_is_now_year_new_time_in_seconds_columns_optimized.csv')
## df = pd.read_csv('./2024-12-11_emerg_data_organized.csv')
# Either Filter response units ending with '11' or '12'
filtered_df = df[df['response_unit'].str.endswith(('0', '1', '2'))]
# filtered_df = df[df['response_unit'].str.startswith(('M'))]
response_units: pd = filtered_df['response_unit'].unique()
#print(f"Length of the filtered_df = {len(['response_units'])}")
num_rows = response_units.shape[0]
print(f"{df.shape[0]} rows in the whole dataframe")
print(f"{response_units.shape[0]} rows in filtered response_units")
#print(f"{df.describe()}")
time_to_arrival_list = []
print(f"time_to_arrival_list is type: {type(time_to_arrival_list)}")

for index in df.index:
    time_to_arrival = calc_time_to_arrival(df['arrive_time_in_seconds'][index], df['dispatch_time_in_seconds'][index])
    time_to_arrival_list.append(time_to_arrival)
    # print(f"response_unit: {df['response_unit'][index]}, call_type: {df['call_type'][index]}, time_to_arrival: {time_to_arrival}")

    #print(f"{time_to_arrival_list}")
df = df.assign(response_time_in_seconds = time_to_arrival_list)
my_timedelta = pd.to_timedelta(df['response_time_in_seconds'], unit='s')
df = df.assign(response_time = my_timedelta)
# Convert the 'date_column' column to just hh:mm:ss format in-place
df['response_time'] = df['response_time'].astype(str).str.replace('0 days ', '')

print(f"-----------------------------------------")
#print(f"{my_timedelta}")
#print(f"{df['response_time_in_seconds'].describe()}")
#print(f"{df.describe()}")
df = df[['incident_date', 'incident_date_year_only', 'response_unit', 'call_type', 'dispatch_time', 'dispatch_time_in_seconds', 'enroute_time', 'enroute_time_in_seconds', 'arrive_time', 'arrive_time_in_seconds', 'response_time_in_seconds', 'response_time', 'time_in_service', 'time_in_service_in_seconds']]
print(f"-----------------------------------------")
#print(f"{df}")
df.to_csv('usable_output_file.csv', encoding='utf-8', index=False, header=True)
#df = df.assign(time_to_arrival = time_to_arrival_list)
"""
#for unit in response_units:
for index in filtered_df.index:
    time_to_arrival = calc_time_to_arrival(filtered_df['arrive_time_in_seconds'][index], filtered_df['dispatch_time_in_seconds'][index])
    #if filtered_df['arrive_time_in_seconds'][index] > filtered_df['dispatch_time_in_seconds'][index]:
    #    time_to_arrival: int = filtered_df['arrive_time_in_seconds'][index] - filtered_df['dispatch_time_in_seconds'][index]
    #else:
    #    time_to_arrival = (filtered_df['arrive_time_in_seconds'][index] + SECONDS_IN_A_DAY)  - filtered_df['dispatch_time_in_seconds'][index]

    # print(f"response_unit: {filtered_df['response_unit'][index]}, call_type: {filtered_df['call_type'][index]}, time_to_arrival: {seconds_to_time(int(time_to_arrival))}")
    #print(f"response_unit: {filtered_df['response_unit'][index]}, call_type: {filtered_df['call_type'][index]}, time_to_arrival: {time_to_arrival} seconds, or {seconds_to_time(int(time_to_arrival))}")
    ## print(f"response_unit: {filtered_df['response_unit'][index]}, call_type: {filtered_df['call_type'][index]}, time_to_arrival: {time_to_arrival}")
    # record_counter = df.describe #(df[unit]['event_dispatch_date_time'])

        # concatenat time to the date column value:
        # str_date_time = (f"str({df['incident_date']}) str({df['arrive_time']})")
        # concatenating the columns 
        filtered_df['event_arrive_date_time'] = filtered_df['incident_date'].map(str) + ' ' + filtered_df['arrive_time'].map(str) 
        # cast 'event_arrive_date_time' to type: datetime64[ns]
        filtered_df['event_arrive_date_time'] = pd.to_datetime(filtered_df['event_arrive_date_time'])
        print(f"\n\nresponse_unit: {filtered_df['response_unit']}, event_arrive_date_time: {filtered_df['event_arrive_date_time']}\n\n")
        #
        # concatenat time to the date column value:
        # str_date_time = (f"str({df['incident_date']}) str({df['arrive_time']})")
        # concatenating the columns 
        filtered_df['event_dispatch_date_time'] = filtered_df['incident_date'].map(str) + ' ' + filtered_df['dispatch_time'].map(str) 
        # cast 'event_dispatch_date_time' to type: datetime64[ns]
        filtered_df['event_dispatch_date_time'] = pd.to_datetime(filtered_df['event_dispatch_date_time'])
        
        #print(f"event_arrive_date_time type: {(df['event_arrive_date_time'].dtype)}")
        #print(f"event_dispatch_date_time type: {(df['event_dispatch_date_time'].dtype)}")
        if filtered_df['event_arrive_date_time'] >= filtered_df['event_dispatch_date_time']:
            print(f"response time: {(filtered_df['event_arrive_date_time'] - filtered_df['event_dispatch_date_time'])}")
        else:
            filtered_df['event_arrive_date_time'] = (filtered_df['event_arrive_date_time'] + pd.Timedelta(days=1))
            print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
            print(f"negative response time: {(filtered_df['event_arrive_date_time'] - filtered_df['event_dispatch_date_time'])}")
        print(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        """
"""
# Convert 'incident_date' to datetime format
df['incident_date'] = pd.to_datetime(df['incident_date'], format='%Y-%m-%d')

# Either Filter response units ending with '11' or '12'
# filtered_df = df[df['response_unit'].str.endswith(('11', '12'))]

# Or Filter response units starting with 'WAVE' or 'SE'
# filtered_df = df[df['response_unit'].str.startswith(('WAVE', 'SE'))]
filtered_df = df[df['response_unit'].str.startswith(('M6'))]

# Plot time series for each 'response_unit'
response_units = filtered_df['response_unit'].unique()

for unit in response_units:
    unit_data = filtered_df[filtered_df['response_unit'] == unit]
    # For troubleshooting:
    # print(f"unit_data: {unit_data}")
    ### unit_data['time_in_service'] = (pd.to_timedelta(unit_data['time_in_service']).dt.total_seconds() / (60)).astype(int)
    print(f"arrive_time: {pd.to_timedelta(unit_data['arrive_time']).dt.total_seconds()} and dispatch_time: {pd.to_timedelta(unit_data['dispatch_time']).dt.total_seconds()}")
    # Declare a list that is to be converted into a column
    # representing response_time in minutes.
    response_time = ((pd.to_timedelta(unit_data['arrive_time']).dt.total_seconds() - pd.to_timedelta(unit_data['dispatch_time']).dt.total_seconds() ) / (60)).astype(int)
    # Using 'response_time' as the column name
    # and equating it to the list
    unit_data['response_time'] = response_time
    # Testing
    # print(f"unit_data['response_time']: {unit_data['response_time']}")
    
    # print(f"unit_data: {unit_data}")
    #unit_data.plot(x='incident_date', y='time_in_service', kind="line")
    # 
    # Create a time series plot
    plt.figure(figsize=(11, 6))
    ### plt.plot(unit_data['incident_date'], pd.to_timedelta(unit_data['time_in_service']).dt.total_seconds() / (60 * 60),label=unit)
    plt.plot(unit_data['incident_date'], pd.to_timedelta(unit_data['response_time']).dt.total_seconds(),label=unit)
    # plt.scatter(unit_data['incident_date'], pd.to_timedelta(unit_data['time_in_service']).dt.total_seconds() / (60 * 60),
    #         label=unit)
    #plt.hist(unit_data['incident_date'], pd.to_timedelta(unit_data['time_in_service']).dt.total_seconds() / (60 * 60),
    #         label=unit)

    # provide both local time and UTC time to better support
    # distributed operations
    run_at  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    run_at_utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    # Customize the plot
    plt.title(f'Time Series Plot for {unit}.  Report run at {run_at}')
    plt.xlabel('Incident Date')
    plt.ylabel('Response Time (minutes)')
    plt.legend()
    plt.grid(True)

    # Show the plot or save it to a file
    # plt.show()
    # Alternatively, save the plot to a file if needed:
    ### plt.savefig(f'reports/{unit}_time_in_service_plot.png')
    plt.savefig(f'reports/{unit}_response_time_plot.png')
"""    