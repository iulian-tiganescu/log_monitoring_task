import read_and_parse

def main():
    parsed_csv = read_and_parse.read_csv("logs.log")
    for row in parsed_csv:
        print(row)

if __name__ == "__main__":
    main()