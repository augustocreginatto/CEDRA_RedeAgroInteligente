"""Method-specific parameterizations for the shared water-balance core."""

from .fao56 import adjusted_depletion_fraction as fao56_adjusted_depletion_fraction
from .sbmi import depletion_fraction_f as sbmi_depletion_fraction_f

__all__ = [
    "fao56_adjusted_depletion_fraction",
    "sbmi_depletion_fraction_f",
]
