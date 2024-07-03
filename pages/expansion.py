import streamlit as st
import sys
import os
import pandas as pd
from streamlit_folium import folium_static
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to sys.path to import helper functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helper import create_store_map, create_hexbin_plot, create_folium_map, create_competitor_plot

def render():
    st.title("Expansion Analysis")

    st.write("Store locations on the map:")
    store_map = create_store_map()
    folium_static(store_map)

    # Get list of CSV files in the directory
    expansion_files = [f for f in os.listdir('locations') if f.endswith('_expansion_areas.csv')]

    if not expansion_files:
        st.error("No expansion area files found.")
        return

    # Create a dropdown to select a CSV file
    selected_file = st.selectbox("Select Expansion Area File", expansion_files)

    if selected_file:
        file_path = os.path.join('locations', selected_file)

        hexbin_plot = create_hexbin_plot(file_path)
        st.plotly_chart(hexbin_plot)

        folium_plot = create_folium_map(file_path)
        folium_static(folium_plot)
        
        comp_plot = create_competitor_plot(file_path)
        st.plotly_chart(comp_plot)


        # Read and display the CSV file
        df = pd.read_csv(file_path)
        st.write("CSV File Contents:")
        st.dataframe(df)

if __name__ == "__main__":
    render()