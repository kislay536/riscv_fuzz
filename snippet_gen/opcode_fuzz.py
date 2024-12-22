import os
import pandas as pd
import numpy as np

def fuzz(file_path_threshold, file_path_additional, file_path_s, directory, iteration):

    # Define the directory containing the CSV files
    csv_directory = 'snippet_gen/opcodes/'
    # Create an empty dictionary to store the DataFrames
    dataframes = {}

    # Loop over the range 'A' to 'J' (which are the filenames)
    for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
        # Define the file path
        file_path = os.path.join(csv_directory, f'{letter}.csv')
        
        # Check if the file exists and then read it into a DataFrame
        if os.path.exists(file_path):
            dataframes[letter] = pd.read_csv(file_path)
        else:
            print(f"File {file_path} does not exist")

    # Define a dictionary for 'Type' values mapping
    my_dict = {
        'A': 4,
        'B': 3,
        'C': 41,
        'D': 2,
        'E': 20,
        'F': 7,
        'G': 44,
        'H': 20,
        'I': 8,
        'J': 8
    }
    
    # Load the threshold CSV file
    df_threshold = pd.read_csv(file_path_threshold)
    threshold_array = df_threshold['threshold'].to_numpy()  # Convert to NumPy array

    # Load the additional CSV file
    df_additional = pd.read_csv(file_path_additional)

    # Read the .s file and determine the number of lines
    with open(file_path_s, 'r') as f:
        lines = f.readlines()

    num_lines = len(lines)

    # Ensure the arrays are the same length
    if len(threshold_array) != num_lines:
        raise ValueError("The number of lines in the .s file must match the number of threshold values")

    # Extract the first string from each line before the first white space
    first_strings = np.array([line.split()[0] for line in lines])

    # Create a new array to store the Type values
    types_array = []

    # For each element in first_strings, find the corresponding Type in the additional CSV
    for first_string in first_strings:
        matched_row = df_additional[df_additional['Opcode'] == first_string]
        if not matched_row.empty:
            types_array.append(matched_row['Type'].values[0])
        else:
            types_array.append(None)  # If no match is found, append None or a suitable default value

    # Convert types_array to a NumPy array
    types_array = np.array(types_array)
    values_array = np.array([my_dict[key] for key in types_array])


    # Check if fuzz.csv exists in the directory
    fuzz_file_path = os.path.join(directory, 'fuzz.csv')

    # Initialize the 2D array to store results
    results_array = np.empty((0, len(first_strings)), dtype=object)

    # Loop for iterations
    for i in range(iteration):
        # Generate random integers and compare with threshold values
        random_integers = np.random.randint(0, 101, size=num_lines)
        result_array = np.where(random_integers > threshold_array, 1, 0)
        random_array = np.array([np.random.randint(1, val + 1) for val in values_array])
        prob_array = random_array * result_array
        print(prob_array)
        
        # Create the new array with characters and corresponding numbers (or 0 if the number is zero)
        mul_array = np.array([f"{types_array[i]}{prob_array[i]}" if prob_array[i] != 0 else "0" for i in range(len(types_array))])

        # Initialize a new array to store the resulting values
        new_array = []

        # Loop through each element in the arrays
        for i in range(len(first_strings)):
            type_char = types_array[i]  # Get the corresponding type character (e.g., 'C')
            mul_str = mul_array[i]  # Get the corresponding value from mul_array (e.g., 'C11')
            first_str = first_strings[i]  # Get the corresponding first string (e.g., 'string1')

            if mul_str == '0':
                # If mul_array element is '0', copy the string from first_strings
                new_array.append(first_str)
            else:
                # Find the corresponding dataframe
                df = dataframes.get(type_char)
                if df is not None:
                    # Look for the row where "Type" matches mul_array element
                    matching_row = df[df['Type'] == mul_str]
                    if not matching_row.empty:
                        # Find the value in the "Opcode" column and append it to new_array
                        opcode_value = matching_row['Opcode'].values[0]
                        new_array.append(opcode_value)
                    else:
                        # If no match found, append the first string
                        new_array.append(first_str)
                else:
                    # If no dataframe for the type, append the first string
                    new_array.append(first_str)

        # Append new_array to the results_array
        results_array = np.vstack([results_array, new_array])

        # Check if results_array has reached 100,000 rows
        if results_array.shape[0] >= 100000:
            # Export to CSV
            if os.path.exists(fuzz_file_path):
                mode = 'a'  # Append mode
            else:
                mode = 'w'  # Write mode (create a new file)

            # Write to CSV
            df_results = pd.DataFrame(results_array)
            df_results.to_csv(fuzz_file_path, mode=mode, header=not os.path.exists(fuzz_file_path), index=False)

            # Reset results_array to avoid memory overload
            results_array = np.empty((0, len(first_strings)), dtype=object)

    # After all iterations, write the remaining data to the CSV file
    if results_array.shape[0] > 0:
        df_results = pd.DataFrame(results_array)
        df_results.to_csv(fuzz_file_path, mode='a', header=not os.path.exists(fuzz_file_path), index=False)

    print(f"Results exported to {fuzz_file_path}")

# Call the function with appropriate paths
print(fuzz("snippet_gen/threshold.csv", "snippet_gen/opcodes.csv", "snippet_gen/snippet.s", "snippet_gen/", 10000000))
