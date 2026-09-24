"""SBMI-compatible depletion-fraction parameterization used by this project.

The table below is the group x ETc_max table documented in the project
materials. This module does not claim that every SBMI configuration uses this
single parameterization or a single Ks formulation.
"""

from __future__ import annotations

ETC_MAX_GRID_MM_DAY = (2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)

F_TABLE = {
    1: (0.500, 0.425, 0.350, 0.300, 0.250, 0.225, 0.200, 0.200, 0.175),
    2: (0.675, 0.575, 0.475, 0.400, 0.350, 0.325, 0.275, 0.250, 0.225),
    3: (0.800, 0.700, 0.600, 0.500, 0.450, 0.425, 0.375, 0.350, 0.300),
    4: (0.875, 0.800, 0.700, 0.600, 0.550, 0.500, 0.450, 0.425, 0.400),
}


def depletion_fraction_f(crop_group: int, etc_max_mm_day: float) -> float:
    """Return F by exact lookup or linear interpolation within 2..10 mm/day."""
    if crop_group not in F_TABLE:
        raise ValueError("crop_group must be one of 1, 2, 3, or 4.")
    if not ETC_MAX_GRID_MM_DAY[0] <= etc_max_mm_day <= ETC_MAX_GRID_MM_DAY[-1]:
        raise ValueError("etc_max_mm_day must be within the documented table range 2..10.")

    values = F_TABLE[crop_group]
    for i, x in enumerate(ETC_MAX_GRID_MM_DAY):
        if etc_max_mm_day == x:
            return values[i]
        if etc_max_mm_day < x:
            x0 = ETC_MAX_GRID_MM_DAY[i - 1]
            x1 = x
            y0 = values[i - 1]
            y1 = values[i]
            return y0 + (etc_max_mm_day - x0) * (y1 - y0) / (x1 - x0)

    return values[-1]
