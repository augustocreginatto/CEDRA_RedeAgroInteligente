import pytest

from irrigation_model.water_balance import management_capacity_mm, water_stress_coefficient
from irrigation_model.water_balance.parameterizations import (
    fao56_adjusted_depletion_fraction,
    sbmi_depletion_fraction_f,
)


def test_fao56_and_sbmi_parameterizations_change_threshold_not_core():
    cad = 100.0
    etc = 6.37

    p_fao56 = fao56_adjusted_depletion_fraction(0.50, etc)
    f_sbmi = sbmi_depletion_fraction_f(4, etc)

    assert p_fao56 == pytest.approx(0.4452)
    assert f_sbmi == pytest.approx(0.5315)

    cra_fao56 = management_capacity_mm(cad, p_fao56)
    cra_sbmi = management_capacity_mm(cad, f_sbmi)

    assert cra_fao56 == pytest.approx(44.52)
    assert cra_sbmi == pytest.approx(53.15)

    d = 50.0
    ks_fao56 = water_stress_coefficient(d, cad, cra_fao56)
    ks_sbmi = water_stress_coefficient(d, cad, cra_sbmi)

    assert ks_fao56 == pytest.approx(50.0 / 55.48)
    assert ks_sbmi == pytest.approx(1.0)
