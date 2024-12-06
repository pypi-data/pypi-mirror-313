from datetime import datetime
from typing import Any, Dict, List, Tuple

import pandas as pd

from hydreservoir.columns_constant import (
    BOX_CULVERT_PREFIX,
    CAPACITY,
    CIRCULAR_CULVERT_PREFIX,
    FREE_SPILLWAY_PREFIX,
    GATED_SPILLWAY_PREFIX,
    PUMP_PREFIX,
    TIMESERIES,
    UNKNOWN_DISCHARGE_PREFIX,
    WATER_LEVEL,
)
from hydreservoir.water_balance.hydraulic_work import HydraulicWork

HydraulicWorkMap = Dict[str, Tuple[HydraulicWork, List[float]]]


class Dataset:
    def __init__(self):
        self._timeseries: List[datetime] = []

        self._water_level: List[float] = []
        self._capacity: List[float] = []

        self._pumps: Dict[str, List[float]] = {}

        self._box_culverts: HydraulicWorkMap = {}
        self._circular_culverts: HydraulicWorkMap = {}

        self._gated_spillways: HydraulicWorkMap = {}
        self._free_spillways: HydraulicWorkMap = {}

        self._unknown_discharge: Dict[str, List[float]] = {}

    # Getter methods
    def get_timeseries(self) -> List[datetime]:
        return self._timeseries

    def get_water_level(self) -> List[float]:
        return self._water_level

    def get_capacity(self) -> List[float]:
        return self._capacity

    def get_pumps(self) -> Dict[str, List[float]]:
        return self._pumps

    def get_box_culverts(self) -> HydraulicWorkMap:
        return self._box_culverts

    def get_circular_culverts(self) -> HydraulicWorkMap:
        return self._circular_culverts

    def get_gated_spillways(self) -> HydraulicWorkMap:
        return self._gated_spillways

    def get_free_spillways(self) -> HydraulicWorkMap:
        return self._free_spillways

    def get_unknown_discharge(self) -> Dict[str, List[float]]:
        return self._unknown_discharge

    # Optional method for debugging
    def get_all_data(self) -> Dict[str, Any]:
        return {
            "timeseries": self.get_timeseries(),
            "water_level": self.get_water_level(),
            "capacity": self.get_capacity(),
            "pumps": self.get_pumps(),
            "box_culverts": self.get_box_culverts(),
            "circular_culverts": self.get_circular_culverts(),
            "gated_spillways": self.get_gated_spillways(),
            "free_spillways": self.get_free_spillways(),
            "unknown_discharge": self.get_unknown_discharge(),
        }

    def time_series(self, timeseries: List[datetime]) -> "Dataset":
        self._timeseries = timeseries
        return self

    def water_level(self, water_level: List[float]) -> "Dataset":
        self._water_level = water_level
        return self

    def capacity(self, capacity: List[float]) -> "Dataset":
        self._capacity = capacity
        return self

    def pump(self, pump_id: str, values: List[float]) -> "Dataset":
        if "." in pump_id:
            raise ValueError("Pump ID must not contain dot.")
        self._pumps[pump_id] = values
        return self

    def box_culvert(
        self, box_culvert_id: str, hydraulic_work: HydraulicWork, values: List[float]
    ) -> "Dataset":
        if "." in box_culvert_id:
            raise ValueError("Box Culvert ID must not contain dot.")
        self._box_culverts[box_culvert_id] = (hydraulic_work, values)
        return self

    def circular_culvert(
        self,
        circular_culvert_id: str,
        hydraulic_work: HydraulicWork,
        values: List[float],
    ) -> "Dataset":
        if "." in circular_culvert_id:
            raise ValueError("Circular Culvert ID must not contain dot.")
        self._circular_culverts[circular_culvert_id] = (hydraulic_work, values)
        return self

    def gated_spillway(
        self, gated_spillway_id: str, hydraulic_work: HydraulicWork, values: List[float]
    ) -> "Dataset":
        if "." in gated_spillway_id:
            raise ValueError("Gated Spillway ID must not contain dot.")
        self._gated_spillways[gated_spillway_id] = (hydraulic_work, values)
        return self

    def free_spillway(
        self, free_spillway_id: str, hydraulic_work: HydraulicWork, values: List[float]
    ) -> "Dataset":
        if "." in free_spillway_id:
            raise ValueError("Free Spillway ID must not contain dot.")
        self._free_spillways[free_spillway_id] = (hydraulic_work, values)
        return self

    def unknown_discharge(self, _id: str, values: List[float]) -> "Dataset":
        if "." in _id:
            raise ValueError("ID must not contain dot.")
        self._unknown_discharge[_id] = values
        return self

    def to_dataframe(self) -> pd.DataFrame:
        dataset_dict: Dict[str, List[Any]] = {
            TIMESERIES: self._timeseries,
            WATER_LEVEL: self._water_level,
        }

        for pump_id, values in self._pumps.items():
            dataset_dict[f"{PUMP_PREFIX}{pump_id}"] = values

        for box_culvert_id, (hydraulic_work, values) in self._box_culverts.items():
            dataset_dict[f"{BOX_CULVERT_PREFIX}{box_culvert_id}"] = values

        for circular_culvert_id, (
            hydraulic_work,
            values,
        ) in self._circular_culverts.items():
            dataset_dict[f"{CIRCULAR_CULVERT_PREFIX}{circular_culvert_id}"] = values

        for gated_spillway_id, (
            hydraulic_work,
            values,
        ) in self._gated_spillways.items():
            for i, val in enumerate(values):
                dataset_dict[f"{GATED_SPILLWAY_PREFIX}{gated_spillway_id}.{i}"] = val

        for free_spillway_id, (hydraulic_work, values) in self._free_spillways.items():
            for i, val in enumerate(values):
                dataset_dict[f"{FREE_SPILLWAY_PREFIX}{free_spillway_id}.{i}"] = val

        for unknown_discharge_id, values in self._unknown_discharge.items():
            dataset_dict[f"{UNKNOWN_DISCHARGE_PREFIX}{unknown_discharge_id}"] = values

        dataset_dict[CAPACITY] = self._capacity

        df = pd.DataFrame(dataset_dict)
        df[TIMESERIES] = pd.to_datetime(df[TIMESERIES])

        return df
