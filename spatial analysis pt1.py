import dask.dataframe as dd
import plotly.graph_objects as go

# Step 1: Data Collection
crime_data = dd.read_csv('output_file.csv')  # Using Dask to read the CSV file

# Step 2: Drop rows with missing latitude or longitude values
crime_data = crime_data.dropna(subset=['Latitude', 'Longitude'])

# Convert Dask DataFrame to Pandas DataFrame for easier processing
crime_data_pandas = crime_data.compute()

def plot_crime_map_for_district(district_name):
    """
    Function to generate a crime map for a specific district.
    
    Parameters:
    - district_name: The name of the district for which to generate the map.
    """
    # Check if the district exists in the dataset
    if district_name not in crime_data_pandas['District_Name'].unique():
        print(f"The district '{district_name}' is not found in the dataset.")
        return

    # Filter data for the specified district
    district_data = crime_data_pandas[crime_data_pandas['District_Name'] == district_name]
    
    if district_data.empty:
        print(f"No data available for district: {district_name}")
        return
    
    # Create a map centered at the mean latitude and longitude of the district
    center = {
        'lat': district_data['Latitude'].mean(),
        'lon': district_data['Longitude'].mean()
    }
    
    # Create a Scattermapbox Plot for the current district
    fig = go.Figure(go.Scattermapbox(
        lat=district_data['Latitude'],
        lon=district_data['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=district_data['CrimeType']
    ))
    
    # Customize the map layout
    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox_center=center,
        mapbox_zoom=10,
        height=800,  # Adjust the height of the map
        width=1000,  # Adjust the width of the map
        title=f"Crime Map for {district_name}"  # Set the title of the map as the district name
    )
    
    # Show the map
    fig.show()

# User input for the district
user_input_district = input("Enter the district name to generate the crime map: ")

# Call the function with the user input
plot_crime_map_for_district(user_input_district.strip())
