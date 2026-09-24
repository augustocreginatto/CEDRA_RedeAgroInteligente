import json
from pathlib import Path

import pytest

from irrigation_model.water_balance import (
    readily_available_water_mm,
    root_zone_balance_step,
    total_available_water_mm,
)

DATA = Path(__file__).parents[3] / "data" / "validation" / "fao56" / "example_37.json"


def test_fao56_example_37_reproduces_water_stress_sequence():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    inputs = payload["inputs"]
    expected = payload["expected"]

    taw = total_available_water_mm(inputs["theta_fc"], inputs["theta_wp"], inputs["zr_m"])
    raw = readily_available_water_mm(taw, inputs["p"])

    assert taw == pytest.approx(expected["taw_mm"], abs=1e-12)
    assert raw == pytest.approx(expected["raw_mm"], abs=1e-12)

    depletion = inputs["initial_depletion_mm"]
    for row in expected["table"]:
        step = root_zone_balance_step(
            depletion_start_mm=depletion,
            eto_mm=inputs["eto_mm_day"],
            kc=inputs["kc"],
            taw_mm=taw,
            depletion_fraction_p=inputs["p"],
        )

        # The FAO table is rounded to 2 decimals for Ks and 0.1 mm for ET/depletion.
        assert step.depletion_start_mm == pytest.approx(row["dr_start_mm"], abs=0.11)
        assert step.ks == pytest.approx(row["ks"], abs=0.011)
        assert step.etc_adjusted_mm == pytest.approx(row["etc_adj_mm"], abs=0.11)
        assert step.depletion_end_mm == pytest.approx(row["dr_end_mm"], abs=0.11)

        depletion = step.depletion_end_mm
