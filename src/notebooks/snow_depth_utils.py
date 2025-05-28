# Import necessary libraries
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import sys
import os

# Add the data-scripts directory to Python path
sys.path.append(os.path.join(os.getcwd(), 'data-scripts'))

# Import our custom utilities
from snow_depth_utils import (
    filtered_observation_data,
    filter_snow_depth_outliers,
    calculate_snow_depth_accumulation,
    SNOW_DEPTH_CONFIG,
    SNOW_DEPTH_24H_CONFIG
)

# Create database connection
db_connection_string = 'postgresql://default:rz5dBTWh0kbF@ep-cool-haze-a42pervx-pooler.us-east-1.aws.neon.tech/verceldb?sslmode=require'
engine = create_engine(db_connection_string)

# Query to get data
query = """
SELECT o.*
FROM observations o
WHERE o.station_id = (
    SELECT s.id
    FROM stations s
    WHERE s.station_name = 'Mt. Baker - Heather Meadows'
)
AND o.date_time >= CURRENT_DATE - INTERVAL '1 day'
ORDER BY o.date_time DESC
"""

# Execute query and load into pandas DataFrame
df = pd.read_sql(query, engine)

# Process the data
options = {
    'start_hour': 0,
    'end_hour': 23,
    'mode': 'summary'
}

# Filter the data
filtered_data = filtered_observation_data(df, options, is_metric=False)

# Display results for the first station
first_station = list(filtered_data.keys())[0]
print(f"\nFiltered data for station {first_station}:")
display(filtered_data[first_station].head())

# Calculate snow accumulation
accumulation_data = calculate_snow_depth_accumulation(filtered_data[first_station])
print("\nSnow accumulation data:")
display(accumulation_data[['date_time', 'snow_depth', 'new_snow', 'snow_total']].head())