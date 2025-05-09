## Requirements
    • Python3 installed
## How to use
```bash
To run the file: python3 main.py
The main.py will generate 10 files: 5 input logs (.log) and 5 expected output files (.txt). 
After that, it will evaluate if the output logs are correct
```

```bash
To run with an external input file, uncomment the 28 line. 
A file called logs.log with the following structure is required:
    • HH:MM:SS is a timestamp in hours, minutes, and seconds. 
    • A job description.
    • Either the “START” or “END” of a process. 
    • Each job has a PID associated with it e.g., 46578. 
```
## How it works
The solution reads and parses a CSV file, using a default delimiter = ',' if not specified and removes all the extra spaces if exist.

After the CSV is parsed, it goes through each line and stores in a dict with key = PID, value = START_timestamp

When the same PID is found and the process is marked with END, it checks the difference between end_timestamp and start_timestamp in seconds

It logs a message if the difference is bigger than 300 seconds but lower than 600 seconds with WARNING, else if difference is > 600 seconds it logs an ERROR

All the following corner cases were treated:
```
    • A process that starts but doesn't end
    • A process that has the start timestamp in seconds bigger than the end timestamp
    • A process that starts over and over, it keeps only the first start
    • A process that ends but it never started, it ignores it
```
#
Beside the solution, some tests were generated using the unit_testing.py file. The tests are checked in the main function.
