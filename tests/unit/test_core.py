import pytest

from irrigation_model.water_balance import (
    available_water_capacity_mm,
    management_capacity_mm,
    water_balance_step,
    water_stress_coefficient,
)


def test_cad_and_cra_are_generic_reservoir_quantities():
    cad = available_water_capacity_mm(0.32, 0.12, 80.0)
    cra = management_capacity_mm(cad, 0.40)
    assert cad == pytest.approx(160.0)
    assert cra == pytest.approx(64.0)


def test_shared_stress_law_uses_only_d_cad_and_cra():
    assert water_stress_coefficient(55.0, 160.0, 64.0) == pytest.approx(1.0)
    assert water_stress_coefficient(67.0, 160.0, 64.0) == pytest.approx(93.0 / 96.0)
    assert water_stress_coefficient(160.0, 160.0, 64.0) == pytest.approx(0.0)


def test_balance_exposes_surplus_instead_of_hiding_negative_depletion():
    step = water_balance_step(
        depletion_start_mm=5.0,
        eto_mm=0.0,
        kc=1.0,
        cad_mm=100.0,
        cra_mm=50.0,
        effective_precipitation_mm=8.0,
    )
    assert step.depletion_end_mm == pytest.approx(0.0)
    assert step.surplus_water_mm == pytest.approx(3.0)
