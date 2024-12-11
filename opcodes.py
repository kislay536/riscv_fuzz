import pandas as pd
import re

# Define a function to process the .txt file and convert to a DataFrame
def process_riscv_opcodes(input_file):
    # Define the column names
    columns = ["Extension", "Opcode", "rd", "rs1", "rs2", "rs3", "imm", "shamt", "pred", "succ", "aqrl", "rm"]
    
    # Initialize an empty list to store rows of data
    rows = []
    
    # Open the input file and process line by line
    with open(input_file, 'r') as file:
        extension = ''
        for line in file:
            # Strip any leading/trailing whitespace
            line = line.strip()

            # Check if the line defines a new extension (e.g., #RV64I)
            extension_match = re.match(r"#RV\w+([A-Z])", line)
            if extension_match:
                # If a new extension is found, update the extension variable
                extension = extension_match.group(1)
                continue  # Skip this line, as it doesn't contain an opcode

            # If the line contains an opcode, process it
            if line:
                row = [extension]  # Start the row with the current extension
                
                # Initialize all columns as empty
                fields = {col: '' for col in columns[1:]}  
                
                # Extract the first word before the first space as the Opcode
                fields["Opcode"] = line.split()[0]  # Get the first word (opcode)
                
                # Check for specific columns in the line and update them if found
                for col in fields:
                    if col in line:
                        fields[col] = col  # Replace with column name if found

                # Append the row to the rows list
                rows.append([extension] + list(fields.values()))
    
    # Convert the rows into a DataFrame
    df = pd.DataFrame(rows, columns=columns)
    
    # Export the DataFrame to a CSV file
    df.to_csv('opcodes.csv', index=False)
    print("CSV file 'opcodes.csv' has been created.")

# Call the function with your input file name
input_file = 'opcodes.txt'  # Replace this with the path to your input file
process_riscv_opcodes(input_file)
