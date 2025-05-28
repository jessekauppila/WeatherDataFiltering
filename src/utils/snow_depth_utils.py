from typing import Dict, List, Optional, TypedDict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SnowDepthConfig:
    threshold: float
    max_positive_change: float
    max_negative_change: float
    window_size: int
    upper_iqr_multiplier: float = 1.5
    lower_iqr_multiplier: float = 1.5
    apply_identical_check: bool = True

class SnowDataPoint(TypedDict):
    date_time: str
    snow_depth: Optional[float]
    stid: Optional[str]

# Configuration constants
SNOW_DEPTH_CONFIG = SnowDepthConfig(
    threshold=0,
    max_positive_change=4,
    max_negative_change=10,
    window_size=24,
    upper_iqr_multiplier=1,
    lower_iqr_multiplier=2,
    apply_identical_check=True
)

SNOW_DEPTH_24H_CONFIG = SnowDepthConfig(
    threshold=-1,
    max_positive_change=4,
    max_negative_change=30,
    window_size=24,
    upper_iqr_multiplier=2,
    lower_iqr_multiplier=1,
    apply_identical_check=False
)

def apply_iqr_filter(data: List[SnowDataPoint], window_size: int, 
                    upper_multiplier: float, lower_multiplier: float) -> List[SnowDataPoint]:
    result = []
    
    for idx, point in enumerate(data):
        half_kernel = window_size // 2
        start = max(0, idx - half_kernel)
        end = min(len(data), idx + half_kernel + 1)
        
        window = sorted([p['snow_depth'] for p in data[start:end] 
                       if p['snow_depth'] is not None])
        
        if not window:
            result.append({'date_time': point['date_time'], 'snow_depth': None})
            continue
            
        q1 = window[int(len(window) * 0.25)]
        q3 = window[int(len(window) * 0.75)]
        iqr = q3 - q1
        
        lower_bound = q1 - (lower_multiplier * iqr)
        upper_bound = q3 + (upper_multiplier * iqr)
        
        snow_depth = point['snow_depth']
        is_outlier = (snow_depth is None or 
                     snow_depth < lower_bound or 
                     snow_depth > upper_bound)
        
        result.append({
            'date_time': point['date_time'],
            'snow_depth': None if is_outlier else snow_depth
        })
    
    return result

def filter_snow_depth_outliers(data: List[SnowDataPoint], 
                             config: SnowDepthConfig,
                             is_metric: bool = False) -> List[SnowDataPoint]:
    if not data:
        return []
        
    # Convert to metric if needed
    working_config = config
    if is_metric:
        working_config = SnowDepthConfig(
            threshold=config.threshold * 2.54,
            max_positive_change=config.max_positive_change * 2.54,
            max_negative_change=config.max_negative_change * 2.54,
            window_size=config.window_size,
            upper_iqr_multiplier=config.upper_iqr_multiplier,
            lower_iqr_multiplier=config.lower_iqr_multiplier,
            apply_identical_check=config.apply_identical_check
        )
    
    # Sort data by date
    sorted_data = sorted(data, key=lambda x: datetime.fromisoformat(x['date_time']))
    
    # Apply filters
    filtered_data = apply_iqr_filter(
        sorted_data,
        working_config.window_size,
        working_config.upper_iqr_multiplier,
        working_config.lower_iqr_multiplier
    )
    
    return filtered_data