import pandas as pd
import re
from pyproj import Transformer
import folium
import streamlit as st

# Load the main CSV data
@st.cache_data
def load_data():
    df = pd.read_csv("data/PlotDataHeleWeek.csv")
    stations = pd.read_csv("data/Randstad.csv")
    return df, stations

# Extract coordinates function
def extract_coords(geometry_str):
    coords = re.findall(r'(-?\d+\.\d+)\s(-?\d+\.\d+)', geometry_str)
    return [tuple(map(float, coord)) for coord in coords]

# Precompute data processing for lines
@st.cache_data
def process_line_data(df):
    df['coords'] = df['geometry'].apply(extract_coords)
    df['color_hex'] = df['color'].apply(lambda rgb: f'#{int(eval(rgb)[0]*255):02x}{int(eval(rgb)[1]*255):02x}{int(eval(rgb)[2]*255):02x}')
    transformer = Transformer.from_crs("epsg:32631", "epsg:4326")
    
    def convert_coords_to_latlon(coords):
        x_vals, y_vals = zip(*coords)
        lat_vals, lon_vals = transformer.transform(x_vals, y_vals)
        return list(zip(lat_vals, lon_vals))
    
    df['latlon_coords'] = df['coords'].apply(convert_coords_to_latlon)
    return df

# Efficiently plot lines and stations
@st.cache_data
def draw_map(df, initial_center, initial_zoom):
    # Use initial center and zoom level to keep map state
    m = folium.Map(location=initial_center, zoom_start=initial_zoom, control_scale=True, tiles='CartoDB positron')
    
    # Add the polyline for the train lines
    for _, row in df.iterrows():
        latlon_coords = row['latlon_coords']
        color_hex = row['color_hex']
        folium.PolyLine(latlon_coords, color=color_hex, weight=2.5, opacity=1).add_to(m)
    
    return m

# Add station markers based on selection
def add_stations_to_map(m, stations, selected_types):
    for _, row in stations.iterrows():
        if row['Randstad'] in selected_types:
            color = 'blue' if row['Randstad'] == 0.0 else 'red'
            folium.CircleMarker(
                location=[row['Lat-coord'], row['Lng-coord']],
                radius=1,  
                color=color,
                fill=True,
                fill_opacity=1,
                popup=row['Station']
            ).add_to(m)
    return m

# Main function for Streamlit
def main():
    st.title("Streamlit Map with Selectable Station Types")

    # Load and process data
    df, stations = load_data()
    df = process_line_data(df)

    # Get the initial map center and zoom level from the first coordinates
    initial_center = df['latlon_coords'][0][0]  # First coordinate
    initial_zoom = 7

    # Sidebar selection for station types
    station_type = st.multiselect(
        "Select station types to display:",
        options=[0.0, 1.0],
        format_func=lambda x: "Randstad" if x == 0.0 else "Non-Randstad",
        default=[]
    )

    # Draw the Folium map for the lines
    folium_map = draw_map(df, initial_center, initial_zoom)

    # Add selected station types to the map (if any)
    if station_type:
        folium_map = add_stations_to_map(folium_map, stations, station_type)

    # Display the map in Streamlit
    st.components.v1.html(folium_map._repr_html_(), height=600)

# Run the app
if __name__ == "__main__":
    main()
