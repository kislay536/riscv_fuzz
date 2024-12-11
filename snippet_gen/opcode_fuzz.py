import pandas as pd
import sys

# sys.argv contains command-line arguments
# sys.argv[0] is the script name, sys.argv[1] is the first argument (line number)
if len(sys.argv) > 1:
    line_num = int(sys.argv[1])  # Get the line number from the command-line argument
    print("Line number received:", line_num)
else:
    print("No line number received")

def read_and_search_assembly(file_path, csv_path, line_num):
    """
    Reads a specific line from the .s file based on line_num,
    extracts the first part of the line,
    searches for it in the "Opcode" column of a CSV file,
    and stores the corresponding ("a", "imm", "aqrl/rm") pair.

    Args:
        file_path (str): Path to the .s file.
        csv_path (str): Path to the CSV file.
        line_num (int): The line number to process (1-based index).

    Returns:
        tuple: A tuple containing ("a", "imm", "aqrl/rm") if a match is found, else None.
    """
    try:
        # Load the CSV file
        data = pd.read_csv(csv_path)

        # Replace NaN values with empty strings
        data = data.fillna("")

        # Validate required columns
        required_columns = {"number_regs", "imm/shamt", "Opcode", "aqrl/rm"}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")

        # Read the .s file and process the specific line
        with open(file_path, 'r') as file:
            lines = file.readlines()

            if line_num <= 0 or line_num > len(lines):
                print("Error: line_num is out of range")
                return None
            
            line = lines[line_num - 1].strip()  # Get the specific line (convert to 0-based index)
            first_part = line.split()[0] if line.split() else None  # Extract the first part (opcode)

            if first_part:
                # Search for the first part in the "Opcode" column
                matching_row = data.loc[data['Opcode'] == first_part]

                if not matching_row.empty:
                    # Extract corresponding "number_regs", "imm/shamt", and "aqrl/rm" values
                    a_value = matching_row.iloc[0]['number_regs']
                    imm_value = matching_row.iloc[0]['imm/shamt']
                    aq_rm = matching_row.iloc[0]["aqrl/rm"]
                    return (a_value, imm_value, aq_rm)

        return None  # Return None if no match was found or line_num is invalid

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_matching_opcodes(csv_path, a_value, imm_value, aq_rm):
    """
    Searches the CSV for all rows where the triplet ("a", "imm", "aqrl/rm") matches,
    and returns a list of all opcodes that correspond to this triplet.

    Args:
        csv_path (str): Path to the CSV file.
        a_value (str): The "number_regs" value.
        imm_value (str): The "imm/shamt" value.
        aq_rm (str): The "aqrl/rm" value.

    Returns:
        list: List of opcodes that match the given triplet.
    """
    try:
        # Load the CSV file
        data = pd.read_csv(csv_path)

        # Replace NaN values with empty strings
        data = data.fillna("")

        # Find all rows where the triplet matches
        matching_rows = data.loc[(data['number_regs'] == a_value) &
                                 (data['imm/shamt'] == imm_value) &
                                 (data['aqrl/rm'] == aq_rm)]

        # Extract and return the list of opcodes that match
        return matching_rows['Opcode'].tolist()

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    # Replace 'snippet.s' and 'opcodes.csv' with your file paths
    s_file_path = "snippet.s"
    csv_file_path = "opcodes.csv"

    match = read_and_search_assembly(s_file_path, csv_file_path, line_num)
    
    if match:
        a, imm, aq = match
        print(f"Match for line {line_num}: a = {a}, imm = {imm}, aq/rm = {aq}")
        
        # Find and print all opcodes that match this triplet
        matching_opcodes = find_matching_opcodes(csv_file_path, a, imm, aq)
        if matching_opcodes:
            print(f"Opcodes matching the triplet ({a}, {imm}, {aq}):")
            for opcode in matching_opcodes:
                print(f"- {opcode}")
        else:
            print(f"No opcodes found matching the triplet ({a}, {imm}, {aq})")
    else:
        print(f"No match found for line {line_num}")
