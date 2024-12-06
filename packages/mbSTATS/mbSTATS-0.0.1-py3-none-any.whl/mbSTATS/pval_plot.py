import matplotlib.pyplot as plt

def plot_p_values(p_values_df, th):
    """
    Plots p-values for each compound with a significance threshold line.

    Parameters:
    p_values_df (pd.DataFrame): DataFrame containing 'Compound' and 'p-value' columns.
    th (float): The threshold for significance, e.g., 0.05.
    """
    # Extract compounds and p-values for easy plotting
    compounds = p_values_df['Compound']
    p_values = p_values_df['p-value']
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(compounds, p_values, color='skyblue')
    
    # Add a threshold line for p-value significance
    plt.axhline(y=th, color='red', linestyle='--', label=f'Significance Threshold (p = {th})')
    
    # Labels and title
    plt.xlabel('Compound')
    plt.ylabel('p-value')
    plt.title('P-Values for Each Compound')
    plt.xticks(rotation=45)
    plt.legend()
    
    # Display plot
    plt.show()
