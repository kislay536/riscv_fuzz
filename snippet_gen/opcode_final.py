import os

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

if __name__ == "__main__":
    directory = "../gem5/m5out/"  # Replace with the path to your directory
    file_name = "stats.txt"
    file_path = os.path.join(directory, file_name)

    search_strings = ["simTicks", "branchPred.BTBHitRatio", "btb.mispredict::total", "cpu.numCycles", "cpu.cpi"]
    numbers = process_stats_file(file_path, search_strings)

    for key, value in numbers.items():
        print(f"String: {key}, Numbers: {value}")