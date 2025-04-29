def create_logs(parsed_csv: list[list[ str ]]) -> list[ str ]:
    """Compute a list with jobs that took longer than 5 minutes to execute based on a log file
    >= 10 minutes produces an ERROR message
    >= 5 and < 10 minutes produces a WARNING message"""

    jobs_dict = {}
    logs = []
    for event in parsed_csv:
        if event[ 3 ] in jobs_dict and event[ 2 ].lower() == 'end':
            start_time = 1 # find a way to parse date
            end_time = 1 
            task_description = event[ 1 ]

            if start_time > end_time: #should this annomaly be logged?
                logs.append(f"ERROR: Start time is grater than end time for task {task_description} with PID {event[ 3 ]}")
                continue

            passed_time = end_time - start_time # find a way to obtain the time difference

            if passed_time >= 10: #or 600 seconds?
                logs.append(f"ERROR: Process {task_description} with - {event[ 3 ]} PID, took {passed_time} minutes to execute")
            elif passed_time >= 5: #or 300 seconds?
                logs.append(f"WARNING: Process {task_description} with - {event[ 3 ]} PID, took {passed_time} minutes to execute")
            else: #temporary message for testing purposes
                logs.append(f"INFO: Process {task_description} with - {event[ 3 ]} PID, took {passed_time} minutes to execute")
            del jobs_dict[ event[ 3 ] ] # normally PIDs are reusable, it applies to this case?

        elif event[ 3 ] not in jobs_dict and event[ 2 ].lower() == 'start':
            jobs_dict[ event[ 3 ] ] = event[ 0 ]

    if jobs_dict: # corner case if there's no end for a started job
        for key in jobs_dict:
            logs.append(f"ERROR: Process {key} didn't finish")
    
    return logs