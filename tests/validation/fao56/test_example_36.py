import json
from pathlib import Path

import pytest

from irrigation_model.water_balance import available_water_capacity_mm, management_capacity_mm

DATA = Path(__file__).parents[3] / "data" / "validation" / "fao56" / "example_36.json"


def test_fao56_example_36_with_shared_cad_cra_core():
    payload = json.loads(DATA.read_text(encoding="utf-8"))

    for case in payload["cases"]:
        cad = available_water_capacity_mm(
            case["theta_fc"], case["theta_wp"], case["zr_m"] * 100.0
        )
        cra = management_capacity_mm(cad, case["p"])

        assert cad == pytest.approx(case["taw_mm"], abs=0.51)
        assert cra == pytest.approx(case["raw_mm"], abs=0.51)
