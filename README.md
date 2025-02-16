# Review Raw Emergency Call Data  

## Input Data:  

The original data 19,521 rows that included columns having variable length lists of '*tag-value*' pairs (```response_unit=<time_of_day>,response_unit=<time_of_day>,etc...```) (*think Python dictionary*) and some fields without data or with ```NULL``` values.  It appeared that the *tag-value* pairs in some columns were intended to be tightly coupled to *tag-value* pairs in other columns -- but some weren't. These issues (*and others*) made analysis of the original data a material challenge, and led to the decision to reformat and *clean* the data so that any given row was associated with a given ```incident``` for a given ```response_unit``` that included ```call_type```, ```dispatch_time```, ```enroute_time```, ```arrive_time```, and ```time_in_service``` data to support more effective analysis.  

### The original data looked like:  
```terminal
fdid,incident_num,incident_date,Mutual_Aid_FDID,Mutual_Aid_State,Mutual_Aid_Incident_Num,response_level,call_type,Unit_Dispatch_Times,Unit_Enroute_Times,Unit_Arrive_Times,Unit_At_Patient_Times,Unit_Enroute_To_Hospital_Times,Unit_Arrive_At_Hospital_Times,Unit_Staging_Times,Unit_Fire_Out_Times,Unit_Clear_Times,Time_In_Service,disposition_remarks
15555,10000015,1/1/10 12:00 AM,NULL,NULL,NULL,MC,MEDLE,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,
15555,10000031,1/1/10 12:00 AM,NULL,NULL,NULL,MA,33C2,"WAVE1=06:51:33, WAVE12=06:51:33,M5=07:05:17","WAVE12=07:03:23, M5=07:07:01",WAVE12=07:06:23,NULL,WAVE12=07:24:27,WAVE12=07:48:33,NULL,NULL,"M5=07:10:13,WAVE1=07:11:43, WAVE12=08:18:21","M5=00:04:56, WAVE1=00:20:10, WAVE12=01:26:48",
15555,10000034,1/1/10 12:00 AM,NULL,NULL,NULL,MA,28C4,"WAVE1=07:56:42, GRE310=07:56:42, WAVE11=08:05:59","GRE310=08:01:56, WAVE1=08:03:42, WAVE11=08:06:00",WAVE11=08:08:21,NULL,WAVE11=08:19:14,WAVE11=08:40:02,NULL,NULL,"GRE310=08:03:38, WAVE1=08:08:24, WAVE11=09:05:46","GRE310=00:06:56, WAVE1=00:11:42, WAVE11=00:59:47",
15555,10000043,1/1/10 12:00 AM,NULL,NULL,NULL,PR,17A1,"PLEA1=09:51:58, PLEA2=09:51:58, MWM31=09:51:58","PLEA2=09:55:57, PLEA1=09:57:20, MWM31=10:04:41","PLEA1=09:59:24, MWM31=10:18:57",NULL,MWM31=10:35:33,NULL,NULL,NULL,"PLEA1=10:32:10, PLEA2=10:32:15, MWM31=12:00:31","MWM31=02:08:33, PLEA1=00:40:12, PLEA2=00:40:17",
15555,10000056,1/1/10 12:00 AM,NULL,NULL,NULL,OM,19D1,"SE1=15:48:32, SE11=15:48:32, SE12=15:53:36, SE12=15:58:26","SE1=15:48:53, SE11=15:52:28, SE12=15:53:39","SE1=15:53:29, SE12=15:58:29",NULL,SE12=16:08:03,SE12=16:12:37,NULL,NULL,"SE12=15:54:10, SE11=16:08:38, SE1=16:09:07, SE12=16:26:43","SE1=00:20:35, SE11=00:20:06, SE12=00:33:07",
15555,10000076,1/1/10 12:00 AM,NULL,NULL,NULL,0,C13F ,B1=20:22:57,NULL,NULL,NULL,NULL,NULL,NULL,NULL,B1=20:23:02,B1=00:00:05,
15555,10000088,1/2/10 12:00 AM,NULL,NULL,NULL,FE,FIREC,"CERE1=01:41:51, RAYM1=01:46:16, WAVE1=01:46:16, 8707=02:02:55","CERE1=01:45:11, RAYM1=01:50:42, WAVE1=01:50:45, 8707=02:02:59","CERE1=01:51:58, RAYM1=02:07:09, WAVE1=02:19:25, 8707=02:59:41",NULL,NULL,NULL,NULL,NULL,"WAVE1=02:53:34, RAYM1=03:38:52, CERE1=04:40:33, 8707=04:51:47","8707=02:48:52, CERE1=02:58:42, RAYM1=01:52:36, WAVE1=01:07:18",
15555,10000095,1/2/10 12:00 AM,NULL,NULL,NULL,0,C13F ,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,
15555,10000121,1/2/10 12:00 AM,NULL,NULL,NULL,FE,FIREB,SW1=16:33:09,SW1=16:34:21,SW1=16:49:30,NULL,NULL,NULL,NULL,NULL,SW1=17:00:07,SW1=00:26:58,
15555,10000126,1/2/10 12:00 AM,NULL,NULL,NULL,RA,RSALARM,"GRE1=18:12:34, GRE310=18:12:34, M5=18:12:34, SC5=18:12:34, WAVE1=18:14:17, WAVE12=18:19:33","M5=18:14:26, GRE1=18:14:46, WAVE1=18:17:43, GRE310=18:19:10, WAVE12=18:19:35",NULL,NULL,NULL,NULL,NULL,NULL,"GRE1=18:22:42, GRE310=18:22:42, M5=18:22:42, SC5=18:22:42, WAVE1=18:22:42, WAVE12=18:22:42","GRE1=00:10:08, GRE310=00:10:08, M5=00:10:08, SC5=00:10:08, WAVE1=00:08:25, WAVE12=00:03:09",

```
## Clean the Data For Analysis:  

* [main_step_one.py](main_step_one.py) is used to convert the original data from Lincoln County into a dataset rationalized for this exercise -- it output [2024-12-11_emerg_data_organized.csv](2024-12-11_emerg_data_organized.csv).  

When you run it, be patient. It is slow. To show you it is really doing work it will emit the number of record that it is processing from the original data file and then a short end-of-processing report like that below:  
```terminal
- - - - - - - - - - - - - - - - - - - - - - - -
C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\main.py
Report started at: 2025-02-13 22:01:30.764194 local, 2025-02-14 04:01:30.764194+00:00 UTC
Report ended at: 2025-02-13 22:50:03.953248 local, 2025-02-14 04:50:03.953248+00:00 UTC
Report took: 0:48:33.189054
Reporting processed 19520 input records and output 22829 records
Report Output Files: C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\2025-02-13_emerg_data_organized_step_one.csv
- - - - - - - - - - - - - - - - - - - - - - - -


Process finished with exit code 0
```

* [optimize_data_set_step_two.py](optimize_data_set_step_two.py) ingests the organized data from [main_step_one.py] above, and adds columns for the year of each record, and for each column that contains a ```time``` value, it converts the value into a ```seconds``` value to make it easier to do math and comparisons with the original *times*.  

It runs faster than the [main_step_one.py] and ends with a short end-of-processing report like that below:  
```terminal
- - - - - - - - - - - - - - - - - - - - - - - -
C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\optimize_data_set.py
Report started at: 2025-02-14 07:34:28.073455 local, 2025-02-14 13:34:28.073455+00:00 UTC
Report ended at: 2025-02-14 07:34:29.766743 local, 2025-02-14 13:34:29.766743+00:00 UTC
Report took: 0:00:01.693288
Reporting processed 22829 input records and output 22829 records
Report Output Files: C:\Files\dev\pycharm\emerg-call-data-timeseries-temp\2025-02-14_emerg_data_date_is_now_year_new_time_in_seconds_columns_optimized.csv
- - - - - - - - - - - - - - - - - - - - - - - -

Process finished with exit code 0
```

### The 'clean' data looks like this:  
```terminal
"incident_date","incident_date_year_only","response_unit","call_type","dispatch_time","dispatch_time_in_seconds","enroute_time","enroute_time_in_seconds","arrive_time","arrive_time_in_seconds","time_in_service","time_in_service_in_seconds"
"2010-01-01","2010","WAVE12","33C2","06:51:33","24693","07:03:23","25403","07:06:23","25583","01:26:48","5208"
"2010-01-01","2010","WAVE11","28C4","08:05:59","29159","08:06:00","29160","08:08:21","29301","00:59:47","3587"
"2010-01-01","2010","MWM31","17A1","09:51:58","35518","10:04:41","36281","10:18:57","37137","02:08:33","7713"
"2010-01-01","2010","PLEA1","17A1","09:51:58","35518","09:57:20","35840","09:59:24","35964","00:40:12","2412"
"2010-01-01","2010","SE1","19D1","15:48:32","56912","15:48:53","56933","15:53:29","57209","00:20:35","1235"
"2010-01-01","2010","SE12","19D1","15:58:26","57506","15:53:39","57219","15:58:29","57509","00:33:07","1987"
"2010-01-02","2010","8707","FIREC","02:02:55","7375","02:02:59","7379","02:59:41","10781","02:48:52","10132"
"2010-01-02","2010","CERE1","FIREC","01:41:51","6111","01:45:11","6311","01:51:58","6718","02:58:42","10722"
"2010-01-02","2010","RAYM1","FIREC","01:46:16","6376","01:50:42","6642","02:07:09","7629","01:52:36","6756"
"2010-01-02","2010","WAVE1","FIREC","01:46:16","6376","01:50:45","6645","02:19:25","8365","01:07:18","4038"

```


* [csv-to-sqlite_using-sqlite3.py](csv-to-sqlite_using-sqlite3.py) is used to create [2025-02-13_emerg_data_organized_via_sqlite3.db].  






First pass at the Lancaster County Emergency Response (LCER) raw data from AM.  

## Initial Mission:  

### How often are Lincoln Fire and Rescue (LFR) ambulances responding to calls in the County?  
```terminal
	It would very useful to know what percentage of total annual \
	calls outside of city limits are responded to by LFR units.  
	Is this changing over time?  
	Does the percentage drop when a rural agency starts an ambulance service? etc  
	LFR Ambulances are noted by "M," signifying "Medic" followed by a number.  
	These include:  
		M1, M2, M3, M5, M6, M7, M8, M10, M21, M24, M25
		There may be other M-units listed in the data, but my sense is that those are typos or are very rarely called and will not affect the general sense of the data.
```

### What is the median response time on major calls for County ambulances each year?  
```terminal
	Response time is defined as "Unit_arrive_times" minus "Unit_dispatch_time".  
	All units from the same department are considered to have the same dispatch time.
	I'm interested in all County units with the suffix 10, 11 or 12, \
	which denotes an ambulance.
	County Departments are:
		WAVE, SW, SE, HICK, MALC, RAYM, BENN, HALL, PLEA, FIRT
	"Major Calls" are "call_type":
		 That include "Sub Category" C (Charlie), D (Delta), or E (Echo) \
		 as defined by the file "110520 Master Run Sheet.xlsx"
		call_type:
			FIREC, GRASFIRE, RSALARM, ECHO, CARFIRE, MEDC, MEDD, MEDE
```
Reminder: in a Pandas environment get basic statistics about the dataframe with ```df.describe() ``` and get mean of a specific column with ```df["columnname"].mean()```  


### What is the median response time on major fire, grass fire, and car fire calls each year?  
```terminal
	Response time is defined as "Unit_arrive_times" minus "Unit_dispatch_time".  
	All units from the same department are considered to have the same dispatch time.  
	Call types FIREC, GRASFIRE and CARFIRE (i.e., fire, grass fire, and car fire) \
	will not typically draw an ambulance response so there will be no arrival \
	data for unit XX10,11,12.  
	For these fire calls we want arrival time for the first APPARATUS, not person. \
	Often, XX1 will be first on scene to determine the nature of emergency and \
	communicate with incoming personnel, but we want to know when the first truck \
	arrives.  
	This could be XX30s (pumper), XX40s (tanker), XX20s (grass rig), or possibly XX60s.  
		call_type:
			FIREC, GRASFIRE, CARFIRE

```



This is a subset of the call data. There are 19,520 records. Records include dates from Jan. 2010 through Dec. 2020. 
Assume that all records are anonymous. 

## Pandas data_frame.info() Summary of This Raw Data Without Processing 
```terminal
RangeIndex: 19520 entries, 0 to 19519
Data columns (total 19 columns):
 #   Column Non-Null Count  Dtype  
---  ------ --------------  -----  
 0   fdid   19520 non-null  int64  
 1   incident_num19520 non-null  int64  
 2   incident_date    19520 non-null  object 
 3   Mutual_Aid_FDID  0 non-null float64
 4   Mutual_Aid_State 0 non-null float64
 5   Mutual_Aid_Incident_Num    0 non-null float64
 6   response_level   19520 non-null  object 
 7   call_type   19520 non-null  object 
 8   Unit_Dispatch_Times   18335 non-null  object 
 9   Unit_Enroute_Times    16524 non-null  object 
 10  Unit_Arrive_Times15464 non-null  object 
 11  Unit_At_Patient_Times 4341 non-null   object 
 12  Unit_Enroute_To_Hospital_Times  8114 non-null   object 
 13  Unit_Arrive_At_Hospital_Times   7394 non-null   object 
 14  Unit_Staging_Times    0 non-null float64
 15  Unit_Fire_Out_Times   49 non-nullobject 
 16  Unit_Clear_Times 18277 non-null  object 
 17  Time_In_Service  18379 non-null  object 
 18  disposition_remarks   8356 non-null   object 
dtypes: float64(4), int64(2), object(13)
```

Ideas for chewing through this data:  
* Convert the 'incident_date' strings into datetime objects (*or Pandas date objects*)  
* Decompose the key value pairs in the 'Unit_Dispatch_Times', 'Unit_Enroute_Times', 'Unit_Arrive_Times', 'Unit_Enroute_To_Hospital_Times', 'Unit_Arrive_At_Hospital_Times' and 'Unit_Clear_Times' into Python dictionaries.  
* In each dictionary, convert the time string into a datetime object (*or Pandas date objects*).  
* For each row, find each *related* pair/series in the 'Unit_Dispatch_Times', 'Unit_Enroute_Times', 'Unit_Arrive_Times', 'Unit_Enroute_To_Hospital_Times', 'Unit_Arrive_At_Hospital_Times' and 'Unit_Clear_Times'.  
* For each call duration 'pair' print time series graph of given 'response_level', 'call_type' and 'Time_In_Service' column data, along with calculated *Response_Time* values.  
  * Response_Time = ('Unit_Arrive_Times' minus 'Unit_Dispatch_Times')  

Because the "Unit" is a key identifier, we need to create a Python list of Unit Names.  Then as we iterate through data about each "Unit" we check if that Unit is already in our 'Unit_List" and if not, append it to that list.

## Data Column Descriptions  
| Name|Python Data Type|Desired Data Type|Description|Notes|
|:-----:|:-----:|:-----:|:-----:|:-----:|
| fdid | int64 | int | | |
| incident_num | int64 | int | | |
| incident_date | object | datetime | Time is either "12:00 AM" or "0:00" -- it does not represent the actual time of the call. |
| Mutual_Aid_FDID | float64 | NULL | | Ignore/remove this column |
| Mutual_Aid_State | float64 | NULL | | Ignore/remove this column |
| Mutual_Aid_Incident_Num | float64 | NULL | | Ignore/remove this column |
| response_level | object | str | 1 empty, 198 unique 1 or 2-char strings; see the full list below | Field is right-padded with spaces to a length of 11 char. |
| call_type | object | str | Medical Priority Dispatch System (MPDS) Codes. Example at http://www.rcfireassoc.org/emd.pdf | Data contains 600 unique strings. Remove records containing "TEST". |
| Unit_Dispatch_Times | object | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_Enroute_Times | object | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_Arrive_Times | object |  str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_At_Patient_Times | object | NULL |  | Ignore/remove this column |
| Unit_Enroute_To_Hospital_Times | object | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_Arrive_At_Hospital_Times | object | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_Staging_Times | float64 | NULL |  | Ignore/remove this column |
| Unit_Fire_Out_Times | object | NULL |  | Ignore/remove this column |
| Unit_Clear_Times | object | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Time_In_Service | object | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| disposition_remarks | object |  |  | Remove records containing any of the following in this column: "STORED COMPLAINT DUP:" "(FILE ONLY COMPLAINT)" "TEST" |

### How many times are given Units being contacted for service?  

The data file "2023-02-28_emerg_data_organized.csv" contains 43,915 records and one header row:  
```terminal
matt@hostname:/mnt/d/test/emerg-call-data-review$ wc -l < 2023-02-28_emerg_data_organized.csv
43916
matt@hostname:/mnt/d/test/emerg-call-data-review$
```

Each row includes "date","response_unit","dispatch_time","time_in_service" columns.  
The data includes 207 unique Unit names.  The following commands count how many times each Unit was called upon during the 10 year period that the data describes.  The output is displayed in decending order by the number of times each Unit was called upon for service.  
```terminal
matt@hostname:/mnt/d/test/emerg-call-data-review$ cat 2023-02-28_emerg_data_organized.csv | cut -d "," -f 2 | sort | uniq -c | sort -rid
   3312 "WAVE1"
   2793 "M6"
   2767 "WAVE12"
   2444 "SW1"
   2247 "HICK1"
   1802 "RAYM1"
   1736 "SW11"
   1696 "SE1"
   1615 "MALC1"
   1510 "M5"
   1509 "BENN1"
   1300 "RAYM10"
   1194 "FIRT1"
   1060 "EMS1"
   1048 "SC5"
    955 "M3"
    937 "SE11"
    922 "M8"
    869 "MALC10"
    859 "SE12"
    798 "SW12"
    686 "M7"
    606 "HALL11"
    603 "RAYM11"
    585 "M2"
    534 "HALL1"
    504 "PLEA1"
    415 "WAVE11"
    391 "EAGL1"
    355 "PLEA2"
    344 "TAC3"
    291 "B1"
    261 "CORT1"
    253 "ALVO10"
    247 "TAC4"
    242 "GRE310"
    230 "EAGL10"
    228 "VALP1"
    198 "CERE1"
    187 "VALP10"
    184 "MWM31"
    152 "TAC5"
    148 "GRE1"
    147 "HICK11"
    147 "CERE10"
    113 "EAGL11"
    101 "ALVO1"
    100 "WAVE2"
91 "CRET1"
90 "M10"
85 "HALL2"
75 "SW2"
70 "CLAT1"
69 "TAC6"
64 "HICK2"
61 "MALC2"
58 "M25"
53 "MRED"
53 "CERE11"
52 "RAYM2"
46 "E5"
46 "CRET10"
46 "8705"
40 "E13"
40 "E11"
39 "T5"
39 "CERE12"
37 "T8"
37 "SE2"
37 "AIRG1"
34 "BENN2"
33 "VALP11"
33 "FIRT2"
32 "TAC7"
32 "M1"
30 "E12"
29 "MILF10"
29 "B2"
27 "E6"
27 "E14"
26 "CORT11"
25 "8707"
24 "WR1"
24 "T1"
24 "M214"
23 "M24"
23 "IDG"
22 "M211"
22 "E3"
20 "T7"
19 "TAC8"
18 "E4"
15 "SINSP"
15 "LIFE12"
14 "MWM32"
14 "EMS3"
14 "E8"
13 "PLEA3"
13 "IKH"
13 "DOUG10"
13 "ASHL1"
13 "ADAM10"
11 "SW3"
11 "HEALTH"
11 "ALVO11"
11 "8734"
10 "WAVE3"
10 "REDCRS"
10 "RAYMWR"
10 "E10"
 9 "MWM34"
 9 "IRC"
 9 "ICS"
 9 "E9"
 8 "E7"
 8 "E2"
 8 "E1"
 7 "VALP2"
 7 "HICK3"
 6 "SE3"
 6 "RC1"
 6 "MALC3"
 6 "M21"
 6 "INSPPM"
 6 "IDR"
 6 "CLAT10"
 5 "MWM33"
 5 "HALL3"
 5 "E971"
 5 "BR10"
 4 "ITC"
 4 "H14"
 4 "CERE2"
 3 "TAC9"
 3 "T971"
 3 "SW5"
 3 "RAYM3"
 3 "MWM35"
 3 "MILF1"
 3 "M971"
 3 "M210"
 3 "GARL1"
 3 "EAGL2"
 3 "DOUG1"
 3 "BENN3"
 3 "B971"
 3 "AIRG3"
 3 "AIRG2"
 3 "A14"
 2 "TAC12"
 2 "PALM1"
 2 "LIFE13"
 2 "IBM"
 2 "GRE3"
 2 "FIRT3"
 2 "E972"
 2 "E15"
 2 "CORT2"
 2 "ADAM1"
 2 "8712"
 1 "VALP3"
 1 "UPDF3"
 1 "TAC972"
 1 "T972"
 1 "T12"
 1 "STER1"
 1 "SE5"
 1 "S11"
 1 "S1"
 1 "RED97"
 1 "MWM2"
 1 "M212"
 1 "LT2"
 1 "LFRPOC"
 1 "ITS"
 1 "IRF"
 1 "INSP97"
 1 "INSP"
 1 "IMW"
 1 "IDC"
 1 "HELO1"
 1 "GRE2"
 1 "F3"
 1 "F2"
 1 "EMS2"
 1 "E973"
 1 "E16"
 1 "CRET12"
 1 "CRET11"
 1 "CORT3"
 1 "CLB"
 1 "CLAT2"
 1 "CHAP97"
 1 "CHAP"
 1 "CERE4"
 1 "CERE3"
 1 "BR1"
 1 "BK1"
 1 "B1B"
 1 "ALVO2"
 1 "AIRG4"
 1 "AIR97"
 1 "AGAIR3"
 1 "AGAIR2"
 1 "AGAIR1"
 1 "8714"
 1 "8701"
matt@hostname:/mnt/d/test/emerg-call-data-review$ cat 2023-02-28_emerg_data_organized.csv | cut -d "," -f 2 | sort | uniq -c | sort -r | wc -l
208
matt@hostname:/mnt/d/test/emerg-call-data-review$
```

### What types of calls are associated with requests to these Units?  
If we extract, for example, all the 3312 records associated with response_unit "WAVE1" then count how many times each call_type is associated with a call to "WAVE1."  The following commands count how many times each call_type was associated with "WAVE1" calls during the 10 year period that the data describes.  The output is displayed in decending order by the number of times each call_type appeared in a WAVE1 record.  
```terminal
matt@hostname:/mnt/d/test/emerg-call-data-review$ cat 2023-02-28_emerg_data_organized.csv | cut -d "," -f 1-5 | grep WAVE1 | grep -v WAVE1[1234567890] | cut -d "," -f 3 | sort | uniq -c | sort -nr
    217 "FIREA"
    145 "GRASFIRE"
    136 "MEDLE"
    130 "CARFIRE"
    113 "STILL"
92 "29D2P"
77 "29B1"
74 "RSALARM"
73 "6D2"
72 "LIFTASST"
64 "FIREC"
60 "32D1"
49 "MUTAID"
43 "SPECDUTY"
43 "6D1"
42 "MEDOA"
41 "ODOR"
41 "17B1"
40 "17B1G"
39 "29B4"
38 "32B2"
37 "13C1"
36 "31D3"
35 "31D2"
34 "26C2"
31 "26A1"
31 "10D2"
30 "HAZ2"
29 "FIREB"
28 "32B3"
26 "26D1"
26 "12D2"
25 "32B1"
24 "6C1"
23 "17A1"
22 "HAZ3"
22 "ECHO"
21 "31A1"
21 "26C1"
21 "10D4"
19 "WIRES"
19 "29D5"
18 "CODET"
18 "9E1"
18 "29D2L"
18 "29B5"
18 "26A5"
18 "26A3"
17 "30B1"
17 "17A2G"
16 "31C1"
16 "30A1"
16 "1A1"
16 "10C1"
15 "MEDFD"
15 "17A1G"
14 "33C2T"
14 "30A2"
13 "33C2"
13 "33C1"
13 "17D3"
12 "STANDBY"
12 "ACCLE"
12 "5A1"
12 "33C1T"
12 "17B3G"
11 "6D4"
11 "31C2"
11 "26A10"
11 "17A2"
11 "10C4"
10 "10D1"
10 "10C2"
 9 "33C6"
 9 "26A11"
 9 "1C3"
 9 "17D4G"
 9 "12B1"
 8 "29A2"
 8 "26B1"
 8 "26A6"
 8 "1C6"
 8 "19D4"
 8 "13D1"
 8 "12D4"
 7 "31D1"
 7 "29D2M"
 7 "21B1M"
 7 "17B3"
 7 "12C4"
 7 "12A2"
 6 "6D2E"
 6 "33C6T"
 6 "29D4"
 6 "21D3"
 6 "21B2"
 6 "21B1"
 6 "19C4"
 5 "NOEMD"
 5 "DUMPFIRE"
 5 "9E2"
 5 "9B1"
 5 "6D2O"
 5 "33C4"
 5 "29B5U"
 5 "28C1L"
 5 "28C1"
 5 "23C7"
 5 "23C1"
 5 "19D1"
 5 "17D4"
 5 "17D3G"
 5 "17A3"
 5 "13C2"
 5 "13A1"
 5 "12A1E"
 4 "6E1"
 4 "6D1O"
 4 "33C5T"
 4 "33C4T"
 4 "31A3"
 4 "2D1"
 4 "29D2"
 4 "29B1A"
 4 "29A1"
 4 "26A4"
 4 "21A1"
 4 "19D2"
 4 "19C2"
 4 "17D2"
 4 "13C3"
 4 "12A1"
 4 "11D1"
 4 "10C3"
 3 "MEDSD"
 3 "ELEVATOR"
 3 "6D1E"
 3 "6C1O"
 3 "5A2"
 3 "4B1A"
 3 "33C5"
 3 "33C3T"
 3 "30D3"
 3 "29D4M"
 3 "29D4A"
 3 "29D3"
 3 "29D2Q"
 3 "29D2K"
 3 "29B4U"
 3 "29B3"
 3 "28C4"
 3 "26A7"
 3 "26A2"
 3 "25A1"
 3 "23D1"
 3 "23C1I"
 3 "23B1I"
 3 "23B1"
 3 "21D5M"
 3 "21D4M"
 3 "21D3M"
 3 "21D2"
 3 "21B2M"
 3 "20B1H"
 3 "20A1H"
 3 "1C5"
 3 "18C4"
 3 "17D5"
 3 "12D2E"
 3 "10D3"
 2 "SUSPART"
 2 "C13F"
 2 "ALS"
 2 "9E3"
 2 "9D1"
 2 "9B1A"
 2 "6D3"
 2 "6C1E"
 2 "6C1A"
 2 "5D1"
 2 "33D1"
 2 "33C3"
 2 "33A1"
 2 "2D2"
 2 "2C1I"
 2 "2B1"
 2 "2A1"
 2 "29O1"
 2 "29D9"
 2 "29D7"
 2 "29D6"
 2 "29D2N"
 2 "29D1F"
 2 "29D1D"
 2 "29B5V"
 2 "29B4X"
 2 "29B4M"
 2 "29B1V"
 2 "29B1M"
 2 "29A2V"
 2 "28C5L"
 2 "28C5G"
 2 "28C4L"
 2 "28C4E"
 2 "28C2J"
 2 "28C1X"
 2 "28C1J"
 2 "26A8"
 2 "25D1"
 2 "25B2B"
 2 "23O1A"
 2 "23D2"
 2 "23D1I"
 2 "23C7I"
 2 "21D4"
 2 "21B2T"
 2 "1C1"
 2 "19C3"
 2 "17B2"
 2 "17A4G"
 2 "17A3G"
 2 "12C2E"
 2 "12B1E"
 2 "11D1U"
 2 "10D5"
 1 "SERVCALL"
 1 "HAZPKG"
 1 "GASLEAK"
 1 "ARSON"
 1 "9E6"
 1 "9B1E"
 1 "8O1"
 1 "8D5S"
 1 "8D3U"
 1 "8D3T"
 1 "7C3E"
 1 "7A3E"
 1 "6D4E"
 1 "6D2A"
 1 "5C3"
 1 "4D2A"
 1 "4B3A"
 1 "4B1"
 1 "33D1T"
 1 "33C1P"
 1 "31D4"
 1 "31C3"
 1 "30D2"
 1 "30D1"
 1 "30B2"
 1 "2D2I"
 1 "2C1M"
 1 "2C1"
 1 "29O1V"
 1 "29D8"
 1 "29D3M"
 1 "29D3A"
 1 "29D1B"
 1 "29B5Y"
 1 "29B5X"
 1 "29B4A"
 1 "29B2"
 1 "28C9U"
 1 "28C8J"
 1 "28C7"
 1 "28C6Y"
 1 "28C5Z"
 1 "28C5C"
 1 "28C5"
 1 "28C4X"
 1 "28C4J"
 1 "28C4C"
 1 "28C3X"
 1 "28C3L"
 1 "28C3F"
 1 "28C2L"
 1 "28C2K"
 1 "28C2"
 1 "28C1G"
 1 "28C1F"
 1 "28C1C"
 1 "28C11X"
 1 "28C11G"
 1 "28C11E"
 1 "27D4S"
 1 "27B1S"
 1 "26O7"
 1 "26A21"
 1 "25D2W"
 1 "25D2"
 1 "25D1V"
 1 "25B6W"
 1 "25B6V"
 1 "25B6"
 1 "25B3V"
 1 "25B2V"
 1 "25A1V"
 1 "24D3"
 1 "24D2"
 1 "24C2"
 1 "23C7V"
 1 "23C7A"
 1 "23C3I"
 1 "23C2V"
 1 "23C2I"
 1 "23C2A"
 1 "23C1V"
 1 "22B2"
 1 "22A1B"
 1 "21D5T"
 1 "21D3T"
 1 "21B4T"
 1 "21B4"
 1 "21B1T"
 1 "21A2"
 1 "20D2H"
 1 "1C4"
 1 "1C2"
 1 "19C7"
 1 "18C2"
 1 "18A1"
 1 "17D6"
 1 "17D1"
 1 "17B3P"
 1 "17B1E"
 1 "15C1"
 1 "14D5I"
 1 "14D1"
 1 "13C1C"
 1 "12D4E"
 1 "12D1E"
 1 "12D1"
 1 "12C5"
 1 "12C3"
 1 "12C1E"
 1 "12A3"
 1 "11D2U"
 1 "11D2"
 1 "11D1O"
 1 "11D1M"
 1 "11D1F"
 1 "11A1U"
 1 "11A1F"
 1 "11A1"
 1 "10A1"
matt@hostname:/mnt/d/test/emerg-call-data-review$
```

### Some Column Data Summarized  

#### call_type  
There are 600 unique "call_type" strings in the universe of 19,520 multi-unit records.  
9 unique strings appear 400 or more times.  
13 unique strings appear 300 or more times.  
20 unique strings appear 200 or more times.  
51 unique strings appear 100 or more times.  
126 unique strings appear 20 or more times.  
188 unique strings appear 10 or more times.  
273 unique strings appear 5 or more times.  
326 unique strings appear 4 or less times.  
299 unique strings appear 3 or less times.  
257 unique strings appear 2 or less times.  
180 unique strings appear 1 time.  

#### The top 12 "call_type" strings and their frequency (raw data)  
| Occurances | string |
|:------:|:------:|
| 390 | 29B1 |
| 402 | RSALARM |
| 443 | C13F |
| 456 | FIREC |
| 475 | STANDBY |
| 525 | 29D2P |
| 530 | CARFIRE |
| 701 | MEDLE |
| 856 | STILL |
| 960 | ALS |
| 972 | FIREA |
| 1411| GRASFIRE |

#### The top 12 "call_type" strings and their frequency (processed data)  
```terminal
matt@hostname:/mnt/d/test/emerg-call-data-review$ cat 2023-02-28_emerg_data_organized.csv | cut -d "," -f 3 | sort | uniq -c | sort -id | tail -12
```
| Occurances | string |
|:----------:|:------:|
|  755 | 32D1 |
|  834 | CARFIRE |
|  947 | 6D2 |
| 1063 | STILL |
| 1069 | 29B1 |
| 1157 | FIREC |
| 1230 | FIREA |
| 1505 | ALS |
| 1670 | RSALARM |
| 1740 | MEDLE |
| 2028 | GRASFIRE |
| 2075 | 29D2P |

#### Incident Dates Distribution:  
```terminal
Name: incident_date, dtype: object
count   43915
mean2015-09-04 00:00:00
min 2010-01-01 00:00:00
10% 2011-03-27 00:00:00
20% 2012-05-17 00:00:00
40% 2014-08-01 00:00:00
50% 2015-09-26 00:00:00
60% 2016-11-04 00:00:00
80% 2018-12-21 00:00:00
90% 2020-01-28 00:00:00
max 2020-12-31 00:00:00
```

#### Dispatch Times Distribution:  
```terminal
Name: dispatch_time, dtype: object
count   43915
mean 13:40:38
min  00:00:06
10%  05:17:07
20%  08:17:01
40%  12:27:31
50%  14:24:09
60%  15:59:25
80%  19:12:32
90%  21:11:46
max  23:59:59
```

#### Time in Service Distribution:  
```terminal
Name: time_in_service, dtype: object
count   43915
mean 00:47:13
min  00:00:00
10%  00:05:36
20%  00:12:27
40%  00:27:47
50%  00:35:33
60%  00:46:04
80%  01:11:46
90%  01:31:17
max  19:19:00
```

#### response_level (raw)  
0  
4  
8  
9  
10  
12  
14  
15  
16  
19  
20  
21  
25  
32  
34  
35  
36  
37  
50  
51  
53  
61  
65  
    
??  
AA  
AC  
AL  
AM  
AR  
BC  
BD  
BE  
BF  
BJ  
BL  
BP  
CB  
DB  
DC  
E1  
E2  
E3  
E7  
E8  
EA  
EB  
EC  
ED  
EE  
EF  
EG  
FE  
FF  
FK  
FT  
FU  
FV  
GG  
H1  
H2  
H3  
H5  
H6  
H7  
HA  
KB  
LM  
M2  
MA  
MB  
MC  
MF  
MN  
MO  
MP  
MQ  
MR  
MS  
MT  
MX  
NL  
NM  
OM  
OP  
PA  
PB  
PC  
PD  
PE  
PF  
PG  
PH  
PI  
PJ  
PK  
PR  
RA  
RB  
RC  
RD  
RE  
RG  
RK  
S1  
S2  
S3  
WF  
ZO  
ZR  


## Additional References  
### Response Code Priorities  
Alpha Response=Code 1--Low Priority  
Bravo Response=Code 2--Mid Priority (calls that may involve First Responders)  
Charlie Response=Code 3--Possibly Life Threatening  
Delta Response=Code 3--Life Threatening  
Echo Response=Code 3--Full Arrest or Imminent Death  
Omega Response=Code 1--Lowest Priority  

### MPDS Codes  
http://www.rcfireassoc.org/emd.pdf (18 pages)  
https://www.parliament.vic.gov.au/images/stories/committees/paec/2016-17_Performance_Outcomes/qons/8_Att_4._Dispatch_Grid_as_at_January_2015_Pre_Dispatch_Grid_Review.pdf (33 pages)  


### ToDo:  
* Figure out whether it would help debugging to use [pymg](https://github.com/mimseyedi/pymg), a CLI tool that can interpret Python files by the Python interpreter and display the error message in a more readable way if an exception occurs [https://github.com/mimseyedi/pymg](https://github.com/mimseyedi/pymg)  
* Experiment with the code at: https://github.com/DataForScience/Timeseries using the notes that I took in the "Times Series Analysis for Everyone: Introduction" class and the content at: https://data4sci.com/timeseries.  
* Try writing the scripting so that it can be hosted using Pynecone - "performant, customizable web apps in pure Python."  https://github.com/pynecone-io/pynecone  
>Pynecone is a full-stack Python framework that makes it easy to build and deploy web apps in minutes. All the information for getting started can be found in this README. However, a more detailed explanation of the following topics can be found on our website:  
https://pynecone.io/docs/getting-started/introduction  
https://pynecone.io/docs/library  
https://pynecone.io/docs/hosting/deploy  
https://pynecone.io/docs/gallery  

Review these:  
* MTAD: Tools and Benchmark for Multivariate Time Series Anomaly Detection [https://github.com/OpsPAI/MTAD](https://github.com/OpsPAI/MTAD)  
* "GreyKite: Time Series Forecasting in Python." By Akshay Gupta, 2021-05-30  https://www.analyticsvidhya.com/blog/2021/05/greykite-time-series-forecasting-in-python/  
and https://github.com/linkedin/greykite  
* "A comprehensive beginner’s guide to create a Time Series Forecast (with Codes in Python and R)."  By Aarshay Jain, 2016-02-06  https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/  
* functime is a Python library for production-ready global forecasting and time-series feature engineering (*comes with time-series preprocessing (box-cox, differencing etc), cross-validation splitters (expanding and sliding window), and forecast metrics (MASE, SMAPE etc)*) [https://github.com/descendant-ai/functime](https://github.com/descendant-ai/functime)  
* weightedcalcs: A pandas-based Python library for calculating weighted means, medians, standard deviations, and more. [https://github.com/jsvine/weightedcalcs](https://github.com/jsvine/weightedcalcs)  


### Testing After Migrating to a New PC  
The old PC took 51:40 to run main.py, and the new PC took 25:05 for exactly the same work.  This means that while there is material opportunity for optimization in this Python code, it runs around half the time on the new PC.  

Old PC:  
```terminal
-----------
Record: 1
Record: 2
Record: 3
Record: 4
Record: 5
...
Record: 19515
Record: 19516
Record: 19517
Record: 19518
Record: 19519
Found: D:\Tools\bin\headers.py
- - - - - - - - - - - - - - - - - - - - - - - -
D:\testing\emerg-call-data-review\main.py Report ended at: 2023-02-16 16:03:50.923124
Search Report took: 0:51:40.038619
Target Report Files: D:\testing\emerg-call-data-review
- - - - - - - - - - - - - - - - - - - - - - - -
```

NEW PC:  
```terminal
C:\testing\emerg-call-data-review\venv\Scripts\python.exe C:\testing\emerg-call-data-review\main.py 

- - - - - - - - - - - - - - - - - - - - - - - -
C:\testing\emerg-call-data-review\main.py Report started at: 2023-02-28 11:35:53.950303
Root of target filesystem: C:\testing\emerg-call-data-review
- - - - - - - - - - - - - - - - - - - - - - - -
Record: 1
Record: 2
Record: 3
Record: 4
Record: 5
...
Record: 19515
Record: 19516
Record: 19517
Record: 19518
Record: 19519
Did not find headers.py in the path. Returned: None
- - - - - - - - - - - - - - - - - - - - - - - -
C:\testing\emerg-call-data-review\main.py Report ended at: 2023-02-28 12:00:59.916718
Search Report took: 0:25:05.966415 
Target Report Files: C:\testing\emerg-call-data-review
- - - - - - - - - - - - - - - - - - - - - - - -

Process finished with exit code 0
```
