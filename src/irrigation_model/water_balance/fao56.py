"""FAO-56 compatibility adapter over the shared CAD/CRA/D/Ks core.

TAW maps to CAD, RAW maps to CRA, and Dr maps to D for Golden Case validation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .core import (
    actual_crop_evapotranspiration_mm,
    available_water_capacity_mm,
    crop_evapotranspiration_mm,
    management_capacity_mm,
    water_balance_step,
    water_stress_coefficient as core_water_stress_coefficient,
)


def total_available_water_mm(theta_fc: float, theta_wp: float, root_depth_m: float) -> float:
    """Return FAO-56 TAW [mm], implemented through the generic CAD equation."""
    return available_water_capacity_mm(theta_fc, theta_wp, root_depth_m * 100.0)


def readily_available_water_mm(taw_mm: float, depletion_fraction_p: float) -> float:
    """Return FAO-56 RAW [mm], implemented through generic CRA = fraction * CAD."""
    return management_capacity_mm(taw_mm, depletion_fraction_p)


def water_stress_coefficient(
    depletion_start_mm: float,
    taw_mm: float,
    depletion_fraction_p: float,
) -> float:
    """Return FAO-56 Ks through the shared CAD/CRA/D stress law."""
    raw_mm = readily_available_water_mm(taw_mm, depletion_fraction_p)
    return core_water_stress_coefficient(depletion_start_mm, taw_mm, raw_mm)


def adjusted_crop_evapotranspiration_mm(eto_mm: float, kc: float, ks: float) -> float:
    """Return FAO-style crop ET adjusted by Ks [mm]."""
    return actual_crop_evapotranspiration_mm(eto_mm, kc, ks)


@dataclass(frozen=True)
class RootZoneStep:
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
    raw_mm = readily_available_water_mm(taw_mm, depletion_fraction_p)
    step = water_balance_step(
        depletion_start_mm=depletion_start_mm,
        eto_mm=eto_mm,
        kc=kc,
        cad_mm=taw_mm,
        cra_mm=raw_mm,
        effective_precipitation_mm=precipitation_minus_runoff_mm,
        net_irrigation_mm=irrigation_net_mm,
        capillary_rise_mm=capillary_rise_mm,
        deep_percolation_mm=deep_percolation_mm,
    )
    return RootZoneStep(
        depletion_start_mm=step.depletion_start_mm,
        ks=step.ks,
        etc_potential_mm=step.etc_potential_mm,
        etc_adjusted_mm=step.etr_mm,
        depletion_end_mm=step.depletion_end_mm,
    )
