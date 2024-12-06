import pandas as pd
import glob
import re
import os

def load_csv_data(folders, column_names, required_columns=["Compound_Name", "Area_Percentage"]):
    """
    Loads CSV data from specified folders and assigns dataframes to variables based on filenames.
    Raises an error if folders are empty or required columns are missing.

    Parameters:
    - folders (list of str): List of folder paths to load CSV files from.
    - column_names (list of str): List of column names for the CSV files.
    - required_columns (list of str): Columns required to be present in each CSV file.

    Returns:
    - dict: Dictionary where keys are dataframe names based on filenames, 
            and values are the corresponding dataframes.
    """
    dataframes = {}

    # Define regex to capture the relevant parts of the filenames
    pattern = re.compile(r".*/(wt|oe|oe2)/(\w+_\d).csv")

    for folder in folders:
        csv_files = glob.glob(f"{folder}/*.csv")
        
        # Check if the folder is empty
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in folder: {folder}")

        for file in csv_files:
            match = pattern.match(file)
            if match:
                # Extract parts from the filename to create the key
                group, sample = match.groups()
                df_name = f"{group}_{sample}"  # e.g., "wt_wt1_1" -> "wt1_1"
                
                # Read the CSV file and assign column names
                df = pd.read_csv(file, names=column_names, header=0)

                # Check if required columns are present
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    raise ValueError(f"File {file} is missing required columns: {', '.join(missing_columns)}")

                dataframes[df_name] = df
            else:
                print(f"File {file} did not match expected pattern")

    return dataframes

# Example usage
folders = ["/home/satvik/Thesis/csv/wt", "/home/satvik/Thesis/csv/oe", "/home/satvik/Thesis/csv/oe2"]
column_names = [
    "Start_Time", "End_Time", "Retention_Time", "Ion_Mode", 
    "Intensity", "Area_Percentage", "Adjusted_Intensity", 
    "Adjusted_Area_Percentage", "Peak_Width", "Flag", 
    "Compound_Name", "CAS_Number", "Similarity_Score"
]

try:
    dataframes = load_csv_data(folders, column_names)
    # Access specific dataframes by name as before
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")
