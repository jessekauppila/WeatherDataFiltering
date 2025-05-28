from datetime import datetime
from typing import Dict, List, Any, TypedDict
import pandas as pd
from .snow_depth_utils import (
    filter_snow_depth_outliers,
    SNOW_DEPTH_CONFIG,
    SNOW_DEPTH_24H_CONFIG,
    SnowDataPoint
)

def filter_dataframe_observations(
    df: pd.DataFrame,
    is_metric: bool = False
) -> pd.DataFrame:
    """
    Filter snow depth measurements from a pandas DataFrame.
    
    Args:
        df: DataFrame with columns: date_time, snow_depth, snow_depth_24h
        is_metric: Boolean indicating if measurements are in metric
    
    Returns:
        DataFrame with filtered snow depth measurements
    """
    # Convert DataFrame to list of dictionaries for filtering
    observations = df.to_dict('records')
    
    # Create snow depth data points
    snow_depth_data = [
        SnowDataPoint(
            date_time=str(obs['date_time']),
            snow_depth=obs.get('snow_depth'),
            stid=obs.get('station_id', 'default')
        )
        for obs in observations
    ]
    
    snow_depth_24h_data = [
        SnowDataPoint(
            date_time=str(obs['date_time']),
            snow_depth=obs.get('snow_depth_24h'),
            stid=obs.get('station_id', 'default')
        )
        for obs in observations
    ]
    
    # Apply filters
    filtered_snow_depth = filter_snow_depth_outliers(
        snow_depth_data,
        SNOW_DEPTH_CONFIG,
        is_metric
    )
    
    filtered_snow_depth_24h = filter_snow_depth_outliers(
        snow_depth_24h_data,
        SNOW_DEPTH_24H_CONFIG,
        is_metric
    )
    
    # Create lookup dictionaries
    snow_depth_map = {
        item['date_time']: item['snow_depth']
        for item in filtered_snow_depth
    }
    
    snow_depth_24h_map = {
        item['date_time']: item['snow_depth']
        for item in filtered_snow_depth_24h
    }
    
    # Create new filtered DataFrame
    df_filtered = df.copy()
    df_filtered['snow_depth'] = df_filtered['date_time'].astype(str).map(snow_depth_map)
    df_filtered['snow_depth_24h'] = df_filtered['date_time'].astype(str).map(snow_depth_24h_map)
    
    return df_filtered