# Review Raw Emergency Call Data  

First pass at the raw data from AM.

This is a subset of the call data. There are 19,520 records. Records include dates from Jan. 2010 through Dec. 2020. 
Assume that all records are anonymous. 

## Pandas data_frame.info() Summary of This Raw Data Without Processing 
```terminal
RangeIndex: 19520 entries, 0 to 19519
Data columns (total 19 columns):
 #   Column                          Non-Null Count  Dtype  
---  ------                          --------------  -----  
 0   fdid                            19520 non-null  int64  
 1   incident_num                    19520 non-null  int64  
 2   incident_date                   19520 non-null  object 
 3   Mutual_Aid_FDID                 0 non-null      float64
 4   Mutual_Aid_State                0 non-null      float64
 5   Mutual_Aid_Incident_Num         0 non-null      float64
 6   response_level                  19520 non-null  object 
 7   call_type                       19520 non-null  object 
 8   Unit_Dispatch_Times             18335 non-null  object 
 9   Unit_Enroute_Times              16524 non-null  object 
 10  Unit_Arrive_Times               15464 non-null  object 
 11  Unit_At_Patient_Times           4341 non-null   object 
 12  Unit_Enroute_To_Hospital_Times  8114 non-null   object 
 13  Unit_Arrive_At_Hospital_Times   7394 non-null   object 
 14  Unit_Staging_Times              0 non-null      float64
 15  Unit_Fire_Out_Times             49 non-null     object 
 16  Unit_Clear_Times                18277 non-null  object 
 17  Time_In_Service                 18379 non-null  object 
 18  disposition_remarks             8356 non-null   object 
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


## Some Column Data Summarized  
### call_type  
There are 600 unique "call_type" strings in the universe of 19,520 records.  
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

#### The top 12 "call_type" strings and their frequency  
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


### response_level  
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
Experiment with the code at: https://github.com/DataForScience/Timeseries using the notes that I took in the "Times Series Analysis for Everyone: Introduction" class and the content at: https://data4sci.com/timeseries.  
Try writing the scripting so that it can be hosted using Pynecone - "performant, customizable web apps in pure Python."  https://github.com/pynecone-io/pynecone  
>Pynecone is a full-stack Python framework that makes it easy to build and deploy web apps in minutes. All the information for getting started can be found in this README. However, a more detailed explanation of the following topics can be found on our website:  
https://pynecone.io/docs/getting-started/introduction  
https://pynecone.io/docs/library  
https://pynecone.io/docs/hosting/deploy  
https://pynecone.io/docs/gallery  

Review these:  
* "GreyKite : Time Series Forecasting in Python." By Akshay Gupta, 2021-05-30  https://www.analyticsvidhya.com/blog/2021/05/greykite-time-series-forecasting-in-python/  
and https://github.com/linkedin/greykite  
* "A comprehensive beginner’s guide to create a Time Series Forecast (with Codes in Python and R)."  By Aarshay Jain, 2016-02-06  https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/  
* functime is a Python library for production-ready global forecasting and time-series feature engineering (*comes with time-series preprocessing (box-cox, differencing etc), cross-validation splitters (expanding and sliding window), and forecast metrics (MASE, SMAPE etc)*) [https://github.com/descendant-ai/functime](https://github.com/descendant-ai/functime)  

