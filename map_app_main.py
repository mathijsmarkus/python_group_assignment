import pandas as pd
import re
from pyproj import Transformer
import folium
import streamlit as st

# Load the CSV data for multiple line sets
@st.cache_data
def load_data():
    # Load multiple datasets
    df_hele_week = pd.read_csv("Streamlit_data/PlotDataHeleWeek.csv")
    df_other_set_1 = pd.read_csv("Streamlit_data/PlotData2024-10-07.csv")  # Add your other datasets here
    df_other_set_2 = pd.read_csv("Streamlit_data/PlotData2024-10-07 - kopie.csv")
    stations = pd.read_csv("Streamlit_data/Randstad-0.csv")
    return df_hele_week, df_other_set_1, df_other_set_2, stations

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
def draw_map(initial_center, initial_zoom):
    # Use initial center and zoom level to keep map state
    m = folium.Map(location=initial_center, zoom_start=initial_zoom, control_scale=True, tiles='CartoDB positron')
    return m

# Add lines to the map
def add_lines_to_map(m, df):
    for _, row in df.iterrows():
        latlon_coords = row['latlon_coords']
        color_hex = row['color_hex']
        folium.PolyLine(latlon_coords, color=color_hex, weight=2.5, opacity=1).add_to(m)
    return m

# Add station markers based on selection
def add_stations_to_map(m, stations, selected_types):
    for _, row in stations.iterrows():
        if row['Randstad'] in selected_types:
            color = '#bbbfb5' if row['Randstad'] == 0.0 else '#868a81'
           
            # Add a visible small marker
            folium.CircleMarker(
                location=[row['Lat-coord'], row['Lng-coord']],
                radius=1,  # Keep the bullet size small
                color=color,
                fill=True,
                fill_opacity=1,
                popup=row['Station'],  # Show station name on click
                tooltip=row['Station']  # Show station name on hover
            ).add_to(m)
            
            # Add an invisible, larger clickable area to make selection easier
            folium.CircleMarker(
                location=[row['Lat-coord'], row['Lng-coord']],
                radius=8,  # Larger radius for easier selection
                color=color,
                fill=True,
                fill_opacity=0,  # Make the clickable area invisible
                popup=row['Station'],
                weight=0  # No border for a seamless look
            ).add_to(m)
    
    return m

# Add legend to the map
def add_legend(m):
    legend_html = """
    <div style="position: fixed; 
                top: 10px; 
                right: 10px; 
                width: 150px; 
                height: auto; 
                background-color: white; 
                border: 2px solid grey; 
                z-index:9999; 
                padding: 10px;">
        <h4 style="margin: 0; text-align: center;">Station Legend</h4>
        <i style="background: #bbbfb5; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></i> Non-Randstad<br>
        <i style="background: #868a81; width: 20px; height: 20px; display: inline-block; border-radius: 50%;"></i> Randstad<br>
    </div>
    """
    # Add the HTML legend to the map using the Popup
    folium.Marker(
        location=m.location,
        icon=folium.DivIcon(html=legend_html),
        control=False
    ).add_to(m)

# Main function for Streamlit
def main():
    st.title("Intensity of rail use")
    st.write("The map below shows the intensity of each piece of rail in The Netherlands. The map is adjustable. \
             Different station types can be selected, as well as different transport operators.")
    
    # Load and process data
    df_hele_week, df_other_set_1, df_other_set_2, stations = load_data()

    # Process each DataFrame
    df_hele_week = process_line_data(df_hele_week)
    df_other_set_1 = process_line_data(df_other_set_1)
    df_other_set_2 = process_line_data(df_other_set_2)

    # Get the initial map center and zoom level from the first coordinates
    initial_center = df_hele_week['latlon_coords'][0][0]  # First coordinate
    initial_zoom = 7

    # Sidebar for line set selection
    line_sets = st.sidebar.multiselect(
        "Select provider to display:",
        options=['PlotDataHeleWeek', 'OtherLineSet1', 'OtherLineSet2'],
        default=['PlotDataHeleWeek']
    )

    # Sidebar selection for station types
    station_type = st.sidebar.multiselect(
        "Select station types to display:",
        options=[0.0, 1.0],
        format_func=lambda x: "Randstad" if x == 1.0 else "Non-Randstad",
        default=[]
    )

    # Draw the initial map
    folium_map = draw_map(initial_center, initial_zoom)

    # Add selected line sets to the map
    if 'PlotDataHeleWeek' in line_sets:
        folium_map = add_lines_to_map(folium_map, df_hele_week)
    if 'OtherLineSet1' in line_sets:
        folium_map = add_lines_to_map(folium_map, df_other_set_1)
    if 'OtherLineSet2' in line_sets:
        folium_map = add_lines_to_map(folium_map, df_other_set_2)

    # Add selected station types to the map (if any)
    if station_type:
        folium_map = add_stations_to_map(folium_map, stations, station_type)

    # Add legend to the map
    add_legend(folium_map)

    # Display the map in Streamlit
    st.components.v1.html(folium_map._repr_html_(), height=600)

# Run the app
if __name__ == "__main__":
    main()
