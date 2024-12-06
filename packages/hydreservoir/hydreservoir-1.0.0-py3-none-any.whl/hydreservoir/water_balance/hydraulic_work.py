from dataclasses import dataclass


@dataclass
class HydraulicWork:
    elevation: float
    height_or_diameter: float
    
