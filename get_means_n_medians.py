import csv
import sys
from datetime import datetime
from statistics import mean, median
from collections import defaultdict

"""
This script reads the output of step 4, 
groups that data by "response_unit by year and quarter" 
    and by "response_unit by year", and then 
calculates the mean and median for each response_unit and period.
I assume it will be used by scripts that will graph
    this data by response_unit over time
"""

line_separator = "- - - - - - - - - - - - - - - - - - -"

# 1. Read CSV into a list of dicts
def read_times(path):
    records = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "incident_date": datetime.strptime(row["incident_date"], "%Y-%m-%d"),  # adjust format if needed
                "response_unit": row["response_unit"],
                "response_time_in_seconds": float(row["response_time_in_seconds"]),
            })
    return records

# 2. Bucket data into 4‑month and 12‑month periods
def four_month_bucket(dt):
    # months: 1–4 -> 1, 5–8 -> 2, 9–12 -> 3
    return (dt.year, (dt.month - 1) // 4 + 1)

def twelve_month_bucket(dt):
    return dt.year   # or (dt.year, 1) if you prefer explicit periods

# 3. Aggregate mean and median times in seconds by response_unit and period
def aggregate_stats(records):
    by_response_unit_4m = defaultdict(list)
    by_response_unit_12m = defaultdict(list)

    for r in records:
        response_unit = r["response_unit"]
        response_time_in_seconds = r["response_time_in_seconds"]
        dt = r["incident_date"]

        key_4m = (response_unit, *four_month_bucket(dt))   # (response_unit, year, 4m_period_index)
        key_12m = (response_unit, twelve_month_bucket(dt)) # (response_unit, year)

        by_response_unit_4m[key_4m].append(response_time_in_seconds)
        by_response_unit_12m[key_12m].append(response_time_in_seconds)

    stats_4m = {}
    for key, times in by_response_unit_4m.items():
        # we are using seconds, round off fractions of seconds
        stats_4m[key] = {
            "mean": round(mean(times), 0),
            "median": round(median(times), 0),
        }

    stats_12m = {}
    for key, times in by_response_unit_12m.items():
        # we are using seconds, round off fractions of seconds
        stats_12m[key] = {
            "mean": round(mean(times), 0),
            "median": round(median(times), 0),
        }

    return stats_4m, stats_12m


# 4. Sort the data by response unit and then, for each, by year
def build_12m_stats(data):
    stats_12m = data
    csv_organized = []
    for (response_unit, year), s in sorted(stats_12m.items()):
        mean = s["mean"]
        median = s["median"]
        csv_organized.append(f"{response_unit}, {year}, {mean}, {median}")
    return csv_organized


# 5. Build and write a csv file for review or graphing
def write_to_csv(file_path, data: list):
    import csv

    with open(file_path, "w", newline="", encoding="utf-8") as file:  # Open file in write mode
        writer = csv.writer(file)
        writer.writerow(["response_unit", "year", "mean", "median"])
        for line in data:
            row = next(csv.reader([line], skipinitialspace=True))
            # Remove the empty field created by the trailing comma
            if row and row[-1] == "":
                row.pop()
            writer.writerow(row)  # Write rows of data

# Use those functions if running the script from the command line
if __name__ == "__main__":
    # This data file path will need to be updated for your use case
    datafilepath = "2025-08-02_emerg_data_organized_step_four.csv"
    response_time_quarterly_csv_file = "response_time_quarterly.csv"
    response_time_yearly_csv_file = "response_time_yearly.csv"
    records = read_times(datafilepath)
    stats_4m, stats_12m = aggregate_stats(records)
    data_for_12m_csv = build_12m_stats(stats_12m)

    #write_to_csv(response_time_quarterly_csv_file, stats_4m)
    write_to_csv(response_time_yearly_csv_file, data_for_12m_csv)

    sys.exit()

    print(f"\n{line_separator}")
    print("\n4‑month stats (response_unit, year, quarter):")
    # print(f"{response_unit}, {year}, {period}, mean={mean:.1f}, median={median:.1f}")

    print(f"\n\n{line_separator}")
    print("\n12‑month stats (response_unit, year):")
    # print(f"{response_unit}, {year}, mean={mean:.1f}, median={median:.1f}")
