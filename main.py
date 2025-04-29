import read_and_parse
import process_csv
import unit_testing

def main():
    # Reads the csv file and parses it
    parsed_csv = read_and_parse.read_csv("logs.log") 
    if parsed_csv is None:
        print("Error: Could not read the CSV file.")
        return
    # Generates the logs based on the specified conditions
    log_output = process_csv.create_logs(parsed_csv) 
    
    with open("logs.txt", 'w') as f: 
        for event in log_output:
            print(event, file = f)

def test_solution():
    # Generate tests cases for the logs
    for i in range(1, 6):
        unit_testing.generate_test_cases(i * 10, f"logs{i}.log", f"logs{i}.txt")

    # Checks if the generated test cases are correct with what the process_csv.solve_logs function returns
    for i in range(1, 6):
        unit_testing.test_create_logs_output(f"logs{i}.log", f"logs{i}.txt")

if __name__ == "__main__":
    main()
    test_solution()