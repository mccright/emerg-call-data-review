# Review Raw Emergency Call Data  

First pass at the raw data from AM.

This is a subset of the call data. There are 19,520 records. Records include dates from Jan. 2010 through Dec. 2020. 
Assume that all records are anonymous. 


## Data Column Descriptions  
| Name|Data Type|Description|Notes|
|:-----:|:-----:|:-----:|:-----:|
| fdid | int | | |
| incident_num | int | | |
| incident_date | datetime | Time is either "12:00 AM" or "0:00" -- it does not represent the actual time of the call. |
| Mutual_Aid_FDID | NULL | | Ignore/remove this column |
| Mutual_Aid_State | NULL | | Ignore/remove this column |
| Mutual_Aid_Incident_Num | NULL | | Ignore/remove this column |
| response_level | str | 1 empty, 198 unique 1 or 2-char strings; see the full list below | Field is right-padded with spaces to a length of 11 char. |
| call_type | str | Medical Priority Dispatch System (MPDS) Codes. Example at http://www.rcfireassoc.org/emd.pdf | Data contains 600 unique strings. Remove records containing "TEST". |
| Unit_Dispatch_Times | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_Enroute_Times | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_Arrive_Times |  str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_At_Patient_Times | NULL |  | Ignore/remove this column |
| Unit_Enroute_To_Hospital_Times | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_Arrive_At_Hospital_Times | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Unit_Staging_Times | NULL |  | Ignore/remove this column |
| Unit_Fire_Out_Times | NULL |  | Ignore/remove this column |
| Unit_Clear_Times | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| Time_In_Service | str | One or more 'key=value' pairs containing "OrgApparatusAbbreviation"="time" where time is in 24-hour formatted hh:mm:ss. May be NULL. | Convert into Python dictionary |
| disposition_remarks |  |  | Remove records containing any of the following in this column: "STORED COMPLAINT DUP:" "(FILE ONLY COMPLAINT)" "TEST" |

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
| Number | string |
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
