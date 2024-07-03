import streamlit as st
import pandas as pd
import model
from streamlit_folium import folium_static
import os

# Cache loading of data
@st.cache_data
def load_data(city_dir, store):
    return model.load_data(city_dir, store)

# Define directories and load initial data
city_directories = {'Bangalore': 'blr', 'Mysore': 'mys'}
stores_df = pd.read_excel('Store_Info_Latitude_Longitude.xlsx')
stores_df = stores_df[stores_df['Town_x'].isin(['Bengaluru', 'Mysore'])]

page = st.query_params.get('page', [''])[0]

if page == 'expansion':
    # Import and call the expansion page content
    from pages import expansion
    expansion.render()  # assuming your expansion.py has a render function
else:
    st.title("Store Location Analysis Dashboard")

# Main interface for store location analysis
city = st.selectbox("Select City", list(city_directories.keys()))
if city:
    city_dir = city_directories[city]
    store_files = [f.split('.')[0] for f in os.listdir(f'./{city_dir}') if f.endswith('.csv')]
    store = st.selectbox("Select Store", store_files)

    if store:
        df = load_data(city_dir, store)
        st.header(f"Data for Store Code: {store} in {city}")
        store_int = int(store)
        store_row = stores_df[stores_df['StoreCode_x'] == store_int]
        if not store_row.empty:
            store_row = store_row.iloc[0]
            store_location = (store_row['Latitude_x'], store_row['Longitude_x'])

            st.markdown("#### 1. Hexbin Plot")
            st.write("It shows the distribution of property types around the store location. The color intensity represents the density of data points.")
            st.write("Select the property type you want to view from the drop-down menu.")

            hexbin_plot = model.create_hexbin_plot(df, store_location)
            st.plotly_chart(hexbin_plot)

            # kde_plot = model.create_kde_plot(df, store_location)
            # st.pyplot(kde_plot)

            st.markdown("#### 2. Hotspot Plot")
            st.write("This plot highlights the areas with the highest concentration of data points for different property types.")

            hotspot_plot = model.create_hotspot_plot(df)
            st.pyplot(hotspot_plot)

            # boxplot = model.create_boxplot(df)
            # st.pyplot(boxplot)

            property_types = df['Property Type'].unique()

            # Create a horizontal container with map and property type selector
            col1, col2 = st.columns([3, 1])

            with col2:
                selected_property_types = st.multiselect(
                    "Select Property Types to Display",
                    options=property_types,
                    default=[property_types[0]]
                )

            with col1:
                st.markdown("#### 3. Property Type Map")
                st.write("This map shows the locations of different property types around the store.")
                st.write("Select the property type you want to view from the drop-down menu.")

                if selected_property_types:
                    folium_map = model.create_folium_map(df, store_location, selected_property_types)
                    folium_static(folium_map)
            
            
            st.markdown("#### 4. Scatter Plot")
            st.write("This plot shows the distribution of data points around the store location.")
            st.write("Double click on the legend to isolate property types.")


            scatter_plot = model.create_scatter_plot(df, store_location)
            st.plotly_chart(scatter_plot)

            st.markdown("#### 5. Competitor Plot")
            st.write("Hover over datapoints to see the competitor store names")

            competitor_plot = model.create_competitor_plot(df, store_location)
            st.plotly_chart(competitor_plot)
            
            pie = model.pie_chart(df)
            st.pyplot(pie)

        else:
            st.error(f"Store code {store} not found.")
        
