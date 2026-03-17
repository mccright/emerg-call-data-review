# Emergency Data Timeseries plots

## ToDo:  
Review https://github.com/eceariakdemir/Biofuel-MOEA/tree/main/Figure%20codes%20and%20datasets for example charting code ideas. It is associated with this article: https://www.sciencedirect.com/science/article/pii/S0961953425000017#bib68.  That article presents the outputs of the github repo code.  

One of the examples in the article below may work to match given Nebraska codes with codes from the code table:
The fastest way to detect a vowel in a string
6/13/2025
https://austinhenley.com/blog/vowels.html


#### Started with "Light timeseries plots"  
Original by Fabio Arciniegas  
Original at: https://github.com/fabioarciniegas/light_timeseries_charts/tree/master  

## Assembled for quick aggregation of Lincoln County, Nebraska Emergency Service Response Data

Plot diagrams using time series data having the layout below:

``` csv
"incident_date","response_unit","dispatch_time","time_in_service"
"01/01/10","M5","07:05:17","00:04:56"
"01/01/10","WAVE1","06:51:33","00:20:10"
"01/01/10","WAVE12","06:51:33","01:26:48"
"01/01/10","GRE310","07:56:42","00:06:56"
"01/01/10","WAVE1","07:56:42","00:11:42"
"01/01/10","WAVE11","08:05:59","00:59:47"
"01/01/10","MWM31","09:51:58","02:08:33"
"01/01/10","PLEA1","09:51:58","00:40:12"
"01/01/10","PLEA2","09:51:58","00:40:17"
"01/01/10","SE1","15:48:32","00:20:35"
"01/01/10","SE11","15:48:32","00:20:06"
"01/01/10","SE12","15:58:26","00:33:07"
"01/01/10","B1","20:22:57","00:00:05"
"01/02/10","8707","02:02:55","02:48:52"
"01/02/10","CERE1","01:41:51","02:58:42"
"01/02/10","RAYM1","01:46:16","01:52:36"
"01/02/10","WAVE1","01:46:16","01:07:18"
"01/02/10","SW1","16:33:09","00:26:58"

```

This was assembled to consolidate some of the Lincoln County, Nebraska emergency service response data into simple time series plots.  

The input data is in a csv file.  The output is in png files.

Normally response_unit is the name of a given team, dispatch_time is when they received a call for service and time_in_service is the amount of time a given response_unit spent on that given service.


![trial report](reports/trial.png)


LFR Ambulances are noted by "M," signifying "Medic" followed by a number.  
	These include:  
		M1, M2, M3, M5, M6, M7, M8, M10, M21, M24, M25
		There may be other M-units listed in the data, but my sense is that those are typos or are very rarely called and will not affect the general sense of the data.

* Quality check for those "M" LFR ambulance designators in the data:  
```terminal
matt@host:/dev/emerg-call-data$ strings 2024-11-06_emerg_data_organized.csv | cu
t -d "," -f 2 | grep \"M | sort | uniq -c | sort
      1 "M21"
      1 "MILF10"
      1 "MWM33"
      2 "MWM35"
      4 "MWM34"
      6 "MWM32"
      7 "M214"
      9 "M211"
     10 "M24"
     13 "M1"
     15 "M25"
     25 "MALC2"
     56 "MWM31"
     61 "M10"
    307 "M2"
    367 "M7"
    543 "MALC10"
    550 "M8"
    609 "M3"
    984 "M5"
   1213 "MALC1"
   2128 "M6"
matt@host:/dev/emerg-call-data$
```

Then remove the out-of-scope units and present the rest:
```terminal
matt@host:/dev/emerg-call-data$ strings 2024-11-06_emerg_data_organized.csv | cut -d "," -f 2 | grep \"M | grep -v -E "(\"MA|\"MW|\"MI)" | sort | uniq -c | sort
      1 "M21"
      7 "M214"
      9 "M211"
     10 "M24"
     13 "M1"
     15 "M25"
     61 "M10"
    307 "M2"
    367 "M7"
    550 "M8"
    609 "M3"
    984 "M5"
   2128 "M6"
matt@host:/dev/emerg-call-data$ strings 2024-11-06_emerg_data_organized.csv | cut -d "," -f 2 | grep \"M | grep -v -E "(\"MA|\"MW|\"MI)" | sort | uniq | sort
"M1"
"M10"
"M2"
"M21"
"M211"
"M214"
"M24"
"M25"
"M3"
"M5"
"M6"
"M7"
"M8"
matt@host:/dev/emerg-call-data$
```



What is the median response time on major calls for County ambulances each year?
"Major Calls" are "call_type":
		 That include "Sub Category" C (Charlie), D (Delta), or E (Echo) \
		 as defined by the file "110520 Master Run Sheet.xlsx"
		call_type:
			FIREC, GRASFIRE, RSALARM, ECHO, CARFIRE, MEDC, MEDD, MEDE

```			
 strings 2024-11-06_emerg_data_organized.csv | cut -d "," -f 2 | grep -E "(\"WAVE|\"SW|\"SE|\"HICK|\"MALC|\"RAYM|\"BENN|\"HALL|\"PLEA|\"FIRT)" | wc -l
 
 matt@host:/dev/emerg-call-data$ strings 2024-11-06_emerg_data_organized.csv | cut -d "," -f 2 | grep -E "(\"WAVE|\"SW|\"SE|\"HICK|\"MALC|\"RAYM|\"BENN|\"HALL|\"PLEA|\"FIRT)" | wc -l
15715
matt@host:/dev/emerg-call-data$ strings 2024-11-06_emerg_data_organized.csv | cut -d "," -f 2 | grep -E "(\"WAVE|\"SW|\"SE|\"HICK|\"MALC|\"RAYM|\"BENN|\"HALL|\"PLEA|\"FIRT)" | sort | uniq -c | sort
      1 "FIRT3"
      1 "RAYMWR"
      1 "SE3"
      1 "SE5"
      2 "RAYM3"
      2 "WAVE3"
      3 "SW3"
      4 "HALL2"
     15 "RAYM2"
     16 "FIRT2"
     16 "SE2"
     17 "BENN2"
     21 "PLEA2"
     25 "MALC2"
     32 "SW2"
     36 "HICK2"
     40 "WAVE2"
     96 "HICK11"
    221 "WAVE11"
    223 "HALL1"
    336 "RAYM11"
    338 "PLEA1"
    365 "HALL11"
    387 "SE11"
    410 "SW12"
    432 "SE12"
    516 "RAYM10"
    543 "MALC10"
    864 "SE1"
    876 "FIRT1"
   1035 "WAVE1"
   1077 "SW11"
   1097 "RAYM1"
   1176 "SW1"
   1179 "BENN1"
   1213 "MALC1"
   1511 "WAVE12"
   1587 "HICK1"
matt@host:/dev/emerg-call-data$
```

How many response_unit incident calls are there in our universe of records? 22830  
How many response_unit incident calls are unambiguously tagged with a priority "sub_category"? 14246  
That leaves 8584 response_unit incident calls in some state of priority ambiguity.  (*22830 - 14246 = 8584*)  
```
matt@host:/dev/emerg-call-data$ wc -l 2025-08-02_emerg_data_organized_step_four.
csv
22830 2025-08-02_emerg_data_organized_step_four.csv
matt@host:/dev/emerg-call-data$ cat 2025-08-02_emerg_data_organized_step_four.csv | cut -d "," -f 7 | grep -E "(alpha|bravo|charlie|delta|echo)" | wc -l
14246
matt@host:/dev/emerg-call-data$ cat 2025-08-02_emerg_data_organized_step_four.csv | cut -d "," -f 7 | grep -v -E "(alpha|bravo|charlie|delta|echo)" | wc -l
8584
matt@host:/dev/emerg-call-data$
```

So, what is this *non-standard* universe of response_unit incident calls categorized as?  
There are 36 unique "sub_category" types.  

```
matt@host:/dev/emerg-call-data$ cat 2025-08-02_emerg_data_organized_step_four.csv | cut -d "," -f 7 | grep -v -E "(alpha|bravo|charlie|delta|echo)" | sort | uniq -c | sort | wc -l
36
matt@host:/dev/emerg-call-data$ cat 2025-08-02_emerg_data_organized_step_four.csv | cut -d "," -f 7 | grep -v -E "(alpha|bravo|charlie|delta|echo)" | sort | uniq -c | sort
      1 ammo
      1 sub_category
      2 c13f
      2 hazpkg
      3 arson
      3 bomb
      3 elevator
      4 aircrash
      6 servcall
      7 swat
     20 dumpfire
     22 suspart
     30
     36 medsd
     66 standby
     74 wires
     78 haz3
     93 accle
     94 codet
    116 medfd
    160 haz2
    162 specduty
    192 fireb
    204 odor
    213 mutaid
    234 medoa
    260 medical
    395 firea
    443 carfire
    586 still
    675 rsalarm
    686 firec
    739 als
    838 CTNIMRS
    909 medle
   1227 grasfire
matt@host:/dev/emerg-call-data$ 
```

Number of response_unit incident calls in column 1, and the term used in the data, and (the term's definition):  

     93 accle (medical request for accident - by law enforcement)
     94 codet (carbon monoxide det, hazmat)
    116 medfd (medical request from fire department)
    160 haz2 (hazmat level 2)
    162 specduty (special duty)
    192 fireb (fire bldg in peril)
    204 odor (burn/chem/elec/gas hazmat call)
    213 mutaid (mutual aid, fire, based on request made)
    234 medoa (medical request from outside agency)
    260 medical
    395 firea (fire alarm - alpha)
    443 carfire (car on fire)
    586 still (minor fire, still)
    675 rsalarm (rescue alarm)
    686 firec (fire confirmed)
    739 als
    838 CTNIMRS
    909 medle (medical request from law enforcement),
   1227 grasfire (grass on fire)

I could not find useful definitions (*that might identify a priority*) for the following terms:  
ToDo: What are "CTNIMRS", "als", "medical", "specduty" calls?  

How many 
```
cat 2025-08-02_emerg_data_organized_step_four.csv | cut -d "," -f 7 | grep -E "(alpha|bravo|charlie|delta|echo)" | wc -l
```


```
matt@host:/dev/emerg-call-data$ grep alpha 2025-08-02_emerg_data_organized_step_four.csv | wc -l
2594
matt@host:/dev/emerg-call-data$ grep bravo 2025-08-02_emerg_data_organized_step_
four.csv | wc -l
2966
matt@host:/dev/emerg-call-data$ grep charlie 2025-08-02_emerg_data_organized_ste
p_four.csv | wc -l
2352
matt@host:/dev/emerg-call-data$ grep delta 2025-08-02_emerg_data_organized_step_
four.csv | wc -l
6018
matt@host:/dev/emerg-call-data$ grep echo 2025-08-02_emerg_data_organized_step_f
our.csv | wc -l
576
matt@host:/dev/emerg-call-data$ grep firea 2025-08-02_emerg_data_organized_step_
four.csv | wc -l
395
matt@host:/dev/emerg-call-data$ grep fireb 2025-08-02_emerg_data_organized_step_
four.csv | wc -l
192
matt@host:/dev/emerg-call-data$ grep firec 2025-08-02_emerg_data_organized_step_
four.csv | wc -l
686
matt@host:/dev/emerg-call-data$ grep fired 2025-08-02_emerg_data_organized_step_
four.csv | wc -l
0
matt@host:/dev/emerg-call-data$ grep firee 2025-08-02_emerg_data_organized_step_
four.csv | wc -l
0
```


Of those that are not, what is going on?  
```
$ grep -i medical 2025-08-02_emerg_data_organized_step_four.csv | cut -d "," -f 8 | sort | uniq -c | sort
      4 blood thinners - medical
      5 not dangerous hemorrhage - medical
      9 serious hemorrhage - medical
     13 medical request
     14 abnormal breathing - medical
     14 possibly dangerous hemorrhage - medical
     16 not alert - medical
     21 dangerous hemorrhage - medical
     36 medical request from service desk
     93 medical request for accident - by law enforcement
    116 medical request from fire department
    158 medical alarm (alert) notifications (no patient information)
    234 medical request from outside agency
    260 cardiac/respiratory arrest
    909 medical request from law enforcement
matt@host:/dev/emerg-call-data$
```

Are any of those "medical" calls also tagged with some type of unambiguous priority "sub_category"?  
Yes, there are 1902 response_unit incidents described as some "medical" type.  Of those, 514 are tagged with any of: alpha, bravo, charlie, delta or echo (*1902 - 1388 = 514*).  
```
$ grep -i medical 2025-08-02_emerg_data_organized_step_four.csv | wc -l
1902
$ grep -i medical 2025-08-02_emerg_data_organized_step_four.csv | grep -v -E "(alpha|bravo|charlie|delta|echo)" | wc -l
1388
$
```

If we remove those 514 from our universe of "medical" tagged response_unit incidents, then:  
```
$ grep -i medical 2025-08-02_emerg_data_organized_step_four.csv | grep -v -E "(alpha|bravo|charlie|delta|echo)" | cut -d "," -f 8 | sort | uniq -c | sort
     36 medical request from service desk
     93 medical request for accident - by law enforcement
    116 medical request from fire department
    234 medical request from outside agency
    909 medical request from law enforcement
```

What was the "sub_category" for those response_unit incidents?  
```
matt@host:/dev/emerg-call-data$ grep -i medical 2025-08-02_emerg_data_organized_step_four.csv | grep -v -E "(alpha|bravo|charlie|delta|echo)" | cut -d "," -f 7 | sort | uniq -c | sort
     36 medsd
     93 accle
    116 medfd
    234 medoa
    909 medle
matt@host:/dev/emerg-call-data$
```

Does that universe match our previous number (*1388*)?  Yes.  So, medsd, accle, medfd, medoa and medle are unique "sub_category" types.  
* accle == medical request for accident - by law enforcement  
* medfd == medical request from fire department  
* medle == medical request from law enforcement  
* medoa == medical request from outside agency  
* medsd == medical request from service desk  
I don't know how to identify the *priority* of calls in the 5 categories listed above  
```
$ grep -i medical 2025-08-02_emerg_data_organized_step_four.csv | grep -E "(medsd|accle|medfd|medoa|medle)" | wc -l
1388
```

What are the numeric tags used with CTNIMRS?  
```
$ cat 2025-08-02_emerg_data_organized_step_four.csv | cut -d "," -f 6-8 | grep CTNIMRS | sort | uniq -c | sort | wc -l
61
```
There are 61 unique numeric tags used with CTNIMRS.  
```
matt@host:/dev/emerg-call-data$ cat 2025-08-02_emerg_data_organized_step_four.csv | cut -d "," -f 6-8 | grep CTNIMRS | sort | uniq -c | sort
      1 26o11,CTNIMRS,CTNIMRS
      1 27b2,CTNIMRS,CTNIMRS
      1 28c11,CTNIMRS,CTNIMRS
      1 29b3m,CTNIMRS,CTNIMRS
      1 9o1,CTNIMRS,CTNIMRS
      1 grassfir,CTNIMRS,CTNIMRS
      2 15c1,CTNIMRS,CTNIMRS
      2 21a2,CTNIMRS,CTNIMRS
      2 21d1,CTNIMRS,CTNIMRS
      2 24o1,CTNIMRS,CTNIMRS
      2 26a13,CTNIMRS,CTNIMRS
      2 26a21,CTNIMRS,CTNIMRS
      2 26a32,CTNIMRS,CTNIMRS
      2 26a38,CTNIMRS,CTNIMRS
      2 27d1,CTNIMRS,CTNIMRS
      2 27d3,CTNIMRS,CTNIMRS
      2 29d3a,CTNIMRS,CTNIMRS
      2 29d3m,CTNIMRS,CTNIMRS
      2 9o1y,CTNIMRS,CTNIMRS
      3 27d2,CTNIMRS,CTNIMRS
      3 28c7,CTNIMRS,CTNIMRS
      3 29d5a,CTNIMRS,CTNIMRS
      4 20b2,CTNIMRS,CTNIMRS
      4 28c10,CTNIMRS,CTNIMRS
      4 28c5,CTNIMRS,CTNIMRS
      4 28c9,CTNIMRS,CTNIMRS
      4 29o1v,CTNIMRS,CTNIMRS
      4 33a1,CTNIMRS,CTNIMRS
      5 20d1,CTNIMRS,CTNIMRS
      5 33d1,CTNIMRS,CTNIMRS
      5 8o1,CTNIMRS,CTNIMRS
      5 9e6,CTNIMRS,CTNIMRS
      6 26o7,CTNIMRS,CTNIMRS
      6 33c3,CTNIMRS,CTNIMRS
      6 33c5,CTNIMRS,CTNIMRS
      7 23o1a,CTNIMRS,CTNIMRS
      7 28c2,CTNIMRS,CTNIMRS
      7 29b4a,CTNIMRS,CTNIMRS
      9 21b4,CTNIMRS,CTNIMRS
     11 33c4,CTNIMRS,CTNIMRS
     15 29d4a,CTNIMRS,CTNIMRS
     17 29d4m,CTNIMRS,CTNIMRS
     18 21d2,CTNIMRS,CTNIMRS
     20 29b4m,CTNIMRS,CTNIMRS
     20 29o1,CTNIMRS,CTNIMRS
     22 12a1,CTNIMRS,CTNIMRS
     24 21a1,CTNIMRS,CTNIMRS
     24 33c6,CTNIMRS,CTNIMRS
     27 28c3,CTNIMRS,CTNIMRS
     27 28c4,CTNIMRS,CTNIMRS
     28 21d3,CTNIMRS,CTNIMRS
     30 33c2,CTNIMRS,CTNIMRS
     33 21d4,CTNIMRS,CTNIMRS
     34 21b2,CTNIMRS,CTNIMRS
     34 33c1,CTNIMRS,CTNIMRS
     35 21b1,CTNIMRS,CTNIMRS
     40 29b1m,CTNIMRS,CTNIMRS
     43 29b1a,CTNIMRS,CTNIMRS
     49 29d2,CTNIMRS,CTNIMRS
     57 28c1,CTNIMRS,CTNIMRS
     97 10c4,CTNIMRS,CTNIMRS
matt@host:/dev/emerg-call-data$
```
