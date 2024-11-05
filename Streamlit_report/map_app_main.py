import pandas as pd
import re
from pyproj import CRS, Transformer
import folium
import streamlit as st
from matplotlib import colors
import numpy as np


# ------------ Functions for loading data ------------------

@st.cache_data
def load_data():
    # Define the date range for the week
    date_range = [
        "2024-10-07",  # Monday
        "2024-10-08",  # Tuesday
        "2024-10-09",  # Wednesday
        "2024-10-10",  # Thursday
        "2024-10-11",  # Friday
        "2024-10-12",  # Saturday
        "2024-10-13"   # Sunday
    ]
    
    # Load datasets for each day of the week
    df_list = []
    for date in date_range:
        df_all = pd.read_csv(f"OutputData/PlotData{date}all.csv")
        df_interm = pd.read_csv(f"OutputData/PlotData{date}intercities.csv")
        df_sprinter = pd.read_csv(f"OutputData/PlotData{date}sprinters.csv")
        df_list.append((df_all, df_interm, df_sprinter))

    # Load datasets for the entire week
    df_week_all = pd.read_csv("OutputData/PlotDataWeekall.csv")
    df_week_interm = pd.read_csv("OutputData/PlotDataWeekintercities.csv")
    df_week_sprinter = pd.read_csv("OutputData/PlotDataWeeksprinters.csv")

    # Load datasets for each provider
    providers = ["Arriva", "Keolis", "NS", "Qbuzz"]
    
    # Initialize DataFrames for providers
    provider_dfs_all = {}
    provider_dfs_interm = {}
    provider_dfs_sprinter = {}
    
    for provider in providers:
        provider_dfs_all[provider] = pd.read_csv(f"OutputData/PlotDataWeek{provider}all.csv")
        provider_dfs_interm[provider] = pd.read_csv(f"OutputData/PlotDataWeek{provider}intercities.csv")
        provider_dfs_sprinter[provider] = pd.read_csv(f"OutputData/PlotDataWeek{provider}sprinters.csv")

    # Load dataset for the stations
    stations = pd.read_csv("Streamlit_data/Randstad-0.0.csv")

    # Unpack data into individual DataFrames
    (df_monday, df_monday_interm, df_monday_sprinter), \
    (df_tuesday, df_tuesday_interm, df_tuesday_sprinter), \
    (df_wednesday, df_wednesday_interm, df_wednesday_sprinter), \
    (df_thursday, df_thursday_interm, df_thursday_sprinter), \
    (df_friday, df_friday_interm, df_friday_sprinter), \
    (df_saturday, df_saturday_interm, df_saturday_sprinter), \
    (df_sunday, df_sunday_interm, df_sunday_sprinter) = df_list

    return (df_week_all, df_week_interm, df_week_sprinter, 
            provider_dfs_all['Arriva'], provider_dfs_interm['Arriva'], provider_dfs_sprinter['Arriva'],
            provider_dfs_all['Keolis'], provider_dfs_interm['Keolis'], provider_dfs_sprinter['Keolis'],
            provider_dfs_all['NS'], provider_dfs_interm['NS'], provider_dfs_sprinter['NS'],
            provider_dfs_all['Qbuzz'], provider_dfs_interm['Qbuzz'], provider_dfs_sprinter['Qbuzz'],
            df_monday, df_monday_interm, df_monday_sprinter,
            df_tuesday, df_tuesday_interm, df_tuesday_sprinter,
            df_wednesday, df_wednesday_interm, df_wednesday_sprinter,
            df_thursday, df_thursday_interm, df_thursday_sprinter,
            df_friday, df_friday_interm, df_friday_sprinter,
            df_saturday, df_saturday_interm, df_saturday_sprinter,
            df_sunday, df_sunday_interm, df_sunday_sprinter, 
            stations)



# ------------ Functions for fetching coordinates from data  ------------------

#Extract coordinates from the 'LINESTRING' format
def extract_coords(geometry_str):
    coords = re.findall(r'(-?\d+\.\d+)\s(-?\d+\.\d+)', geometry_str)
    if not coords:  
        return None
    return [(float(lat), float(lon)) for lon, lat in coords] # Swap the coordinates if reversed 

# Precompute data processing for lines
@st.cache_data
def process_line_data(df):
    df['coords'] = df['geometry'].apply(extract_coords)
    df = df.dropna(subset=['coords'])  # Drop rows where no valid coordinates could be extracted

    # Normalize seat capacity to use for color scaling
    df['capacity_norm'] = (df['Seats'] - df['Seats'].min()) / (df['Seats'].max() - df['Seats'].min())
    df['latlon_coords'] = df['coords']  
    return df.dropna(subset=['latlon_coords']) 


# ------------ Functions for train lines and stations  ------------------

# Generate a gradient color based on normalized capacity
def capacity_color(norm_value):
    return colors.to_hex((1, 1 - norm_value, 0))  # Interpolates between yellow (0) and red (1)

# Get color value for specific seat capacity
def get_color_for_seat_value(seat_value, min_seat, max_seat):
    if max_seat == min_seat:  
        return colors.to_hex((1, 0, 0))  # Return red if no variation in data
    norm_value = (seat_value - min_seat) / (max_seat - min_seat)
    return capacity_color(norm_value)

# Plot lines and stations
@st.cache_data
def draw_map(initial_center, initial_zoom):
    # Use initial center and zoom level to keep map state
    m = folium.Map(location=initial_center, zoom_start=initial_zoom, control_scale=True, tiles='CartoDB positron')
    return m

# Add lines to the map with color based on seat capacity
def add_lines_to_map(m, df):
    for _, row in df.iterrows():
        latlon_coords = row['latlon_coords']
        norm_capacity = row['capacity_norm']
        color = capacity_color(norm_capacity)
        folium.PolyLine(latlon_coords, color=color, weight=2.5, opacity=1).add_to(m)
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


# -------------- Main function for Streamlit --------------------
def main():
    st.subheader("Intensity of Rail Use")
    st.write('''The map below shows the intensity of each piece of rail in The Netherlands. 
         The map is adjustable and several different options can be selected in the side bar. 
         Different station types can be selected for both inside as outside of the Randstad area. 
         For the whole week option, different transport providers can be selected. If a particular day of the week is selected, 
         the map is shown for all providers combined. In the legend the meaning of the colors are visible. The range of this colors is
         determined by the maximum, minimum, mean, 1st quarter (25% of the maximum value) and 3rd quarter (75% of the maximum value) of the capacities. So if, for example, the red color in a particular selection
         is equal to 2804, the maximum seat capacity in that selection is equal to 2,804,000 seats.''')

    # Load and process data
    (df_week_all, df_week_interm, df_week_sprinter, 
     df_arriva_all, df_arriva_interm, df_arriva_sprinter,
     df_keolis_all, df_keolis_interm, df_keolis_sprinter,
     df_ns_all, df_ns_interm, df_ns_sprinter,
     df_qbuzz_all, df_qbuzz_interm, df_qbuzz_sprinter,
     df_monday, df_monday_interm, df_monday_sprinter,
     df_tuesday, df_tuesday_interm, df_tuesday_sprinter,
     df_wednesday, df_wednesday_interm, df_wednesday_sprinter,
     df_thursday, df_thursday_interm, df_thursday_sprinter,
     df_friday, df_friday_interm, df_friday_sprinter,
     df_saturday, df_saturday_interm, df_saturday_sprinter,
     df_sunday, df_sunday_interm, df_sunday_sprinter,
     stations) = load_data()

    # Process weekly data
    df_week_all = process_line_data(df_week_all)
    df_week_interm = process_line_data(df_week_interm)
    df_week_sprinter = process_line_data(df_week_sprinter)
    
    # Process daily data
    df_monday = process_line_data(df_monday)
    df_monday_interm = process_line_data(df_monday_interm)
    df_monday_sprinter = process_line_data(df_monday_sprinter)
    
    df_tuesday = process_line_data(df_tuesday)
    df_tuesday_interm = process_line_data(df_tuesday_interm)
    df_tuesday_sprinter = process_line_data(df_tuesday_sprinter)
    
    df_wednesday = process_line_data(df_wednesday)
    df_wednesday_interm = process_line_data(df_wednesday_interm)
    df_wednesday_sprinter = process_line_data(df_wednesday_sprinter)
    
    df_thursday = process_line_data(df_thursday)
    df_thursday_interm = process_line_data(df_thursday_interm)
    df_thursday_sprinter = process_line_data(df_thursday_sprinter)
    
    df_friday = process_line_data(df_friday)
    df_friday_interm = process_line_data(df_friday_interm)
    df_friday_sprinter = process_line_data(df_friday_sprinter)
    
    df_saturday = process_line_data(df_saturday)
    df_saturday_interm = process_line_data(df_saturday_interm)
    df_saturday_sprinter = process_line_data(df_saturday_sprinter)
    
    df_sunday = process_line_data(df_sunday)
    df_sunday_interm = process_line_data(df_sunday_interm)
    df_sunday_sprinter = process_line_data(df_sunday_sprinter)

    # Process provider data
    df_arriva_all = process_line_data(df_arriva_all)
    df_arriva_interm = process_line_data(df_arriva_interm)
    df_arriva_sprinter = process_line_data(df_arriva_sprinter)
    
    df_keolis_all = process_line_data(df_keolis_all)
    df_keolis_interm = process_line_data(df_keolis_interm)
    df_keolis_sprinter = process_line_data(df_keolis_sprinter)

    df_ns_all = process_line_data(df_ns_all)
    df_ns_interm = process_line_data(df_ns_interm)
    df_ns_sprinter = process_line_data(df_ns_sprinter)
    
    df_qbuzz_all = process_line_data(df_qbuzz_all)
    df_qbuzz_interm = process_line_data(df_qbuzz_interm)
    df_qbuzz_sprinter = process_line_data(df_qbuzz_sprinter)


    # Get the initial map center and zoom level (Utrecht coordinates)
    initial_center = [52.0907, 6.1214]  # Utrecht coordinates
    initial_zoom = 7

    days_of_week = [
        'Week', 'Monday', 'Tuesday', 'Wednesday', 
        'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]
    selected_day = st.sidebar.selectbox(
        "Select a day of the week:",
        options=days_of_week,
        index=0,  # Default to 'Week'
        key="day_selectbox"  # Unique key for the day selectbox
    )

    # Sidebar for provider selection
    providers = ['All', 'Arriva', 'Keolis', 'NS', 'Qbuzz']
    # Provider selection is conditional based on selected day
    if selected_day == 'Week':
        selected_provider = st.sidebar.selectbox(
            "Select a provider:",
            options=providers,
            index=0,  # Default to 'All'
            key="provider_selectbox"  # Unique key for the provider selectbox
        )
    else:
        selected_provider = 'All'  # Default to 'All' when a specific day is selected

    # Sidebar for train type selection
    if selected_day == 'Week' and selected_provider == 'Qbuzz':
        train_types = ['Sprinters']  # Only Sprinters available for Qbuzz
    else:
        train_types = ['All', 'Intercity', 'Sprinters']  # Default options

    selected_train_type = st.sidebar.selectbox(
        "Select train type:",
        options=train_types,
        index=0,  # Default to 'All' or the only option
        key="train_type_selectbox"  # Unique key for the train type selectbox
    )

    # Sidebar selection for Randstad types
    station_type = st.sidebar.multiselect(
        "Select stations area:",
        options=[0.0, 1.0],
        format_func=lambda x: "Randstad" if x == 1.0 else "Non-Randstad",
        default=[],
        key="station_type_multiselect"  # Unique key for the station type multiselect
    )

    # Sidebar selection for Type codes
    type_code_options = stations['Type code'].unique()  # Get unique Type codes from the stations
    selected_type_codes = st.sidebar.multiselect(
        "Select station type:",
        options=type_code_options,
        format_func=lambda x: "Intercity station" if x == 1.0 else "Sprinter station",
        default=[],
        key="type_code_multiselect"  # Unique key for the type code multiselect
    )

    # Determine the dataset to use based on selections
    if selected_day == 'Week':
        line_set = 'PlotDataWeekall' if selected_train_type == 'All' else f'PlotDataWeek{selected_train_type.lower()}'
        if selected_provider != 'All':
            line_set = f'PlotDataWeek{selected_train_type.lower()}{selected_provider}'
    else:
        line_set = f'PlotData{selected_day}{selected_train_type.lower()}'

    # Draw the initial map
    folium_map = draw_map(initial_center, initial_zoom)


    # For the whole week, data per provider is available
    if selected_day == "Week":
        if selected_train_type == 'All':
            if selected_provider == 'All':
                folium_map = add_lines_to_map(folium_map, df_week_all)
                min_seat = int(df_week_all['Seats'].min() // 1000)
                max_seat = int(df_week_all['Seats'].max() // 1000)
            else:
                provider_key = selected_provider.lower()  # Convert provider name to lower case
                folium_map = add_lines_to_map(folium_map, eval(f'df_{provider_key}_all'))
                min_seat = int(eval(f'df_{provider_key}_all')['Seats'].min() // 1000)
                max_seat = int(eval(f'df_{provider_key}_all')['Seats'].max() // 1000)
        elif selected_train_type == 'Intercity':
            if selected_provider == 'All':
                folium_map = add_lines_to_map(folium_map, df_week_interm)
                min_seat = int(df_week_interm['Seats'].min() // 1000)
                max_seat = int(df_week_interm['Seats'].max() // 1000)
            else:
                provider_key = selected_provider.lower()
                folium_map = add_lines_to_map(folium_map, eval(f'df_{provider_key}_interm'))
                min_seat = int(eval(f'df_{provider_key}_interm')['Seats'].min() // 1000)
                max_seat = int(eval(f'df_{provider_key}_interm')['Seats'].max() // 1000)
        elif selected_train_type == 'Sprinters':
            if selected_provider == 'All':
                folium_map = add_lines_to_map(folium_map, df_week_sprinter)
                min_seat = int(df_week_sprinter['Seats'].min() // 1000)
                max_seat = int(df_week_sprinter['Seats'].max() // 1000)
            else:
                provider_key = selected_provider.lower()
                folium_map = add_lines_to_map(folium_map, eval(f'df_{provider_key}_sprinter'))
                min_seat = int(eval(f'df_{provider_key}_sprinter')['Seats'].min() // 1000)
                max_seat = int(eval(f'df_{provider_key}_sprinter')['Seats'].max() // 1000)

    # Handle daily cases
    else:
        if selected_day == 'Monday':
            if selected_train_type == 'All':
                folium_map = add_lines_to_map(folium_map, df_monday)
                min_seat = int(df_monday['Seats'].min() // 1000)
                max_seat = int(df_monday['Seats'].max() // 1000)
            elif selected_train_type == 'Intercity':
                folium_map = add_lines_to_map(folium_map, df_monday_interm)
                min_seat = int(df_monday_interm['Seats'].min() // 1000)
                max_seat = int(df_monday_interm['Seats'].max() // 1000)
            elif selected_train_type == 'Sprinters':
                folium_map = add_lines_to_map(folium_map, df_monday_sprinter)
                min_seat = int(df_monday_sprinter['Seats'].min() // 1000)
                max_seat = int(df_monday_sprinter['Seats'].max() // 1000)
        elif selected_day == 'Tuesday':
            if selected_train_type == 'All':
                folium_map = add_lines_to_map(folium_map, df_tuesday)
                min_seat = int(df_tuesday['Seats'].min() // 1000)
                max_seat = int(df_tuesday['Seats'].max() // 1000)
            elif selected_train_type == 'Intercity':
                folium_map = add_lines_to_map(folium_map, df_tuesday_interm)
                min_seat = int(df_tuesday_interm['Seats'].min() // 1000)
                max_seat = int(df_tuesday_interm['Seats'].max() // 1000)
            elif selected_train_type == 'Sprinters':
                folium_map = add_lines_to_map(folium_map, df_tuesday_sprinter)
                min_seat = int(df_tuesday_sprinter['Seats'].min() // 1000)
                max_seat = int(df_tuesday_sprinter['Seats'].max() // 1000)
        elif selected_day == 'Wednesday':
            if selected_train_type == 'All':
                folium_map = add_lines_to_map(folium_map, df_wednesday)
                min_seat = int(df_wednesday['Seats'].min() // 1000)
                max_seat = int(df_wednesday['Seats'].max() // 1000)
            elif selected_train_type == 'Intercity':
                folium_map = add_lines_to_map(folium_map, df_wednesday_interm)
                min_seat = int(df_wednesday_interm['Seats'].min() // 1000)
                max_seat = int(df_wednesday_interm['Seats'].max() // 1000)
            elif selected_train_type == 'Sprinters':
                folium_map = add_lines_to_map(folium_map, df_wednesday_sprinter)
                min_seat = int(df_wednesday_sprinter['Seats'].min() // 1000)
                max_seat = int(df_wednesday_sprinter['Seats'].max() // 1000)
        elif selected_day == 'Thursday':
            if selected_train_type == 'All':
                folium_map = add_lines_to_map(folium_map, df_thursday)
                min_seat = int(df_thursday['Seats'].min() // 1000)
                max_seat = int(df_thursday['Seats'].max() // 1000)
            elif selected_train_type == 'Intercity':
                folium_map = add_lines_to_map(folium_map, df_thursday_interm)
                min_seat = int(df_thursday_interm['Seats'].min() // 1000)
                max_seat = int(df_thursday_interm['Seats'].max() // 1000)
            elif selected_train_type == 'Sprinters':
                folium_map = add_lines_to_map(folium_map, df_thursday_sprinter)
                min_seat = int(df_thursday_sprinter['Seats'].min() // 1000)
                max_seat = int(df_thursday_sprinter['Seats'].max() // 1000)
        elif selected_day == 'Friday':
            if selected_train_type == 'All':
                folium_map = add_lines_to_map(folium_map, df_friday)
                min_seat = int(df_friday['Seats'].min() // 1000)
                max_seat = int(df_friday['Seats'].max() // 1000)
            elif selected_train_type == 'Intercity':
                folium_map = add_lines_to_map(folium_map, df_friday_interm)
                min_seat = int(df_friday_interm['Seats'].min() // 1000)
                max_seat = int(df_friday_interm['Seats'].max() // 1000)
            elif selected_train_type == 'Sprinters':
                folium_map = add_lines_to_map(folium_map, df_friday_sprinter)
                min_seat = int(df_friday_sprinter['Seats'].min() // 1000)
                max_seat = int(df_friday_sprinter['Seats'].max() // 1000)
        elif selected_day == 'Saturday':
            if selected_train_type == 'All':
                folium_map = add_lines_to_map(folium_map, df_saturday)
                min_seat = int(df_saturday['Seats'].min() // 1000)
                max_seat = int(df_saturday['Seats'].max() // 1000)
            elif selected_train_type == 'Intercity':
                folium_map = add_lines_to_map(folium_map, df_saturday_interm)
                min_seat = int(df_saturday_interc['Seats'].min() // 1000)
                max_seat = int(df_saturday_interc['Seats'].max() // 1000)
            elif selected_train_type == 'Sprinters':
                folium_map = add_lines_to_map(folium_map, df_saturday_sprinter)
                min_seat = int(df_saturday_sprinter['Seats'].min() // 1000)
                max_seat = int(df_saturday_sprinter['Seats'].max() // 1000)
        elif selected_day == 'Sunday':
            if selected_train_type == 'All':
                folium_map = add_lines_to_map(folium_map, df_sunday)
                min_seat = int(df_sunday['Seats'].min() // 1000)
                max_seat = int(df_sunday['Seats'].max() // 1000)
            elif selected_train_type == 'Intercity':
                folium_map = add_lines_to_map(folium_map, df_sunday_interm)
                min_seat = int(df_sunday_interc['Seats'].min() // 1000)
                max_seat = int(df_sunday_interc['Seats'].max() // 1000)
            elif selected_train_type == 'Sprinters':
                folium_map = add_lines_to_map(folium_map, df_sunday_sprinter)
                min_seat = int(df_sunday_sprinter['Seats'].min() // 1000)
                max_seat = int(df_sunday_sprinter['Seats'].max() // 1000)

    # Add selected station types to the map (if any)
    folium_map = add_stations_to_map(folium_map, stations, station_type, selected_type_codes)

    # Display the map in Streamlit
    st.components.v1.html(folium_map._repr_html_(), height=600)

    # Create a legend on the right side of the map
    median_seat = int((min_seat + max_seat) / 2)  
    third_seat_value = median_seat - (median_seat - min_seat) // 2  
    fourth_seat_value = max_seat - (max_seat - median_seat) // 2 

    legend_html = """
    <div style="position: relative; 
                top: -610px; 
                left: 480px; 
                width: 200px; 
                height: 240px; 
                border:2px solid grey; 
                background-color: white; 
                padding: 10px; 
                font-size: 14px; 
                margin-top: 10px;">
    <b>Legend</b><br>
    <i>Seat capacity (x1000)</i><br>
    <span style="display: flex; justify-content: space-between; padding-left: 10px;">
        <span><i style="color: #ff0000;">&#9679;</i> Seats:</span><span>{max_seat}</span>
    </span>
    <span style="display: flex; justify-content: space-between; padding-left: 10px;">
        <span><i style="color: #ff8000;">&#9679;</i> Seats:</span><span>{fourth_seat_value}</span>
    </span>
    <span style="display: flex; justify-content: space-between; padding-left: 10px;">
        <span><i style="color: #ffa500;">&#9679;</i> Seats:</span><span>{median_seat}</span>
    </span>
    <span style="display: flex; justify-content: space-between; padding-left: 10px;">
        <span><i style="color: #ffff00;">&#9679;</i> Seats:</span><span>{third_seat_value}</span>
    </span>
    <span style="display: flex; justify-content: space-between; padding-left: 10px;">
        <span><i style="color: #ffff00;">&#9679;</i> Seats:</span><span>{min_seat}</span>
    </span>
    <i>Stations</i><br>
    <span style="display: flex; justify-content: space-between; padding-left: 10px;">
        <span><i style="color: #bbbfb5;">&#9679;</i> Non-Randstad</span>
    </span>
    <span style="display: flex; justify-content: space-between; padding-left: 10px;">
        <span><i style="color: #868a81;">&#9679;</i> Randstad</span>
    </span>
    </div>
    """.format(max_seat=max_seat, median_seat=median_seat, min_seat=min_seat, 
            third_seat_value=third_seat_value, fourth_seat_value=fourth_seat_value)

    st.markdown(legend_html, unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    main()
