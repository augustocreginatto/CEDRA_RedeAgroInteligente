import json
from pathlib import Path

import pytest

from irrigation_model.water_balance import (
    readily_available_water_mm,
    total_available_water_mm,
)

DATA = Path(__file__).parents[3] / "data" / "validation" / "fao56" / "example_36.json"


def test_fao56_example_36_reproduces_published_taw_and_raw():
    payload = json.loads(DATA.read_text(encoding="utf-8"))

    for case in payload["cases"]:
        taw = total_available_water_mm(case["theta_fc"], case["theta_wp"], case["zr_m"])
        raw = readily_available_water_mm(taw, case["p"])

        assert taw == pytest.approx(case["taw_mm"], abs=0.51)
        assert raw == pytest.approx(case["raw_mm"], abs=0.51)
