import pandas as pd

def read_and_search_assembly(file_path, csv_path):
    """
    Reads a .s file, extracts the first part of each line,
    searches for it in the "opcodes" column of a CSV file,
    and stores the corresponding ("a", "imm") pair.

    Args:
        file_path (str): Path to the .s file.
        csv_path (str): Path to the CSV file.

    Returns:
        list: List of tuples containing ("a", "imm") pairs for matching rows.
    """
    try:
        # Load the CSV file
        data = pd.read_csv(csv_path)

        # Validate required columns
        required_columns = {"number_regs", "imm/shamt", "Opcode","aqrl/rm"}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")

        # List to store matching ("a", "imm") pairs
        result = []

        # Read the .s file and process line by line
        with open(file_path, 'r') as file:
            for line in file:
                # Extract the first part of the line
                first_part = line.split()[0] if line.split() else None

                if first_part:
                    # Search for the first part in the "opcodes" column
                    matching_row = data.loc[data['Opcode'] == first_part]

                    if not matching_row.empty:
                        # Extract corresponding "number_regs" and "imm" values
                        a_value = matching_row.iloc[0]['number_regs']
                        imm_value = matching_row.iloc[0]['imm/shamt']
                        aq_rm=matching_row.iloc[0]["aqrl/rm"]
                        result.append((a_value, imm_value,aq_rm))

        return result

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'example.s' and 'data.csv' with your file paths
    s_file_path = "spectre/snippet.s"
    csv_file_path = "opcodes.csv"

    matches = read_and_search_assembly(s_file_path, csv_file_path)
    
    # Print the results
    for idx, (a, imm,aq) in enumerate(matches, start=1):
        print(f"Match {idx}: a = {a}, imm = {imm}, aq/rm = {aq}")
