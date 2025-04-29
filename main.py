import read_and_parse
import process_csv

def main():
    parsed_csv = read_and_parse.read_csv("logs.log")
    if parsed_csv is None:
        print("Failed to read the CSV file.")
        return
    logs = process_csv.create_logs(parsed_csv)
    print(logs)

if __name__ == "__main__":
    main()