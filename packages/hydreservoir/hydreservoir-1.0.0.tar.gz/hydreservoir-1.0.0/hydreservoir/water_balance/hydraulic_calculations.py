import math
from typing import Literal


def box_culvert_flow(B: float, a: float, H: float) -> float:
    """
    Calculate discharge flow through a box culvert.

    Args:
        B (float): Width of the culvert (meters)
        a (float): Height of the culvert opening (meters)
        H (float): Water head (meters)

    Returns:
        float: Discharge flow Q (cubic meters per second)

    Formula: Q = e * jc * B * a * sqrt(2g * (H - e * a))
    Where:
    - e = 0.63 (discharge coefficient)
    - jc = 0.94 (contraction coefficient)
    - g = 9.81 (gravitational acceleration, m/s²)

    Raises:
        ValueError: If input parameters are negative or invalid
    """
    # Input validation
    if any(val < 0 for val in [B, a, H]):
        raise ValueError("Input parameters must be non-negative")

    e = 0.63  # Discharge coefficient
    jc = 0.94  # Contraction coefficient
    g = 9.81  # Gravitational acceleration

    Q = e * jc * B * a * math.sqrt(2 * g * (H - e * a))
    return Q


def circular_culvert_flow(wc: float, a: float, H: float) -> float:
    """
    Calculate discharge flow through a circular culvert.

    Args:
        wc (float): Diameter of the culvert (meters)
        a (float): Height of the culvert opening (meters)
        H (float): Water head (meters)

    Returns:
        float: Discharge flow Q (cubic meters per second)

    Formula: Q = e * jc * wc * sqrt(2g * (H - e * a))
    Where:
    - e = 0.63 (discharge coefficient)
    - jc = 0.94 (contraction coefficient)
    - g = 9.81 (gravitational acceleration, m/s²)

    Raises:
        ValueError: If input parameters are negative or invalid
    """
    # Input validation
    if any(val < 0 for val in [wc, a, H]):
        raise ValueError("Input parameters must be non-negative")

    e = 0.63  # Discharge coefficient
    jc = 0.94  # Contraction coefficient
    g = 9.81  # Gravitational acceleration

    Q = e * jc * wc * math.sqrt(2 * g * (H - e * a))
    return Q


def gated_spillway_flow(B: float, a: float, H: float) -> float:
    """
    Calculate discharge flow through a gated spillway.

    Args:
        B (float): Width of the spillway (meters)
        a (float): Opening height of the gate (meters)
        H (float): Water head (meters)

    Returns:
        float: Discharge flow Q (cubic meters per second)

    Formula: Q = e * m * B * a * sqrt(2g * (H - e * a))
    Where:
    - e = 0.63 (discharge coefficient)
    - m = 0.94 (discharge coefficient)
    - g = 9.81 (gravitational acceleration, m/s²)

    Raises:
        ValueError: If input parameters are negative or invalid
    """
    # Input validation
    if any(val < 0 for val in [B, a, H]):
        raise ValueError("Input parameters must be non-negative")

    e = 0.63  # Discharge coefficient
    m = 0.94  # Discharge coefficient
    g = 9.81  # Gravitational acceleration

    Q = e * m * B * a * math.sqrt(2 * g * (H - e * a))
    return Q


def free_spillway_flow(B: float, H: float) -> float:
    """
    Calculate discharge flow through a free spillway (wide-crested weir).

    Args:
        B (float): Width of the spillway (meters)
        H (float): Water head (meters)

    Returns:
        float: Discharge flow Q (cubic meters per second)

    Formula: Q = m * B * sqrt(2g) * H^(3/2)
    Where:
    - m = 0.36 (discharge coefficient for wide-crested weir)
    - g = 9.81 (gravitational acceleration, m/s²)

    Raises:
        ValueError: If input parameters are negative or invalid
    """
    # Input validation
    if any(val < 0 for val in [B, H]):
        raise ValueError("Input parameters must be non-negative")

    m = 0.36  # Discharge coefficient for wide-crested weir
    g = 9.81  # Gravitational acceleration

    Q = m * B * math.sqrt(2 * g) * (H ** (3 / 2))
    return Q


FlowType = Literal["box", "circular", "gated", "free"]


def flow(
    water_level: float,
    elevation: float,
    height_or_diameter: float,
    opening_height: float,
    flow_type: FlowType,
) -> float:
    """
    Calculate the discharge flow based on different flow types and hydraulic conditions.

    This function determines the appropriate flow calculation method based on the water level,
    structure elevation, and specified flow type. It handles various hydraulic structures
    including box culverts, circular culverts, gated spillways, and free spillways.

    Args:
        water_level (float): Current water level (meters)
        elevation (float): Base elevation of the hydraulic structure (meters)
        height_or_diameter (float): Width (for box/gated) or diameter (for circular) of the structure (meters)
        opening_height (float): Height of the culvert or gate opening (meters)
        flow_type (Literal["box", "circular", "gated", "free"]): Type of hydraulic structure

    Returns:
        float: Discharge flow Q (cubic meters per second)
             Returns 0 if water level is below the structure's elevation

    Raises:
        ValueError: If an invalid flow_type is provided

    Notes:
    - If water head (H) is greater than 1.5 times the opening height, uses the specific
      flow calculation for the given structure type
    - If water head is less than 1.5 times the opening height, defaults to free spillway flow
    - Supports four flow types: box culvert, circular culvert, gated spillway, and free spillway
    """
    # Implementation follows the existing logic in the original function
    if water_level < elevation:
        return 0

    H = water_level - elevation
    B = height_or_diameter
    wc = height_or_diameter
    a = opening_height

    if H > 1.5 * a:
        if flow_type == "box":
            return box_culvert_flow(B, a, H)
        elif flow_type == "circular":
            return circular_culvert_flow(wc, a, H)
        elif flow_type == "gated":
            return gated_spillway_flow(B, a, H)
        elif flow_type == "free":
            return free_spillway_flow(B, H)
        else:
            raise ValueError("Invalid 'flow_type'")

    return free_spillway_flow(B, H)
