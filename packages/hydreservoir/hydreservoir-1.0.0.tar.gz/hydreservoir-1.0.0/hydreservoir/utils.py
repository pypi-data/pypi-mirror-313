import numpy as np
from typing import Dict, Union, List, Array

def get_capacity(water_level: float, water_level_capacity_map: Dict[float, float], nearest_mapping: bool = False) -> float:
    """
    Map a single water level to its corresponding capacity.
    
    Args:
        water_level: Input water level
        water_level_capacity_map: Dictionary mapping water levels to capacities
        nearest_mapping: If True, use nearest available mapping when exact match not found
    
    Returns:
        Corresponding capacity or np.nan
    """
    if water_level in water_level_capacity_map:
        return water_level_capacity_map[water_level]
    
    if nearest_mapping:
        nearest_key = min(water_level_capacity_map.keys(), key=lambda x: abs(x - water_level))
        return water_level_capacity_map[nearest_key]
    
    return np.nan

def map_capacity(water_levels: Union[List[float], np.ndarray], 
                 water_level_capacity_map: Dict[float, float], 
                 nearest_mapping: bool = False) -> np.ndarray:
    """
    Map an array of water levels to their corresponding capacities.
    
    Args:
        water_levels: Input water levels array
        water_level_capacity_map: Dictionary mapping water levels to capacities
        nearest_mapping: If True, use nearest available mapping when exact match not found
    
    Returns:
        Array of capacities
    
    Raises:
        ValueError: If missing values exist and nearest_mapping is False
    """
    capacities = np.array([get_capacity(wl, water_level_capacity_map, nearest_mapping) for wl in water_levels])
    
    if np.isnan(capacities).any():
        raise ValueError(
            "There are missing values in capacities. Consider setting 'nearest_mapping=True' "
            "to fill missing values with the nearest available capacity."
        )
    
    return capacities

def get_water_level(capacity: float, capacity_water_level_map: Dict[float, float], nearest_mapping: bool = False) -> float:
    """
    Map a single capacity to its corresponding water level.
    
    Args:
        capacity: Input capacity
        capacity_water_level_map: Dictionary mapping capacities to water levels
        nearest_mapping: If True, use nearest available mapping when exact match not found
    
    Returns:
        Corresponding water level or np.nan
    """
    if capacity in capacity_water_level_map:
        return capacity_water_level_map[capacity]
    
    if nearest_mapping:
        nearest_key = min(capacity_water_level_map.keys(), key=lambda x: abs(x - capacity))
        return capacity_water_level_map[nearest_key]
    
    return np.nan

def map_water_level(capacities: Union[List[float], np.ndarray], 
                    capacity_water_level_map: Dict[float, float], 
                    nearest_mapping: bool = False) -> np.ndarray:
    """
    Map an array of capacities to their corresponding water levels.
    
    Args:
        capacities: Input capacities array
        capacity_water_level_map: Dictionary mapping capacities to water levels
        nearest_mapping: If True, use nearest available mapping when exact match not found
    
    Returns:
        Array of water levels
    
    Raises:
        ValueError: If missing values exist and nearest_mapping is False
    """
    water_levels = np.array([get_water_level(cap, capacity_water_level_map, nearest_mapping) for cap in capacities])
    
    if np.isnan(water_levels).any():
        raise ValueError(
            "There are missing values in water levels. Consider setting 'nearest_mapping=True' "
            "to fill missing values with the nearest available water level."
        )
    
    return water_levels