import pandas as pd
from typing import Dict, List, Any, TypedDict, Optional
from .snow_depth_utils import (
    filter_snow_depth_outliers,
    SNOW_DEPTH_CONFIG,
    SNOW_DEPTH_24H_CONFIG,
    SnowDepthConfig,
    SnowDataPoint
)

def filter_dataframe_observations(
    df: pd.DataFrame, 
    is_metric: bool = False,
    snow_depth_config: Optional[SnowDepthConfig] = None,
    snow_depth_24h_config: Optional[SnowDepthConfig] = None
) -> pd.DataFrame:
    """
    Filter snow depth measurements from a pandas DataFrame.
    """
    # Use custom configs if provided, otherwise use defaults
    config_snow_depth = snow_depth_config or SNOW_DEPTH_CONFIG
    config_snow_24h = snow_depth_24h_config or SNOW_DEPTH_24H_CONFIG

    # Convert DataFrame rows to SnowDataPoint format
    snow_depth_data = [
        SnowDataPoint(
            date_time=str(row['date_time']),
            snow_depth=row.get('snow_depth'),
            stid=str(row.get('station_id', 'default'))
        )
        for _, row in df.iterrows()
    ]

    snow_depth_24h_data = [
        SnowDataPoint(
            date_time=str(row['date_time']),
            snow_depth=row.get('snow_depth_24h'),
            stid=str(row.get('station_id', 'default'))
        )
        for _, row in df.iterrows()
    ]

    # Apply filters with custom configs
    filtered_snow_depth = filter_snow_depth_outliers(
        snow_depth_data,
        config_snow_depth,
        is_metric
    )
    
    filtered_snow_depth_24h = filter_snow_depth_outliers(
        snow_depth_24h_data,
        config_snow_24h,
        is_metric
    )

    # Create result DataFrame
    result_df = df.copy()
    
    # Map filtered values back to DataFrame
    snow_depth_map = {item['date_time']: item['snow_depth'] for item in filtered_snow_depth}
    snow_depth_24h_map = {item['date_time']: item['snow_depth'] for item in filtered_snow_depth_24h}
    
    result_df['snow_depth'] = result_df['date_time'].astype(str).map(snow_depth_map)
    result_df['snow_depth_24h'] = result_df['date_time'].astype(str).map(snow_depth_24h_map)
    
    return result_df