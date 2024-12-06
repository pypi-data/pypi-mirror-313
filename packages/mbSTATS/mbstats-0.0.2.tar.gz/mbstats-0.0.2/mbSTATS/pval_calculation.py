import pandas as pd
from scipy.stats import ttest_ind

def calculate_p_values(df):
    """
    Calculates p-values for each compound between overexpressed (oe) and wild-type (wt) samples.

    Parameters:
    df (pd.DataFrame): A DataFrame with a 'sample' column identifying 'oe' and 'wt' samples
                       and additional columns for compound values.

    Returns:
    pd.DataFrame: A DataFrame with compounds and their corresponding p-values.
    """
    # Identify the overexpressed (oe) and wild-type (wt) sample rows
    oe_rows = df[df['sample'].str.startswith('oe')]
    wt_rows = df[df['sample'].str.startswith('wt')]
    
    # Create an empty dictionary to store the p-values for each compound
    p_values = {}

    # Iterate over each compound (column) except the first one (sample names)
    for compound in df.columns[1:]:
        # Extract overexpressed and wild-type values for the current compound
        oe_values = oe_rows[compound].values
        wt_values = wt_rows[compound].values
        
        # Perform a two-sample t-test (independent, unequal variance)
        t_stat, p_val = ttest_ind(oe_values, wt_values, equal_var=False)
        
        # Store the p-value in the dictionary
        p_values[compound] = p_val

    # Convert p-values dictionary to a DataFrame for easy viewing
    p_values_df = pd.DataFrame(list(p_values.items()), columns=['Compound', 'p-value'])
    
    return p_values_df
