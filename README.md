# Review Raw Emergency Call Data  

First pass at the raw data from AM.

This is a subset of the call. 
Assume that all records are anonymous. 


## Data Column Descriptions  
| Name|Data Type|Description|
|+-----+|+-----+|+-----+|
| fdid | int | |
| incident_num | int | |
| incident_date | datetime | Time is either "12:00 AM" or "0:00" -- it does not represent the actual time of the call. |
| Mutual_Aid_FDID | NULL | |
| Mutual_Aid_State | NULL | |
| Mutual_Aid_Incident_Num | NULL | |
| response_level | string | 1 empty, 198 unique 1 or 2-char strings; see the full list below |
| call_type |  |  | Medical Priority Dispatch System (MPDS) Codes. Example at http://www.rcfireassoc.org/emd.pdf |
| Unit_Dispatch_Times |  |  |
| Unit_Enroute_Times |  |  |
| Unit_Arrive_Times |  |  |
| Unit_At_Patient_Times |  |  |
| Unit_Enroute_To_Hospital_Times |  |  |
| Unit_Arrive_At_Hospital_Times |  |  |
| Unit_Staging_Times |  |  |
| Unit_Fire_Out_Times |  |  |
| Unit_Clear_Times |  |  |
| Time_In_Service |  |  |
| disposition_remarks | |
