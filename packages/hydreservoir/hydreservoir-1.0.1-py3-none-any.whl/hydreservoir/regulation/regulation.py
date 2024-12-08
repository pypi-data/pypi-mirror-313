import numpy as np
import pandas as pd
from hydutils.df_validation import validate_columns_for_nulls

from hydreservoir.columns_constant import (
    CAPACITY_HT,
    INFLOW,
    INTERVAL,
    MONTH,
    OUTFLOW,
    TIMESERIES,
    YEAR,
    YEAR_MONTH,
)
from hydreservoir.regulation.dataset import Dataset


def _is_greater_than_10_years(df: pd.DataFrame) -> bool:
    """
    Check if the DataFrame contains data spanning at least 10 unique years.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a time series column

    Returns
    -------
    bool
        True if the DataFrame contains data from 10 or more unique years,
        False otherwise

    Notes
    -----
    This function extracts unique years from the TIMESERIES column
    and checks if the count is at least 10.
    """
    return len(df[TIMESERIES].dt.year.unique()) >= 10


def _init_calculation_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the input DataFrame for hydrological calculations by
    processing time-related columns and resampling data.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with time series data

    Returns
    -------
    pd.DataFrame
        Processed DataFrame with additional time-related columns and
        monthly resampled data

    Notes
    -----
    - Extracts year and month from the TIMESERIES column
    - Resamples data to monthly means
    - Calculates time intervals between observations
    - Converts year and month columns to integer type
    """
    # Extract year and month from timeseries
    df[YEAR] = df[TIMESERIES].dt.year
    df[MONTH] = df[TIMESERIES].dt.month

    # Set index and resample to monthly means
    df.set_index(TIMESERIES, inplace=True)
    df = df.resample("ME").mean()
    df.reset_index(drop=True, inplace=True)

    # Convert year and month to integer
    df[YEAR] = df[YEAR].astype(int)
    df[MONTH] = df[MONTH].astype(int)

    # Create temporary year-month column for interval calculation
    df[YEAR_MONTH] = pd.to_datetime(
        df[YEAR].astype(str) + "-" + df[MONTH].astype(str), format="%Y-%m"
    )

    # Calculate time intervals and drop temporary column
    df[INTERVAL] = df[YEAR_MONTH].diff().dt.total_seconds().fillna(0)
    df = df.drop(columns=[YEAR_MONTH])

    return df


def _P_n(df: pd.DataFrame, V_c: float) -> float:
    """
    Calculate the percentage of years with sufficient water capacity.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing hydrological data with columns for
        outflow, inflow, and time intervals
    V_c : float
        Critical water capacity threshold (in million cubic meters)

    Returns
    -------
    float
        Percentage of years that maintain water capacity above
        the critical threshold

    Notes
    -----
    - Uses vectorized calculations for performance
    - Checks water sufficiency by tracking cumulative capacity changes
    - Handles water balance calculations on a year-by-year basis

    Examples
    --------
    >>> df = prepare_hydrological_dataframe()
    >>> critical_capacity = 100.0  # million cubic meters
    >>> sufficiency_percentage = _P_n(df, critical_capacity)
    """

    # Group by year and perform vectorized calculations
    def check_water_sufficiency(year_group):
        # Calculate cumulative water capacity changes
        capacity_ht = V_c + np.cumsum(
            (year_group[OUTFLOW] - year_group[INFLOW]) * year_group[INTERVAL] / 10**6
        )

        # Check if minimum capacity remains above V_c
        return np.min(np.abs(capacity_ht)) > V_c

    # Use groupby to process years efficiently
    sufficient_years = df.groupby(YEAR).apply(check_water_sufficiency)

    # Calculate percentage of years with enough water
    P_n = (sufficient_years.sum() / len(sufficient_years)) * 100

    return P_n


def P_n(
    dataset: Dataset,
    V_c: float,
    gt_10_years: bool = True,
) -> float:
    """
    Assess the comprehensiveness of a water reservoir regulation strategy.

    Evaluates the performance of a water management strategy based on critical
    water capacity and data comprehensiveness criteria.

    Parameters
    ----------
    dataset : Dataset
        Hydrological dataset containing time series water flow measurements.
        Must include relevant columns for water resource analysis.

    V_c : float
        Critical water capacity threshold in million cubic meters. This value
        represents the minimum water volume necessary for effective reservoir
        management and operational sustainability.

    gt_10_years : bool, optional
        Flag to enforce a minimum data requirement of 10 years.
        Defaults to True, ensuring long-term analysis reliability.

    Returns
    -------
    float
        Performance indicator (P_n) representing the comprehensiveness of the
        water reservoir regulation strategy. A higher value indicates more
        comprehensive management.

    Raises
    ------
    ValueError
        - If data contains null values that cannot be processed
        - When gt_10_years is True and dataset spans less than 10 years

    Examples
    --------
    >>> hydro_dataset = load_hydrological_dataset()
    >>> performance = is_comprehensive_regulation(
    ...     dataset=hydro_dataset,
    ...     V_c=100.0
    ... )
    >>> print(f"Regulation Strategy Performance: {performance}")

    Notes
    -----
    The function performs several key steps:
    - Validates input data for completeness and null values
    - Checks temporal comprehensiveness of the dataset
    - Calculates performance based on critical water capacity
    - Provides a quantitative assessment of regulation strategy effectiveness
    """
    # Validate input data
    df = dataset.to_dataframe()
    df = validate_columns_for_nulls(df)

    # Check data comprehensiveness if required
    if gt_10_years and not _is_greater_than_10_years(df):
        raise ValueError("Requires at least 10 years of data.")

    # Prepare data for calculation
    df = _init_calculation_df(df)

    # Calculate performance
    P_n = _P_n(df, V_c)

    # Compare performance within tolerance
    return P_n
