from typing import List
from hydutils.df_validation import validate_columns_for_nulls
import numpy as np
import pandas as pd

from hydreservoir.columns_constant import (
    BOX_CULVERT_OUT,
    BOX_CULVERT_PREFIX,
    CAPACITY,
    CIRCULAR_CULVERT_OUT,
    CIRCULAR_CULVERT_PREFIX,
    FREE_SPILLWAY_OUT,
    FREE_SPILLWAY_PREFIX,
    GATED_SPILLWAY_OUT,
    GATED_SPILLWAY_PREFIX,
    INFLOW,
    INTERVAL,
    OUTFLOW,
    PUMP,
    TIMESERIES,
    UNKNOWN_DISCHARGE,
    WATER_LEVEL,
)
from hydreservoir.water_balance.dataset import Dataset, HydraulicWorkMap
from hydreservoir.water_balance.hydraulic_calculations import flow, FlowType
from hydreservoir.water_balance.hydraulic_work import HydraulicWork


def _pumps_flow(df: pd.DataFrame):
    """
    Add pump flow to the total outflow.

    Args:
        df (pd.DataFrame): Input dataframe with pump columns.
    """
    pump_columns = [col for col in df.columns if col.startswith(PUMP)]
    df[OUTFLOW] = df[OUTFLOW].values + df[pump_columns].to_numpy().sum(axis=1)


def _unknown_discharge_flow(df: pd.DataFrame):
    """
    Add unknown discharge to the total outflow.

    Args:
        df (pd.DataFrame): Input dataframe with unknown discharge columns.
    """
    unknown_discharge_columns = [
        col for col in df.columns if col.startswith(UNKNOWN_DISCHARGE)
    ]
    df[OUTFLOW] = df[OUTFLOW].values + df[unknown_discharge_columns].to_numpy().sum(
        axis=1
    )


def _hydraulic_works_flow(
    df: pd.DataFrame,
    hydraulic_work_map: HydraulicWorkMap,
    starts_with: str,
    out_prefix: str,
    flow_type: FlowType,
):
    """
    Calculate and add flow for different types of hydraulic works to the total outflow.

    Args:
        df (pd.DataFrame): Input dataframe.
        hydraulic_work_map (HydraulicWorkMap): Mapping of hydraulic work configurations.
        starts_with (str): Prefix for identifying relevant columns.
        out_prefix (str): Prefix for outflow column names.
        flow_type (FlowType): Type of flow calculation (box, circular, gated, free).
    """
    # Collect relevant columns
    relevant_cols = [col for col in df.columns if col.startswith(starts_with)]

    for col in relevant_cols:
        col_components = col.split(".")
        flow_id = col_components[1]

        # Construct outflow column name
        outflow_column_name = f"{out_prefix}{flow_id}"
        if len(col_components) >= 3:
            outflow_column_name += f".{"".join(col_components[2:])}"

        # Get hydraulic work configuration
        cfg, _ = hydraulic_work_map.get(flow_id)

        # Vectorized numpy calculation
        water_levels = df[WATER_LEVEL].to_numpy()
        openings = df[col].to_numpy()

        outflows = np.vectorize(
            lambda w, o: flow(
                water_level=w,
                elevation=cfg.elevation,
                height_or_diameter=cfg.height_or_diameter,
                opening_height=o,
                flow_type=flow_type,
            )
        )(water_levels, openings)

        df[outflow_column_name] = outflows
        df[OUTFLOW] += outflows


def run(
    dataset: Dataset,
):
    """
    Perform water balance calculations for a reservoir dataset.

    This function calculates inflow and outflow based on various hydraulic works,
    including pumps, unknown discharges, box culverts, circular culverts, 
    gated spillways, and free spillways.

    Args:
        dataset (Dataset): Reservoir dataset containing time series and hydraulic work information.

    Returns:
        pd.DataFrame: Dataframe with calculated inflow, outflow, and other water balance parameters.
    """
    df = dataset.to_dataframe()
    df = validate_columns_for_nulls(df)

    # Calculate time interval between measurements
    df[INTERVAL] = df[TIMESERIES].diff().dt.total_seconds().fillna(0)

    # Initialize outflow
    df[OUTFLOW] = 0.0

    # Calculate contributions to outflow from different sources
    _pumps_flow(df)
    _unknown_discharge_flow(df)
    _hydraulic_works_flow(
        df=df,
        hydraulic_work_map=dataset.get_box_culverts(),
        starts_with=BOX_CULVERT_PREFIX,
        out_prefix=BOX_CULVERT_OUT,
        flow_type="box",
    )
    _hydraulic_works_flow(
        df=df,
        hydraulic_work_map=dataset.get_circular_culverts(),
        starts_with=CIRCULAR_CULVERT_PREFIX,
        out_prefix=CIRCULAR_CULVERT_OUT,
        flow_type="circular",
    )
    _hydraulic_works_flow(
        df=df,
        hydraulic_work_map=dataset.get_gated_spillways(),
        starts_with=GATED_SPILLWAY_PREFIX,
        out_prefix=GATED_SPILLWAY_OUT,
        flow_type="gated",
    )
    _hydraulic_works_flow(
        df=df,
        hydraulic_work_map=dataset.get_free_spillways(),
        starts_with=FREE_SPILLWAY_PREFIX,
        out_prefix=FREE_SPILLWAY_OUT,
        flow_type="free",
    )

    # Calculate inflow based on outflow, interval, and capacity changes
    df[INFLOW] = ((df[OUTFLOW] * df[INTERVAL]) + (df[CAPACITY].diff()) * 10**6) / (
        df[INTERVAL]
    )

    # Ensure non-negative and zero-filled values for inflow and outflow
    df[INFLOW] = df[INFLOW].apply(lambda x: x if x >= 0 else 0).fillna(0)
    df[OUTFLOW] = df[OUTFLOW].apply(lambda x: x if x >= 0 else 0).fillna(0)

    return df