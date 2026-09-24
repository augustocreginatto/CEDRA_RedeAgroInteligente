"""Minimal FAO-56 root-zone water-balance implementation.

This module intentionally uses FAO-56 nomenclature (TAW, RAW, Dr, p) so that
published FAO examples can be reproduced without silently translating them to
SBMI/project terminology. Project-specific adapters can be added separately.

References
----------
Allen, R. G.; Pereira, L. S.; Raes, D.; Smith, M. (1998).
FAO Irrigation and Drainage Paper 56, Chapter 8.
https://www.fao.org/4/x0490e/x0490e0e.htm
"""

from __future__ import annotations

from dataclasses import dataclass


def _require_range(name: str, value: float, lower: float, upper: float) -> None:
    if not lower <= value <= upper:
        raise ValueError(f"{name} must be between {lower} and {upper}; got {value}.")


def total_available_water_mm(
    theta_fc: float,
    theta_wp: float,
    root_depth_m: float,
) -> float:
    """Return total available water (TAW) in the root zone [mm].

    FAO-56 Eq. 82: TAW = 1000 * (theta_FC - theta_WP) * Zr.
    """
    _require_range("theta_fc", theta_fc, 0.0, 1.0)
    _require_range("theta_wp", theta_wp, 0.0, 1.0)
    if theta_fc < theta_wp:
        raise ValueError("theta_fc must be greater than or equal to theta_wp.")
    if root_depth_m < 0:
        raise ValueError("root_depth_m must be non-negative.")
    return 1000.0 * (theta_fc - theta_wp) * root_depth_m


def readily_available_water_mm(taw_mm: float, depletion_fraction_p: float) -> float:
    """Return readily available water (RAW) [mm].

    FAO-56 Eq. 83: RAW = p * TAW.
    """
    if taw_mm < 0:
        raise ValueError("taw_mm must be non-negative.")
    _require_range("depletion_fraction_p", depletion_fraction_p, 0.0, 1.0)
    return depletion_fraction_p * taw_mm


def crop_evapotranspiration_mm(eto_mm: float, kc: float) -> float:
    """Return crop evapotranspiration without water stress [mm]."""
    if eto_mm < 0 or kc < 0:
        raise ValueError("eto_mm and kc must be non-negative.")
    return eto_mm * kc


def water_stress_coefficient(
    depletion_start_mm: float,
    taw_mm: float,
    depletion_fraction_p: float,
) -> float:
    """Return FAO-56 water stress coefficient Ks [-].

    Ks = 1 while Dr <= RAW. For Dr > RAW, FAO-56 Eq. 84 gives
    Ks = (TAW - Dr) / ((1 - p) * TAW).
    """
    if taw_mm <= 0:
        raise ValueError("taw_mm must be greater than zero.")
    _require_range("depletion_fraction_p", depletion_fraction_p, 0.0, 1.0)
    if depletion_fraction_p == 1.0:
        return 1.0 if depletion_start_mm <= taw_mm else 0.0

    dr = min(max(depletion_start_mm, 0.0), taw_mm)
    raw = readily_available_water_mm(taw_mm, depletion_fraction_p)
    if dr <= raw:
        return 1.0

    ks = (taw_mm - dr) / ((1.0 - depletion_fraction_p) * taw_mm)
    return min(max(ks, 0.0), 1.0)


def adjusted_crop_evapotranspiration_mm(
    eto_mm: float,
    kc: float,
    ks: float,
) -> float:
    """Return single-Kc crop ET adjusted for water stress [mm]."""
    _require_range("ks", ks, 0.0, 1.0)
    return crop_evapotranspiration_mm(eto_mm, kc) * ks


@dataclass(frozen=True)
class RootZoneStep:
    """Result of one FAO-56 root-zone balance step."""

    depletion_start_mm: float
    ks: float
    etc_potential_mm: float
    etc_adjusted_mm: float
    depletion_end_mm: float


def root_zone_balance_step(
    *,
    depletion_start_mm: float,
    eto_mm: float,
    kc: float,
    taw_mm: float,
    depletion_fraction_p: float,
    precipitation_minus_runoff_mm: float = 0.0,
    irrigation_net_mm: float = 0.0,
    capillary_rise_mm: float = 0.0,
    deep_percolation_mm: float = 0.0,
) -> RootZoneStep:
    """Advance the FAO-56 root-zone depletion by one time step.

    The balance follows FAO-56 Eq. 85. Water stress is evaluated from the
    depletion at the start of the step. This directly reproduces Example 37,
    where precipitation, irrigation, capillary rise and deep percolation are
    all zero.

    More detailed event timing (e.g. early-day irrigation as in Example 38)
    will be implemented separately rather than hidden in this core function.
    """
    for name, value in (
        ("precipitation_minus_runoff_mm", precipitation_minus_runoff_mm),
        ("irrigation_net_mm", irrigation_net_mm),
        ("capillary_rise_mm", capillary_rise_mm),
        ("deep_percolation_mm", deep_percolation_mm),
    ):
        if value < 0:
            raise ValueError(f"{name} must be non-negative.")

    dr_start = min(max(depletion_start_mm, 0.0), taw_mm)
    ks = water_stress_coefficient(dr_start, taw_mm, depletion_fraction_p)
    etc_potential = crop_evapotranspiration_mm(eto_mm, kc)
    etc_adjusted = etc_potential * ks

    dr_end = (
        dr_start
        - precipitation_minus_runoff_mm
        - irrigation_net_mm
        - capillary_rise_mm
        + etc_adjusted
        + deep_percolation_mm
    )
    dr_end = min(max(dr_end, 0.0), taw_mm)

    return RootZoneStep(
        depletion_start_mm=dr_start,
        ks=ks,
        etc_potential_mm=etc_potential,
        etc_adjusted_mm=etc_adjusted,
        depletion_end_mm=dr_end,
    )
