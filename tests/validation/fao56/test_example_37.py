import json
from pathlib import Path

import pytest

from irrigation_model.water_balance import (
    available_water_capacity_mm,
    management_capacity_mm,
    water_balance_step,
)

DATA = Path(__file__).parents[3] / "data" / "validation" / "fao56" / "example_37.json"


def test_fao56_example_37_with_shared_cad_cra_d_ks_core():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    inputs = payload["inputs"]
    expected = payload["expected"]

    cad = available_water_capacity_mm(
        inputs["theta_fc"], inputs["theta_wp"], inputs["zr_m"] * 100.0
    )
    cra = management_capacity_mm(cad, inputs["p"])

    assert cad == pytest.approx(expected["taw_mm"], abs=1e-12)
    assert cra == pytest.approx(expected["raw_mm"], abs=1e-12)

    depletion = inputs["initial_depletion_mm"]
    for row in expected["table"]:
        step = water_balance_step(
            depletion_start_mm=depletion,
            eto_mm=inputs["eto_mm_day"],
            kc=inputs["kc"],
            cad_mm=cad,
            cra_mm=cra,
        )

        assert step.depletion_start_mm == pytest.approx(row["dr_start_mm"], abs=0.11)
        assert step.ks == pytest.approx(row["ks"], abs=0.011)
        assert step.etr_mm == pytest.approx(row["etc_adj_mm"], abs=0.11)
        assert step.depletion_end_mm == pytest.approx(row["dr_end_mm"], abs=0.11)

        depletion = step.depletion_end_mm
