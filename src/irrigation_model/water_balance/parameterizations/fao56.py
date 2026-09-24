"""FAO-56 parameterization of the shared CAD/CRA/D/Ks core."""

from __future__ import annotations


def adjusted_depletion_fraction(p_table: float, etc_mm_day: float) -> float:
    """Return FAO-56 adjusted depletion fraction p.

    p = p_table + 0.04 * (5 - ETc), bounded to [0.1, 0.8].
    """
    if not 0.0 <= p_table <= 1.0:
        raise ValueError("p_table must be between 0 and 1.")
    if etc_mm_day < 0:
        raise ValueError("etc_mm_day must be non-negative.")
    p = p_table + 0.04 * (5.0 - etc_mm_day)
    return min(max(p, 0.1), 0.8)
