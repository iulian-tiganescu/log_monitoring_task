import csv
import os

def read_csv(file_path: str, csv_delimiter: str = ',') -> list[ list[ str ] ]:
    """Reads a CSV file and parses it. Includes optional parameter for csv reading"""

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} doesn't exist.")
        return None

    try:
        with open(file_path, mode="r", newline="") as file:
            # Read the CSV file using the delimiter
            csv_reader = csv.reader(file, delimiter=csv_delimiter)
            # Parse the CSV file into a list of lists
            parsed_csv = [row for row in csv_reader]
            return parsed_csv
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None