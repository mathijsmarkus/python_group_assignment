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
def add_stations_to_map(m, stations, selected_types, selected_type_codes):
    for _, row in stations.iterrows():
        # Logic to filter stations based on selected types and type codes
        if selected_types and selected_type_codes:  # Both selected
            if row['Randstad'] in selected_types and row['Type code'] in selected_type_codes:
                add_station_marker(m, row)
        elif selected_types:  # Only station types selected
            if row['Randstad'] in selected_types:
                add_station_marker(m, row)
        elif selected_type_codes:  # Only type codes selected
            if row['Type code'] in selected_type_codes:
                # Show Randstad intercity stations if type code is 1
                if row['Type code'] == 1 and row['Randstad'] == 1.0:
                    add_station_marker(m, row)
        # If Randstad is selected but no type code selected
        elif selected_types == [1.0]:  # If Randstad is selected and no types are selected
            if row['Randstad'] == 1.0:
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
        weight=0  # No border for a seamless look
    ).add_to(m)


# Main function for Streamlit
def main():
    st.title("Intensity of Rail Use")
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
        "Select Randstad type to display:",
        options=[0.0, 1.0],
        format_func=lambda x: "Randstad" if x == 1.0 else "Non-Randstad",
        default=[]
    )

    # Sidebar selection for Type code
    type_code_options = stations['Type code'].unique()  # Get unique Type codes from the stations
    selected_type_codes = st.sidebar.multiselect(
        "Select Type codes to display:",
        options=type_code_options,
        default=[]  # Default can be adjusted as needed
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
