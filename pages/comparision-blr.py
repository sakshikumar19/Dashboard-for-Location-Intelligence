import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Import seaborn for color palettes

def render():
    st.title("Comparative Analysis for Bangalore")

    def count_property_types(directory):
        property_counts = {}

        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                # Strip the .csv extension from the filename
                area_name = filename[:-4]
                filepath = os.path.join(directory, filename)
                df = pd.read_csv(filepath)
                counts = df['Property Type'].value_counts()
                property_counts[area_name] = counts
        return property_counts

    def create_comparison_df(property_counts):
        comparison_df = pd.DataFrame(property_counts).fillna(0)
        return comparison_df

    def plot_separate_analysis(comparison_df):
        # Define a soft color palette with three complementary colors
        soft_colors = sns.color_palette("pastel", 3)

        for property_type in comparison_df.index:
            fig, ax = plt.subplots(figsize=(10, 6))
            comparison_df.loc[property_type].plot(kind='bar', ax=ax, color=soft_colors)
            ax.set_title(f'Comparative Analysis for {property_type}')
            ax.set_xlabel('Area')
            ax.set_ylabel('Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

    def main():
        # Static directory path
        directory = './blr'

        # Step 1: Count unique property types in each CSV file
        property_counts = count_property_types(directory)

        if property_counts:
            # Step 2: Create a DataFrame for comparison
            comparison_df = create_comparison_df(property_counts)

            # Step 3: Plot separate analysis for each property type
            plot_separate_analysis(comparison_df)
        else:
            st.warning("No CSV files found in the directory.")

    main()

if __name__ == "__main__":
    render()
