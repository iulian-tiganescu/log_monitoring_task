from datetime import datetime, timedelta

def time_to_seconds(timestamp: str) -> int:
    """Converts a string timestamp, formated as 'HH:MM:SS', to seconds."""
    time = datetime.strptime(timestamp, "%H:%M:%S").time()
    return time.hour * 3600 + time.minute * 60 + time.second

def create_logs(parsed_csv: list[list[ str ]]) -> list[ str ]:
    """Compute a list with jobs that took longer than 5 minutes to execute based on a log file
    >= 10 minutes produces an ERROR message
    >= 5 and < 10 minutes produces a WARNING message"""
    
    jobs_dict = {}
    logs = []

    for event in parsed_csv:
        # Ensures that if a process starts again without ending first, it will not reset the timestamp
        if event[ 3 ] in jobs_dict and event[ 2 ].lower() == 'end':
            # Stores timestamps in seconds
            start_time = time_to_seconds(jobs_dict[ event[ 3 ]])
            end_time = time_to_seconds(event[ 0 ])
            task_description = event[ 1 ]
            
            if start_time > end_time: #should this annomaly be logged?
                logs.append(f"ERROR: Start time is grater than end time for task {task_description} with PID {event[ 3 ]}")
                continue

            passed_time = end_time - start_time
            # Convert seconds back to 'HH:MM:SS' to make it more readable
            reconstructed_passed_time = timedelta(seconds=passed_time)

            if passed_time >= 600:
                logs.append(f"ERROR: Process {task_description} with - {event[ 3 ]} PID, took {reconstructed_passed_time} to execute")
            elif passed_time >= 300:
                logs.append(f"WARNING: Process {task_description} with - {event[ 3 ]} PID, took {reconstructed_passed_time} to execute")
            del jobs_dict[ event[ 3 ] ] # normally PIDs are reusable, it applies to this case?
        # Ensures that a end process is not logged if it was never started
        elif event[ 3 ] not in jobs_dict and event[ 2 ].lower() == 'start':
            jobs_dict[ event[ 3 ] ] = event[ 0 ]
            
    # If there are any processes that started but never ended, log them
    if jobs_dict:
        for key in jobs_dict:
            logs.append(f"ERROR: Process {key} didn't finish") 

    return logs