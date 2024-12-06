import math
from typing import Tuple

def py_str_to_bool(s: str) -> bool:
    """Python implementation of string to boolean conversion"""
    s = s.lower()
    if s in ('true', '1', 'yes', 'y', 'on'):
        return True
    if s in ('false', '0', 'no', 'n', 'off'):
        return False
    raise ValueError(f"Cannot convert '{s}' to bool")

def py_point3d_distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """Python implementation of 3D point distance calculation"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return math.sqrt((dx * dx) + (dy * dy) + (dz * dz))
