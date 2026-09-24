"""Generic root-zone water-deficit core.

The core uses project nomenclature (CAD, CRA, D, Ks) and is intentionally
agnostic about how the depletion fraction is obtained. FAO-56 and SBMI-style
parameterizations therefore share the same reservoir physics and stress law.
"""

from __future__ import annotations

from dataclasses import dataclass


def _require_range(name: str, value: float, lower: float, upper: float) -> None:
    if not lower <= value <= upper:
        raise ValueError(f"{name} must be between {lower} and {upper}; got {value}.")


def available_water_capacity_mm(
    theta_cc: float,
    theta_pmp: float,
    root_depth_cm: float,
) -> float:
    """Return CAD [mm] for volumetric water contents and root depth in cm."""
    _require_range("theta_cc", theta_cc, 0.0, 1.0)
    _require_range("theta_pmp", theta_pmp, 0.0, 1.0)
    if theta_cc < theta_pmp:
        raise ValueError("theta_cc must be greater than or equal to theta_pmp.")
    if root_depth_cm < 0:
        raise ValueError("root_depth_cm must be non-negative.")
    return (theta_cc - theta_pmp) * root_depth_cm * 10.0


def management_capacity_mm(cad_mm: float, depletion_fraction: float) -> float:
    """Return CRA [mm] from CAD and a methodology-specific depletion fraction."""
    if cad_mm < 0:
        raise ValueError("cad_mm must be non-negative.")
    _require_range("depletion_fraction", depletion_fraction, 0.0, 1.0)
    return depletion_fraction * cad_mm


def crop_evapotranspiration_mm(eto_mm: float, kc: float) -> float:
    """Return potential crop evapotranspiration ETc [mm]."""
    if eto_mm < 0 or kc < 0:
        raise ValueError("eto_mm and kc must be non-negative.")
    return eto_mm * kc


def water_stress_coefficient(
    depletion_mm: float,
    cad_mm: float,
    cra_mm: float,
) -> float:
    """Return shared piecewise-linear water-stress coefficient Ks.

    Ks = 1 while D <= CRA. Beyond CRA, Ks decreases linearly to zero at D=CAD.
    The threshold-generation method is intentionally external to this function.
    """
    if cad_mm <= 0:
        raise ValueError("cad_mm must be greater than zero.")
    if not 0.0 <= cra_mm <= cad_mm:
        raise ValueError("cra_mm must satisfy 0 <= cra_mm <= cad_mm.")
    if not 0.0 <= depletion_mm <= cad_mm:
        raise ValueError("depletion_mm must satisfy 0 <= depletion_mm <= cad_mm.")

    if depletion_mm <= cra_mm:
        return 1.0
    if cra_mm == cad_mm:
        return 1.0

    ks = (cad_mm - depletion_mm) / (cad_mm - cra_mm)
    return min(max(ks, 0.0), 1.0)


def actual_crop_evapotranspiration_mm(eto_mm: float, kc: float, ks: float) -> float:
    """Return actual crop evapotranspiration ETr [mm]."""
    _require_range("ks", ks, 0.0, 1.0)
    return crop_evapotranspiration_mm(eto_mm, kc) * ks


@dataclass(frozen=True)
class WaterBalanceStep:
    """Result of one root-zone water-deficit balance step."""

    depletion_start_mm: float
    cad_mm: float
    cra_mm: float
    ks: float
    etc_potential_mm: float
    etr_mm: float
    depletion_raw_mm: float
    depletion_end_mm: float
    surplus_water_mm: float
    unmet_depletion_mm: float


def water_balance_step(
    *,
    depletion_start_mm: float,
    eto_mm: float,
    kc: float,
    cad_mm: float,
    cra_mm: float,
    effective_precipitation_mm: float = 0.0,
    net_irrigation_mm: float = 0.0,
    capillary_rise_mm: float = 0.0,
    deep_percolation_mm: float = 0.0,
) -> WaterBalanceStep:
    """Advance depletion D by one time step.

    D* = D + ETr - Pe - IRN - CR + DP

    D is then bounded to [0, CAD]. Any negative raw depletion is exposed as
    surplus_water_mm; any raw depletion above CAD is exposed as
    unmet_depletion_mm. These diagnostics avoid silently hiding the effect of
    finite time-step clipping.
    """
    if not 0.0 <= depletion_start_mm <= cad_mm:
        raise ValueError("depletion_start_mm must satisfy 0 <= D <= CAD.")
    for name, value in (
        ("effective_precipitation_mm", effective_precipitation_mm),
        ("net_irrigation_mm", net_irrigation_mm),
        ("capillary_rise_mm", capillary_rise_mm),
        ("deep_percolation_mm", deep_percolation_mm),
    ):
        if value < 0:
            raise ValueError(f"{name} must be non-negative.")

    ks = water_stress_coefficient(depletion_start_mm, cad_mm, cra_mm)
    etc_potential = crop_evapotranspiration_mm(eto_mm, kc)
    etr = etc_potential * ks

    raw = (
        depletion_start_mm
        + etr
        - effective_precipitation_mm
        - net_irrigation_mm
        - capillary_rise_mm
        + deep_percolation_mm
    )
    surplus = max(-raw, 0.0)
    unmet = max(raw - cad_mm, 0.0)
    depletion_end = min(max(raw, 0.0), cad_mm)

    return WaterBalanceStep(
        depletion_start_mm=depletion_start_mm,
        cad_mm=cad_mm,
        cra_mm=cra_mm,
        ks=ks,
        etc_potential_mm=etc_potential,
        etr_mm=etr,
        depletion_raw_mm=raw,
        depletion_end_mm=depletion_end,
        surplus_water_mm=surplus,
        unmet_depletion_mm=unmet,
    )
