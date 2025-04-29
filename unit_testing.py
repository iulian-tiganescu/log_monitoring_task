import random
from datetime import datetime, timedelta
from process_csv import time_to_seconds, create_logs
import read_and_parse

def generate_classic_case(timestamp_offset:int, offset_max: int, output_log: list[ str ]) -> tuple[str, str]:
    """Generate a job pair that is within an offset.
    It also adds unnecessary spaces to the lines, to test the parser."""
    # Takes current timestamp and adds an offset so that all the timestamps have not the same start time.
    timestamp = datetime.now() + timedelta(minutes=timestamp_offset)

    # Generate a random PID and some spaces to add to the line
    pid = random.randint(1000, 9999)
    spaces = " " * random.randint(0, 5)
    
    # Generate a random number of minutes to add to the timestamp
    offset_minutes = random.randint(0, offset_max)
    second_timestamp = (timestamp + timedelta(minutes=offset_minutes)).strftime("%H:%M:%S")

    # Converts the timestamp to HH:MM:SS format, it hasn't been done before so that operations with timedelta are possible.
    timestamp = timestamp.strftime("%H:%M:%S")
    
    # Generate the start and end lines with the timestamp, spaces, pid and the job name.
    start_line = f"{timestamp}{spaces},Example{spaces} Job, START{spaces},{spaces}{pid}"
    end_line = f"{second_timestamp}{spaces},Example{spaces} Job, END{spaces},{spaces}{pid}"
    
    # Adds info to the output log, will be used for unit testing.
    if offset_minutes >= 5 and offset_minutes < 10:
        output_log.append(f"WARNING: Process Example Job with - {pid} PID, took {timedelta(minutes=offset_minutes)} to execute")
    elif offset_minutes >= 10:
        output_log.append(f"ERROR: Process Example Job with - {pid} PID, took {timedelta(minutes=offset_minutes)} to execute")
    
    return start_line, end_line

def generate_not_paired_cases(timestamp_offset:int, state: str, output_log: list[ str ]) -> str:
    """Generate a job that doesn't have an end or start pair.
    It also adds unnecessary spaces to the lines, to test the parser."""
    # Takes current timestamp and adds an offset + converts it to HH:MM:SS format.
    timestamp = (datetime.now() + timedelta(minutes=timestamp_offset)).strftime("%H:%M:%S")
    # Generate a random PID and some spaces to add to the line
    pid = random.randint(1000, 9999)
    spaces = " " * random.randint(0, 5)
    
    # Generate the line with the timestamp, spaces, pid and the job name.
    line = f"{timestamp}{spaces},Example{spaces} Job, {state}{spaces},{spaces}{pid}"
    if state == "START":
        # Adds info to the output log, will be used for unit testing. In this case only if a process doesn't have an end matters.
        output_log.append(f"ERROR: Process {pid} didn't finish")

    return line

def generate_test_cases(num_cases: int, input_name: str, output_name: str) -> None:
    """Generate a test case with num_cases lines and save it to file_name"""
    output_log = []
    input_log = []
    # Generate the test cases, half of them will be classic cases and half of them will be corner cases
    for i in range(num_cases):
        if i % 2 == 0:
            start_line, end_line = generate_classic_case(i, 30, output_log)
            input_log.append(start_line)
            input_log.append(end_line)
        else:
            state = random.choice(["START", "END"])
            line = generate_not_paired_cases(i * 3, state, output_log)
            input_log.append(line)

    # Sort the input log by timestamp
    input_log.sort(key=lambda x: time_to_seconds(x.split(",")[0].strip()))

    # Save the input and output logs to files
    with open(input_name, 'w') as f:
        for line in input_log:
            print(line, file=f)
    with open(output_name, 'w') as f:
        for event in output_log:
            print(event, file=f)


def test_create_logs_output(generated_input_file: str, expected_output_file: str):
    # Read the output from the logs.txt file
    with open(expected_output_file, 'r') as f:
        expected_output = f.readlines()

    # It removes the '\n' from the end of the lines
    expected_output = [line.strip() for line in expected_output]

    # Reads the input and solves the test case
    parsed_csv = read_and_parse.read_csv(generated_input_file)
    actual_output = create_logs(parsed_csv)
    
    # Sort both outputs to ensure the output will match if everything is correct
    expected_output.sort()
    actual_output.sort()
    
    # Compare the outputs
    try:
        assert expected_output == actual_output, f"Test failed for {generated_input_file}."
        print(f"Test passed for {generated_input_file}. Outputs match.")
    except AssertionError as e:
        print(e)