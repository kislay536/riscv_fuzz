import pandas as pd

def process_files(simul_output_file, terminal_output_file, stats_data_file):
    # Load the stats_data.csv into a pandas DataFrame
    df = pd.read_csv(stats_data_file)

    # Add "Spectre out" and "Error" columns if not present
    if "Spectre out" not in df.columns:
        df["Spectre out"] = ""
    if "Error" not in df.columns:
        df["Error"] = ""

    # Read simul_output.txt file
    with open(simul_output_file, "r") as simul_file:
        simul_lines = simul_file.readlines()

    # Read terminal_output.txt file
    with open(terminal_output_file, "r") as terminal_file:
        terminal_lines = terminal_file.readlines()

    # Find Regions of Interest (RoIs) in simul_output.txt
    roi_start_indices = [i for i, line in enumerate(simul_lines) if "**** REAL SIMULATION ****" in line]
    roi_end_indices = [i for i, line in enumerate(simul_lines) if "***************" in line]

    # Ensure the number of start and end indices are equal
    if len(roi_start_indices) != len(roi_end_indices):
        raise ValueError("Mismatch in the number of ROI start and end markers.")

    # Process each RoI pair
    for start, end in zip(roi_start_indices, roi_end_indices):
        roi_lines = simul_lines[start + 1:end]

        # Check for strings in RoI
        stopping_fetch_found = any("stopping fetch" in line for line in roi_lines)
        terminal_attach_found = any("system.platform.terminal: attach terminal" in line for line in roi_lines)
        m5_exit_found = any("m5_exit instruction" in line for line in roi_lines)

        # Find the last line containing "Data for"
        last_data_line = next((line for line in reversed(roi_lines) if "Data for" in line), None)
        if last_data_line:
            name = last_data_line.split("Data for")[-1].strip().split()[0]  # Extract the name

            # Update the corresponding row in the DataFrame
            if name in df["name"].values:
                row_index = df[df["name"] == name].index[0]

                # Update "Error" column
                if stopping_fetch_found:
                    df.at[row_index, "Error"] = "Address issue"
                elif m5_exit_found:
                    df.at[row_index, "Error"] = "m5exit"
                else:
                    df.at[row_index, "Error"] = "other issue"

    # Process rows in the DataFrame for "Spectre out" column
    terminal_output_array = []
    for i, line in enumerate(terminal_lines):
        if "m5 terminal" in line:
            next_line_index = i + 1
            if next_line_index < len(terminal_lines):
                terminal_output_array.append(terminal_lines[next_line_index].strip())

    # Update DataFrame with terminal output array
    for index, value in enumerate(terminal_output_array):
        if index < len(df):
            df.at[index, "Spectre out"] = value

    # Save the updated DataFrame back to the same file
    df.to_csv(stats_data_file, index=False)

def update_spectre_out_column(stats_data_file):
    # Load the stats_data.csv into a pandas DataFrame
    df = pd.read_csv(stats_data_file)

    # Iterate over rows and update "Spectre out" column
    for index, row in df.iterrows():
        spectre_value = row["Spectre out"]
        if "BOOM!" in spectre_value:
            df.at[index, "Spectre out"] = "BOOM!"
        elif "BOOM" in spectre_value:
            df.at[index, "Spectre out"] = "BOOM"
        elif "BOO" in spectre_value:
            df.at[index, "Spectre out"] = "BOO"
        elif "BO" in spectre_value:
            df.at[index, "Spectre out"] = "BO"
        elif "B" in spectre_value:
            df.at[index, "Spectre out"] = "B"
        else:
            df.at[index, "Spectre out"] = "No Output"

    # Save the updated DataFrame back to the same file
    df.to_csv(stats_data_file, index=False)

# Example usage
process_files("simul_output.txt", "terminal_output.txt", "stats_data.csv")
update_spectre_out_column("stats_data.csv")
