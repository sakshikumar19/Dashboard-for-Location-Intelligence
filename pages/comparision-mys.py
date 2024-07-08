import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Import seaborn for color palettes

def render():
    st.title("Comparative Analysis for Mysore")

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

    def count_competitor_landmarks(directory, competitors):
        competitor_counts = {}

        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                area_name = filename[:-4]
                filepath = os.path.join(directory, filename)
                df = pd.read_csv(filepath)
                
                # Filter for competitor landmarks and count them
                counts = df['Landmark Name'].value_counts()
                filtered_counts = counts[counts.index.isin(competitors)]
                competitor_counts[area_name] = filtered_counts

        return competitor_counts

    def create_comparison_df(property_counts):
        comparison_df = pd.DataFrame(property_counts).fillna(0)
        return comparison_df

    def create_competitor_comparison_df(competitor_counts):
        competitor_df = pd.DataFrame(competitor_counts).fillna(0).T
        return competitor_df

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
    
    def plot_competitor_analysis(competitor_df):
        fig, ax = plt.subplots(figsize=(10, 6))
        competitor_df.plot(kind='bar', stacked=True, ax=ax, color=['skyblue', 'lightgreen', 'salmon'])
        ax.set_title('Number of Competitor Landmarks')
        ax.set_xlabel('Store')
        ax.set_ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    def main():
        # Static directory path
        directory = './mys'
        competitors = ['Reliance Trends', 'Westside', 'Zudio']

        property_counts = count_property_types(directory)

        competitor_counts = count_competitor_landmarks(directory, competitors)
        
        if competitor_counts:
            competitor_df = create_competitor_comparison_df(competitor_counts)
            plot_competitor_analysis(competitor_df)
        else:
            st.warning("No competitor landmarks found in the directory.")

        if property_counts:
            comparison_df = create_comparison_df(property_counts)
            plot_separate_analysis(comparison_df)
        else:
            st.warning("No CSV files found in the directory.")

    main()

if __name__ == "__main__":
    render()
