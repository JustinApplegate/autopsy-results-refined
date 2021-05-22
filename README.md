# Autopsy Keyword Results Refiner
The common digital forensics software Autopsy has a few preset keyword search options, including phone numbers, emails, and IP addresses based on regex statements. While using them, I noticed that they were a little too broad, so I decided to write these Python scripts that sorted and cleaned the results. Specifics for modifications and script usage are included below. 

## Phone Numbers
To run the program, use the following command:

`python3 phone_refine.py input_data.csv [output_data.csv]`

You must specify the CSV file downloaded of the list of phone numbers and number of occurrences of each number in the command. Specifying an output name is optional, and the default is `refined.csv`. 

During the cleaning process, all numbers that have a 3-digit area code or a 7-digit local number that start with a 0 or 1 are removed, per the [North America Numbering Plan](https://en.wikipedia.org/wiki/North_American_Numbering_Plan#Modern_plan). The numbers are formatted like (xxx) xxx-xxxx for easy reading. They are then sorted by the most occurrences. 

After sorting them all, it prints out how many invalid entries were removed from the list.

### Example
```
user@desktop:~$ head phoneNumbersOld.csv 
"List Name","Files with Hits"
"(206) 555-1212 (2)","2"
"(208) 522-5911 (2)","2"
"(303) 210-0665 (4)","4"
"(303) 646-2359 (2)","2"
"(303) 912-3644 (2)","2"
"(310) 433-0685 (2)","2"
"(402) 658-8799 (2)","2"
"(413) 555-0190 (2)","2"
"(413) 555-0191 (2)","2"

user@desktop:~$ python3 phone_refine.py phoneNumbersOld.csv results2.csv
45/513 results were removed (9%)

user@desktop:~$ head results2.csv
Phone Number,Files with Hits
(847) 718-0400,14
(252) 227-7013,12
(800) 548-4725,8
(416) 340-8666,6
(480) 248-7882,6
(781) 665-0053,6
(480) 444-6916,6
(602) 930-7749,6
(480) 685-1547,6
```

## IP Addresses
To run the program, use the following command:

`python3 ip_addr_refine.py input_data.csv [output_data.csv]`

You must specify the CSV file downloaded of the list of IP addresses and number of occurrences of each number in the command. Specifying an output name is optional, and the default is `refined.csv`. 

During the cleaning process, all IP addresses in the 0.x.x.x range and 240.x.x.x to 255.x.x.x ranges have been removed. Then, the remaining IP addresses receive an "Improbable" rating of yes or no, depending on how likely the number is actually an IP address and not a version number. Numbers with the first octet being less than 10 and having 2+ octets of only 0 are marked as improbable. Then, the list is sorted by Improbable (No, then Yes), then Files with Hits (largest to smallest), then IP Address. 

While there are still many potential IP addresses in the 10.x.x.x range that are only version numbers, the prevalence of 10.x.x.x IP addresses in the private IP range is high enough that I didn't want to mark any as improbable. 

After sorting them all, it prints out how many invalid entries were removed from the list and how many were marked as improbable.

### Example
```
user@desktop:~$ head ipAddressesOld.csv 
"List Name","Files with Hits"
"0.0.0.0 (136)","136"
"0.0.0.19 (1)","1"
"0.0.0.24 (1)","1"
"0.0.0.30 (2)","2"
"0.0.0.5 (1)","1"
"0.0.0.6 (3)","3"
"0.0.0.60 (1)","1"
"0.0.1.0 (2)","2"
"0.0.1.1 (1)","1"

user@desktop:~$ python3 ip_addr_refine.py ipAddressesOld.csv results.csv
61/1639 results were removed (4%)
1129/1578 results were marked as improbable (72%)

user@desktop:~$ head results.csv 
IP Address,Files with Hits,Improbable
10.0.1.5,513,No
20.4.0.40,203,No
20.5.0.28,203,No
19.1.0.19,197,No
20.1.0.9,190,No
20.6.0.27,87,No
10.0.1.2,27,No
192.168.1.1,18,No
10.0.1.3,17,No
```