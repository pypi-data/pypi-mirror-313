import argparse
import os
from mbSTATS.data_preparation import load_csv_data
from mbSTATS.final_df_prep import create_summary_dataframe
from mbSTATS.normalization_methods.pqn_normalization import pqn_normalization
from mbSTATS.plots_samples.pca_analysis import perform_pca
from mbSTATS.plots_samples.hca_analysis import perform_hca
from mbSTATS.plots_samples.correlation_analysis import plot_correlation_matrix_samples
from mbSTATS.plots_samples.pls_da import pls_da_plot
from mbSTATS.plots_compounds.hca_analysis import plot_hca
from mbSTATS.plots_compounds.pca_analysis import plot_pca
from mbSTATS.plots_compounds.correlation_matrix import plot_correlation_matrix
from mbSTATS.plots_compounds.volcano import plot_volcano
from mbSTATS.plots_compounds.rf_feature_imp import rf_features
from mbSTATS.plots_compounds.heatmap_comp_v_samp import generate_heatmap
from mbSTATS.plots_compounds.violin_plot import plot_violin
from mbSTATS.plots_compounds.grp_avg import plot_grp_avg
from mbSTATS.plots_compounds.comp_density import plot_density

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run metabolomics analysis with mbSTATS")
    parser.add_argument('-f', '--folders', type=str, nargs='+', required=True, help="Folders containing data")
    parser.add_argument('-o', '--output', type=str, required=True, help="Folder to save the output plots")
    
    # Parse arguments
    args = parser.parse_args()

    # Prepare data by loading CSV files
    column_names = ["Start_Time", "End_Time", "Retention_Time", "Ion_Mode", 
                    "Intensity", "Area_Percentage", "Adjusted_Intensity", 
                    "Adjusted_Area_Percentage", "Peak_Width", "Flag", 
                    "Compound_Name", "CAS_Number", "Similarity_Score"]
    
    dataframes = load_csv_data(args.folders, column_names)
    print("Dataframes loaded:", list(dataframes.keys()))
    
    # Create summary dataframe
    summary_df, compound_to_code = create_summary_dataframe(dataframes)
    print("Summary DataFrame:")
    print(summary_df)
    
    print("Compounds to code:")
    print(compound_to_code)
    
    # Perform normalization
    pqn_normalized_df = pqn_normalization(summary_df)
    print("Normalization complete.")

    # Perform PCA and save the plot
    perform_pca(pqn_normalized_df, args.output)

    # Perform other analyses and save plots
    perform_hca(pqn_normalized_df, args.output)
    plot_correlation_matrix_samples(pqn_normalized_df, args.output)
    pls_da_plot(pqn_normalized_df, args.output)
    
    # Compound level analyses
    plot_hca(summary_df, args.output)
    plot_pca(summary_df, args.output)
    plot_correlation_matrix(summary_df, args.output)
    plot_volcano(summary_df, args.output)
    rf_features(summary_df, args.output)
    generate_heatmap(summary_df, args.output)
    plot_violin(summary_df, args.output)
    plot_grp_avg(summary_df, args.output)
    plot_density(summary_df, args.output)

    print(f"Analysis complete. Plots saved in {args.output}")

if __name__ == "__main__":
    main()
