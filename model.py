#model.py
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from geopy.distance import geodesic
from scipy.stats import zscore
import plotly.graph_objects as go
import folium
import random

def load_data(city, store):
    filepath = f'./{city}/{store}.csv'
    df = pd.read_csv(filepath)
    return df

def create_scatter_plot(df, store_location):
    store_df = pd.DataFrame({
        'Landmark Latitude': [store_location[0]],
        'Landmark Longitude': [store_location[1]],
        'Property Type': ['Store Location'],
        'Landmark Name': ['Store']
    })
    df_with_store = pd.concat([df, store_df], ignore_index=True)

    fig = px.scatter(df_with_store, x='Landmark Longitude', y='Landmark Latitude', color='Property Type',
                     hover_data={'Landmark Name': True, 'Landmark Latitude': True, 'Landmark Longitude': True},
                     labels={'Property Type': 'Property Type'},
                     title="Interactive Scatter Plot of Grouped Columns")
    fig.update_layout(xaxis_title="Longitude", yaxis_title="Latitude")
    return fig



def create_hexbin_plot(df, store_location):
    store_df = pd.DataFrame({
        'Landmark Latitude': [store_location[0]],
        'Landmark Longitude': [store_location[1]],
        'Property Type': ['Store Location']
    })
    df_with_store = pd.concat([df, store_df], ignore_index=True)

    fig = go.Figure()

    property_types = df_with_store['Property Type'].unique()
    buttons = []

    fig.add_trace(go.Scatter(
        x=[store_location[1]],  # Longitude
        y=[store_location[0]],  # Latitude
        mode='markers',
        marker=dict(color='red', size=12),
        name='Store Location',
        visible=True
    ))

    for property_type in property_types:
        subset_data = df_with_store[df_with_store['Property Type'] == property_type]
        fig.add_trace(go.Histogram2d(
            x=subset_data['Landmark Longitude'],
            y=subset_data['Landmark Latitude'],
            autobinx=False, autobiny=False,
            xbins=dict(size=0.004), ybins=dict(size=0.008),
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
        title="",
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



def create_kde_plot(df, store_location):
    property_types = df['Property Type'].unique()
    num_rows_kde = (len(property_types) + 1) // 2
    num_cols_kde = 2
    fig_kde, axes_kde = plt.subplots(num_rows_kde, num_cols_kde, figsize=(15, 5*num_rows_kde))
    axes_kde = axes_kde.flatten()

    for i, property_type in enumerate(property_types):
        subset_data = df[df['Property Type'] == property_type]
        distances = [geodesic(store_location, (row['Landmark Latitude'], row['Landmark Longitude'])).kilometers for _, row in subset_data.iterrows()]
        sns.kdeplot(distances, fill=True, cmap='Reds', bw_adjust=0.1, ax=axes_kde[i])
        axes_kde[i].set_title(f'KDE of {property_type} Distance from Store')
        axes_kde[i].set_xlabel('Distance from Store (km)')
        axes_kde[i].set_ylabel('Density')

    plt.tight_layout()
    return fig_kde

def create_hotspot_plot(df):
    property_types = df['Property Type'].unique()
    num_cols_hotspot = 4
    num_rows_hotspot = int(np.ceil(len(property_types) / num_cols_hotspot))
    fig_hotspot = plt.figure(figsize=(18, 14))

    for i, property_type in enumerate(property_types, start=1):
        subset_data = df[df['Property Type'] == property_type]
        distances = subset_data['Distance']
        standardized_distances = zscore(distances)
        hotspots = subset_data[standardized_distances > 0.5]
        coldspots = subset_data[standardized_distances < -0.5]
        plt.subplot(num_rows_hotspot, num_cols_hotspot, i)
        plt.scatter(subset_data['Landmark Longitude'], subset_data['Landmark Latitude'], c='lightgray')
        plt.scatter(hotspots['Landmark Longitude'], hotspots['Landmark Latitude'], c='blue', label='Hotspots')
        plt.scatter(coldspots['Landmark Longitude'], coldspots['Landmark Latitude'], c='red', label='Coldspots')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Hotspot Analysis of {property_type} around Store')
        plt.legend()

    plt.tight_layout()
    return fig_hotspot

def create_boxplot(df):
    data = {
        'Property Type': df['Property Type'],
        'Distance': df['Distance']
    }
    df2 = pd.DataFrame(data)
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Property Type', y='Distance', hue='Property Type', data=df2, palette='Set2', legend=False)
    plt.title('Distance Variation by Property Type')
    plt.xlabel('Property Type')
    plt.ylabel('Distance')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return plt



def get_random_color():
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 
              'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    return random.choice(colors)

def create_folium_map(df, store_location, selected_property_types):
    map_folium = folium.Map(location=store_location, zoom_start=13)
    
    color_mapping = {ptype: get_random_color() for ptype in selected_property_types}
    feature_groups = {ptype: folium.FeatureGroup(name=ptype) for ptype in selected_property_types}
    
    for _, row in df[df['Property Type'].isin(selected_property_types)].iterrows():
        marker = folium.Marker(
            location=[row['Landmark Latitude'], row['Landmark Longitude']],
            popup=row['Landmark Name'],
            icon=folium.Icon(color=color_mapping[row['Property Type']])
        )
        feature_groups[row['Property Type']].add_child(marker)
    
    for fg in feature_groups.values():
        map_folium.add_child(fg)
    
    folium.Marker(
        location=store_location,
        popup='Store Location',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(map_folium)
    
    folium.LayerControl().add_to(map_folium)
    
    return map_folium


def create_competitor_plot(df, store_location):
    # Filter the dataframe for specific landmarks
    landmarks_to_plot = ['Reliance Trends', 'Zudio', 'Westside']
    filtered_df = df[df['Landmark Name'].isin(landmarks_to_plot)]
    
    # Create a new dataframe for the store location
    store_df = pd.DataFrame({
        'Landmark Latitude': [store_location[0]],
        'Landmark Longitude': [store_location[1]],
        'Property Type': ['Store Location'],
        'Landmark Name': ['Store']
    })
    
    # Concatenate the filtered dataframe with the store location dataframe
    df_with_store = pd.concat([filtered_df, store_df], ignore_index=True)

    # Create the scatter plot
    fig = px.scatter(df_with_store, x='Landmark Longitude', y='Landmark Latitude', color='Property Type',
                     hover_data={'Landmark Name': True, 'Landmark Latitude': True, 'Landmark Longitude': True},
                     labels={'Property Type': 'Property Type'},
                     title="Interactive Scatter Plot of Grouped Columns")
    fig.update_layout(xaxis_title="Longitude", yaxis_title="Latitude")
    return fig

def pie_chart(df):
    property_counts = df['Property Type'].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(property_counts, labels=property_counts.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribution of Property Types')
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
    return fig
