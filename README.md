# Review Raw Emergency Call Data  

First pass at the raw data from AM.

This is a subset of the call. 
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
| response_level | str | 1 empty, 198 unique 1 or 2-char strings; see the full list below | |
| call_type | str | Medical Priority Dispatch System (MPDS) Codes. Example at http://www.rcfireassoc.org/emd.pdf | |
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
