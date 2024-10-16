import pandas as pd
import re
from pyproj import Transformer
import folium
import streamlit as st

# Load the CSV data for multiple line sets (for each day of the week)
@st.cache_data
def load_data():
    # Load datasets for each day of the week
    df_hele_week = pd.read_csv("OutputData/PlotDataWeek.csv")
    df_monday = pd.read_csv("OutputData/PlotDataMonday.csv")
    df_tuesday = pd.read_csv("OutputData/PlotDataTuesday.csv")
    df_wednesday = pd.read_csv("OutputData/PlotDataWednesday.csv")
    df_thursday = pd.read_csv("OutputData/PlotDataThursday.csv")
    df_friday = pd.read_csv("OutputData/PlotDataFriday.csv")
    df_saturday = pd.read_csv("OutputData/PlotDataSaturday.csv")
    df_sunday = pd.read_csv("OutputData/PlotDataSunday.csv")
    
    stations = pd.read_csv("Streamlit_data/Randstad-0.0.csv")
    
    return (df_hele_week, df_monday, df_tuesday, df_wednesday, 
            df_thursday, df_friday, df_saturday, df_sunday, stations)

# Extract coordinates function with added check for empty geometry
def extract_coords(geometry_str):
    coords = re.findall(r'(-?\d+\.\d+)\s(-?\d+\.\d+)', geometry_str)
    if not coords:  # If coords is empty, return None
        return None
    return [tuple(map(float, coord)) for coord in coords]

# Precompute data processing for lines
@st.cache_data
def process_line_data(df):
    df['coords'] = df['geometry'].apply(extract_coords)
    df = df.dropna(subset=['coords'])  # Drop rows where 'coords' is None
    
    df['color_hex'] = df['color'].apply(lambda rgb: f'#{int(eval(rgb)[0]*255):02x}{int(eval(rgb)[1]*255):02x}{int(eval(rgb)[2]*255):02x}')
    transformer = Transformer.from_crs("epsg:32631", "epsg:4326")
    
    def convert_coords_to_latlon(coords):
        x_vals, y_vals = zip(*coords)
        lat_vals, lon_vals = transformer.transform(x_vals, y_vals)
        return list(zip(lat_vals, lon_vals))

    df['latlon_coords'] = df['coords'].apply(lambda x: convert_coords_to_latlon(x) if x is not None else None)
    
    return df.dropna(subset=['latlon_coords'])  # Drop rows where 'latlon_coords' could not be computed


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
def add_stations_to_map(m, stations, selected_types, selected_type_codes):
    if not selected_types and not selected_type_codes:
        # Default: no stations are shown if nothing is selected
        return m

    for _, row in stations.iterrows():
        # If both Randstad type and station type are selected
        if selected_types and selected_type_codes:
            if row['Randstad'] in selected_types and row['Type code'] in selected_type_codes:
                add_station_marker(m, row)

        # If no Randstad type selected, show all stations of the selected station type(s)
        elif not selected_types and selected_type_codes:
            if row['Type code'] in selected_type_codes:
                add_station_marker(m, row)

        # If no station type selected, show all stations for the selected Randstad value(s)
        elif selected_types and not selected_type_codes:
            if row['Randstad'] in selected_types:
                add_station_marker(m, row)

    return m

def add_station_marker(m, row):
    # Determine the color based on Randstad type
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
        weight=row['Type code']  # No border for a seamless look
    ).add_to(m)

# Main function for Streamlit
def main():
    st.title("Intensity of Rail Use")
    st.write("The map below shows the intensity of each piece of rail in The Netherlands. The map is adjustable. \
              Different station types can be selected, as well as different transport operators.")

    # Load and process data
    (df_hele_week, df_monday, df_tuesday, df_wednesday, 
     df_thursday, df_friday, df_saturday, df_sunday, stations) = load_data()

    # Process each DataFrame
    df_hele_week = process_line_data(df_hele_week)
    df_monday = process_line_data(df_monday)
    df_tuesday = process_line_data(df_tuesday)
    df_wednesday = process_line_data(df_wednesday)
    df_thursday = process_line_data(df_thursday)
    df_friday = process_line_data(df_friday)
    df_saturday = process_line_data(df_saturday)
    df_sunday = process_line_data(df_sunday)

    # Get the initial map center and zoom level (Utrecht coordinates)
    initial_center = [52.0907, 5.1214]  # Utrecht coordinates
    initial_zoom = 7

    # Sidebar for line set selection (for each day of the week)
    line_set = st.sidebar.selectbox(
        "Select day of the week to display:",
        options=['PlotDataHeleWeek', 'PlotDataMonday', 'PlotDataTuesday', 
                 'PlotDataWednesday', 'PlotDataThursday', 'PlotDataFriday', 
                 'PlotDataSaturday', 'PlotDataSunday'],
        format_func=lambda x: x.replace("PlotData", "Data for ")  # Custom display names
    )

    # Sidebar selection for Randstad types
    station_type = st.sidebar.multiselect(
        "Select Randstad type to display:",
        options=[0.0, 1.0],
        format_func=lambda x: "Randstad" if x == 1.0 else "Non-Randstad",
        default=[]
    )

    # Sidebar selection for Type codes
    type_code_options = stations['Type code'].unique()  # Get unique Type codes from the stations
    selected_type_codes = st.sidebar.multiselect(
        "Select Type codes to display:",
        options=type_code_options,
        format_func=lambda x: "Intercity station" if x == 1.0 else "Sprinter station",
        default=[]
    )

    # Draw the initial map
    folium_map = draw_map(initial_center, initial_zoom)

    # Add the selected line set to the map
    if line_set == 'PlotDataHeleWeek':
        folium_map = add_lines_to_map(folium_map, df_hele_week)
    elif line_set == 'PlotDataMonday':
        folium_map = add_lines_to_map(folium_map, df_monday)
    elif line_set == 'PlotDataTuesday':
        folium_map = add_lines_to_map(folium_map, df_tuesday)
    elif line_set == 'PlotDataWednesday':
        folium_map = add_lines_to_map(folium_map, df_wednesday)
    elif line_set == 'PlotDataThursday':
        folium_map = add_lines_to_map(folium_map, df_thursday)
    elif line_set == 'PlotDataFriday':
        folium_map = add_lines_to_map(folium_map, df_friday)
    elif line_set == 'PlotDataSaturday':
        folium_map = add_lines_to_map(folium_map, df_saturday)
    elif line_set == 'PlotDataSunday':
        folium_map = add_lines_to_map(folium_map, df_sunday)

    # Add selected station types to the map (if any)
    folium_map = add_stations_to_map(folium_map, stations, station_type, selected_type_codes)

    # Display the map in Streamlit
    st.components.v1.html(folium_map._repr_html_(), height=600)

    # Create a legend on the right side of the map
    legend_html = """
    <div style="position: relative; 
                top: -610px; 
                left: 530px; 
                width: 150px; 
                height: 100px; 
                border:2px solid grey; 
                background-color: white; 
                padding: 10px; 
                font-size: 14px; 
                margin-top: 10px;">
    <b>Legend</b><br>
    <i style="color: #bbbfb5;">&#9679;</i> Non-Randstad<br>
    <i style="color: #868a81;">&#9679;</i> Randstad<br>
    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
