import pandas as pd

def create_summary_dataframe(dataframes, required_columns=["Compound_Name", "Area_Percentage"]):
    # Step 1: Identify common compounds across all DataFrames
    common_compounds = set(dataframes['wt_wt1_1']['Compound_Name'])  # Starting from one of the dataframes, e.g., wt_wt1_1
    for df in dataframes.values():
        common_compounds.intersection_update(set(df['Compound_Name']))

    # Step 2: Create a compound-to-code mapping
    compound_to_code = {compound: f"c{i+1}" for i, compound in enumerate(sorted(common_compounds))}

    # Step 3: Create the new summary DataFrame
    data = []

    # Define a function to extract data for each sample
    def extract_values(df, sample_name):
        values = {'sample': sample_name}
        for compound, code in compound_to_code.items():
            # Use Area_Percentage or any specific metric from the original DataFrame
            value = df.loc[df['Compound_Name'] == compound, 'Area_Percentage'].values
            values[code] = value[0] if len(value) > 0 else None
        return values

    # Gather data from each DataFrame for the summary DataFrame
    for sample_name, df in dataframes.items():
        data.append(extract_values(df, sample_name))

    # Create the summary DataFrame
    summary_df = pd.DataFrame(data)

    return summary_df, compound_to_code

# Example usage
# folders = ["/home/satvik/Thesis/csv/wt", "/home/satvik/Thesis/csv/oe", "/home/satvik/Thesis/csv/oe2"]
# column_names = [
#     "Start_Time", "End_Time", "Retention_Time", "Ion_Mode", 
#     "Intensity", "Area_Percentage", "Adjusted_Intensity", 
#     "Adjusted_Area_Percentage", "Peak_Width", "Flag", 
#     "Compound_Name", "CAS_Number", "Similarity_Score"
# ]

# # Load the dataframes using the previous code
# try:
#     dataframes = load_csv_data(folders, column_names)
    
#     # Create the summary DataFrame
#     summary_df = create_summary_dataframe(dataframes)
    
#     # Display the summary DataFrame
#     print(summary_df)

# except (FileNotFoundError, ValueError) as e:
#     print(f"Error: {e}")
