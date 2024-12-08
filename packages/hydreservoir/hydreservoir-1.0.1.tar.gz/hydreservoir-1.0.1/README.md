# HydReservoir

[![PyPI Version](https://img.shields.io/pypi/v/hydreservoir)](https://pypi.org/project/hydreservoir/)
[![Python Compatibility](https://img.shields.io/pypi/pyversions/hydreservoir)](https://pypi.org/project/hydreservoir/)
[![License](https://img.shields.io/github/license/duynguyen02/hydreservoir)](https://github.com/duynguyen02/hydreservoir)

## Overview

`HydReservoir` is a comprehensive Python library for advanced hydrological calculations and water reservoir management.

## Key Features

- Detailed water balance calculations
- Complex hydraulic system modeling
- Support for multiple hydraulic components:
  - Pumps
  - Box culverts
  - Circular culverts
  - Gated spillways
  - Free spillways
  - Unknown discharge sources
- Advanced reservoir regulation utilities

## Installation

Install HydReservoir quickly using pip:

```bash
pip install hydreservoir
```

## Getting Started

### 1. Water Balance Calculation

```python
from datetime import datetime
from hydreservoir.water_balance import water_balance
from hydreservoir.water_balance.dataset import Dataset
from hydreservoir.water_balance.hydraulic_work import HydraulicWork

# Create a comprehensive dataset with time series and hydraulic components
dataset = (
    Dataset()
    .time_series([datetime(2023, 1, 1), datetime(2023, 1, 2)])
    .water_level([2.0, 3.0])
    .capacity([2.0, 3.0])
    .pump("pump1", [0.5, 0.6])  # Pump discharge (m³/s)
    .pump("pump2", [0.4, 0.4])  # Pump discharge (m³/s)
    .box_culvert(
        "boxculvert1", 
        HydraulicWork(elevation=1.0, height_or_diameter=2.0), 
        [0.7, 0.8]
    )
    .circular_culvert(
        "circularculvert1",
        HydraulicWork(elevation=1.0, height_or_diameter=2.0),
        [0.1, 0.2]
    )
    .gated_spillway(
        "gatedspillway1",
        HydraulicWork(elevation=1.0, height_or_diameter=2.0),
        [
            [0.4, 0.3],  # port 0 (m)
            [0.4, 0.3],  # port 1 (m)
            [0.4, 0.3],  # port 2 (m)
        ]
    )
    .free_spillway(
        "freespillway1",
        HydraulicWork(elevation=1.0, height_or_diameter=0.0), 
        [[0.0, 0.0]]  # Placeholder for free spillway
    )
    .unknown_discharge("unknowndischarge1", [0.4, 0.7])  # Discharge (m³/s)
)

# Run water balance calculation
result_df = water_balance.run(dataset)
```


### Result DataFrame Columns

The water balance calculation returns a detailed DataFrame with the following columns:

| Column Name                      | Description                                                         | Unit                           | Example               |
| -------------------------------- | ------------------------------------------------------------------- | ------------------------------ | --------------------- |
| `Timeseries`                     | Timestamp for the measurement                                       | Datetime                       | `2023-01-01 00:00:00` |
| `WaterLevel`                     | Current water level in the reservoir                                | Meters (m)                     | `2.5`                 |
| `Capacity`                       | Reservoir capacity corresponding to the current water level         | Cubic meters (m³)              | `1500000`             |
| `Pump.<pump_name>`               | Discharge rate for each pump                                        | Cubic meters per second (m³/s) | `0.5`                 |
| `BoxCulvert.<culvert_name>`      | Opening height for each box culvert                                 | Meters (m)                     | `0.7`                 |
| `CircularCulvert.<culvert_name>` | Opening height for each circular culvert                            | Meters (m)                     | `0.2`                 |
| `GatedSpillway.<name>.<port>`    | Opening height for each port of a gated spillway                    | Meters (m)                     | `0.4`                 |
| `FreeSpillway.<name>`            | Placeholder column (actual flow is calculated based on water level) | Not applicable                 | `0.0`                 |
| `UnknownDischarge.<name>`        | Discharge rate for unknown sources                                  | Cubic meters per second (m³/s) | `0.6`                 |
| `Outflow`                        | Total outflow from all components (calculated)                      | Cubic meters per second (m³/s) | `2.8`                 |
| `Out.<component>.<metadata>`     | Outflow rate for individual components (e.g., specific pumps)       | Cubic meters per second (m³/s) | `1.2`                 |
| `Inflow`                         | Total inflow into the reservoir                                     | Cubic meters per second (m³/s) | `3.0`                 |
| `Interval`                       | Time interval between consecutive measurements                      | Seconds                        | `86400`               |

**Note:**
- `FreeSpillway.<name>` values are placeholders, as the actual discharge for a free spillway depends on water level and crest elevation.
- `Outflow` aggregates discharge from all components, including pumps, culverts, spillways, and unknown sources.
- `Inflow` is calculated from the observed changes in water level, reservoir capacity, and outflow.

### 2. Reservoir Regulation Analysis

```python
from datetime import datetime
from hydreservoir.regulation import regulation
from hydreservoir.regulation.dataset import Dataset as RDataset
from hydreservoir.water_balance import water_balance
from hydreservoir.water_balance.dataset import Dataset
from hydreservoir.water_balance.hydraulic_work import HydraulicWork

# Example of generating mock data and performing regulation analysis
data = generate_mock_data(datetime(2023, 1, 1), 10)

dataset = (
    Dataset()
    .time_series(data["dates"])
    .water_level(data["water_levels"])
    .pump("pump1", data["pump1_flows"])
    .pump("pump2", data["pump2_flows"])
    .box_culvert(
        "boxculvert1",
        HydraulicWork(elevation=1.0, height_or_diameter=2.0),
        data["boxculvert_flows"]
    )
    .circular_culvert(
        "circularculvert1",
        HydraulicWork(elevation=1.0, height_or_diameter=2.0),
        data["circularculvert_flows"]
    )
    .gated_spillway(
        "gatedspillway1",
        HydraulicWork(elevation=1.0, height_or_diameter=2.0),
        data["gatedspillway_ports"]
    )
    .free_spillway(
        "freespillway1",
        HydraulicWork(elevation=1.0, height_or_diameter=2.0),
        data["freespillway_ports"]
    )
    .unknown_discharge(
        "unknowndischarge1", data["unknowndischarge_flows"]
    )
    .capacity(data["capacities"])
)

# Perform water balance calculation
df = water_balance.run(dataset)

# Regulation analysis
P = 90.0
eps = 0.1
P_n = regulation.P_n(RDataset.from_wb_df_to_dataset(df), V_c=1.0, gt_10_years=True)

print(P_n - P <= eps)
```

### 3. Mapping Functions for Water Levels and Capacities
These functions allow efficient mapping between water levels and reservoir capacities, with optional support for nearest neighbor interpolation.

`get_capacity`
Maps a single water level to its corresponding capacity using a provided mapping dictionary. Supports optional nearest neighbor interpolation for unmatched values.
```python
from hydreservoir.utils import get_capacity
water_level_capacity_map = {0.0: 0.0, 1.0: 100.0, 2.0: 200.0}
capacity = get_capacity(1.5, water_level_capacity_map, nearest_mapping=True)
print(capacity)  # Output: 100.0
```
`map_capacity`
Maps an array of water levels to their corresponding capacities using a provided mapping dictionary. Supports optional nearest neighbor interpolation for unmatched values.
```python
from hydreservoir.utils import map_capacity
water_level_capacity_map = {0.0: 0.0, 1.0: 100.0, 2.0: 200.0}
water_levels = [0.5, 1.5, 2.0]
capacities = map_capacity(water_levels, water_level_capacity_map, nearest_mapping=True)
print(capacities)  # Output: [0.0, 100.0, 200.0]
```
`get_water_level`
Maps a single capacity to its corresponding water level using a provided mapping dictionary. Supports optional nearest neighbor interpolation for unmatched values.
```python
from hydreservoir.utils import get_water_level
capacity_water_level_map = {0.0: 0.0, 100.0: 1.0, 200.0: 2.0}
water_level = get_water_level(150.0, capacity_water_level_map, nearest_mapping=True)
print(water_level)  # Output: 1.0
```
`map_water_level`
Maps an array of capacities to their corresponding water levels using a provided mapping dictionary. Supports optional nearest neighbor interpolation for unmatched values.
```python
from hydreservoir.utils import map_water_level
capacity_water_level_map = {0.0: 0.0, 100.0: 1.0, 200.0: 2.0}
capacities = [50.0, 150.0, 200.0]
water_levels = map_water_level(capacities, capacity_water_level_map, nearest_mapping=True)
print(water_levels)  # Output: [0.0, 1.0, 2.0]
```

## License

This library is released under the MIT License.