import pandas as pd
import folium
import plotly.graph_objects as go
import random
import plotly.express as px

def load_store_locations(file_path='Store_Info_Latitude_Longitude.xlsx'):
    df = pd.read_excel(file_path)
    df = df[df['Town_x'].isin(['Bengaluru', 'Mysore'])]
    return df

def create_store_map(file_path='Store_Info_Latitude_Longitude.xlsx'):
    df = pd.read_excel(file_path)

    if not df.empty:
        map_center = [df['Latitude_x'].iloc[0], df['Longitude_x'].iloc[0]]
    else:
        map_center = [12.9716, 77.5946]  # Default to Bangalore's coordinates

    store_map = folium.Map(location=map_center, zoom_start=12)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude_x'], row['Longitude_x']],
            icon=folium.Icon(icon='info-sign')
        ).add_to(store_map)

    return store_map

def create_hexbin_plot(file_path):
    file_path=file_path.replace('expansion\\', 'locations\\')

    df = pd.read_csv(file_path)

    property_types = df['Property Type'].unique()
    buttons = []

    fig = go.Figure()

    for property_type in property_types:
        subset_data = df[df['Property Type'] == property_type]
        fig.add_trace(go.Histogram2d(
            x=subset_data['longitude'],
            y=subset_data['latitude'],
            autobinx=False, autobiny=False,
            xbins=dict(size=0.0004), ybins=dict(size=0.0008),
            name=property_type,
            opacity=0.6,
            visible=False  # Default visibility is False
        ))
        buttons.append(
            {
                'method': 'update',
                'label': property_type,
                'args': [{'visible': [True] + [property_type == t for t in property_types]}]
            }
        )

    fig.update_layout(
        title="Hexbin Plot",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        updatemenus=[
            {
                'buttons': buttons,
                'direction': 'down',
                'showactive': True,
            },
        ]
    )

    return fig

def get_random_color():
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 
              'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    return random.choice(colors)

def create_folium_map(filepath):
    filepath = filepath.replace('expansion\\', 'locations\\')
    df = pd.read_csv(filepath)
    
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    store_location = [center_lat, center_lon]

    unique_property_types = df['Property Type'].unique()
    
    map_folium = folium.Map(location=store_location, zoom_start=13)
    
    color_mapping = {ptype: get_random_color() for ptype in unique_property_types}
    feature_groups = {ptype: folium.FeatureGroup(name=ptype, show=(ptype == 'default_property_type')) for ptype in unique_property_types}
    
    default_property_type = 'transportation'  # Replace with your default property type

    for _, row in df.iterrows():
        marker = folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['name'],
            icon=folium.Icon(color=color_mapping[row['Property Type']])
        )
        feature_groups[row['Property Type']].add_child(marker)

    for fg in feature_groups.values():
        map_folium.add_child(fg)

    folium.LayerControl().add_to(map_folium)

    return map_folium

def create_competitor_plot(filepath):
    filepath=filepath.replace('expansion\\', 'locations\\')
    df = pd.read_csv(filepath)

    # Filter the dataframe for specific landmarks
    landmarks_to_plot = ['Reliance Trends', 'Zudio', 'Westside']
    filtered_df = df[df['name'].isin(landmarks_to_plot)]
    
    # Create the scatter plot
    fig = px.scatter(filtered_df, x='longitude', y='latitude', color='Property Type',
                     hover_data={'name': True, 'latitude': True, 'longitude': True},
                     labels={'Property Type': 'Property Type'},
                     title="Interactive Scatter Plot of Grouped Columns")
    fig.update_layout(xaxis_title="Longitude", yaxis_title="Latitude")
    return fig
