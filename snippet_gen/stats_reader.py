import os
import csv
import sys

def process_stats_file(file_path, search_strings):
    results = {}

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for search_string in search_strings:
            for idx, line in enumerate(lines):
                if search_string in line:
                    results[search_string] = results.get(search_string, [])
                    results[search_string].append(idx + 1)  # Store line number

        extracted_numbers = {}
        for search_string, line_numbers in results.items():
            extracted_numbers[search_string] = []
            for line_number in line_numbers:
                line = lines[line_number - 1]
                parts = line.split()
                if len(parts) > 1:
                    try:
                        number = float(parts[1])
                        extracted_numbers[search_string].append(number)
                    except ValueError:
                        continue

        return extracted_numbers

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def update_or_append_csv(csv_file, name, data):
    header = ["name", "simTicks", "branchPred.BTBHitRatio", "btb.mispredict::total", "cpu.numCycles", "cpu.cpi"]
    new_row = [name] + [data.get(key, [None])[0] for key in header[1:]]

    # Read the existing data from the CSV file
    try:
        rows = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
    except FileNotFoundError:
        rows = [header]

    # Check if name exists and update the row
    updated = False
    for i, row in enumerate(rows):
        if row[0] == name:
            rows[i] = new_row
            updated = True
            break

    # If name not found, append as a new row
    if not updated:
        rows.append(new_row)

    # Write the data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 stats_reader.py {name}")
        sys.exit(1)

    name = sys.argv[1]
    directory = "./m5out/"  # Replace with the path to your directory
    file_name = "stats.txt"
    file_path = os.path.join(directory, file_name)
    directory_csv = "./"  # Replace with the path to your directory
    csv_file = os.path.join(directory_csv, "stats_data.csv")

    search_strings = ["simTicks", "branchPred.BTBHitRatio", "btb.mispredict::total", "cpu.numCycles", "cpu.cpi"]
    numbers = process_stats_file(file_path, search_strings)

    update_or_append_csv(csv_file, name, numbers)
    print(f"Data for {name} has been updated in {csv_file}.")
