import numpy as np
import pytest

import astromiedust as amd


@pytest.mark.parametrize(
    "kwargs",
    [
        {"qsil": -0.1},
        {"qsil": 1.1},
        {"qice": -0.1},
        {"qice": 1.1},
        {"mpor": -0.1},
        {"mpor": 1.1},
        {"qsil": np.nan},
        {"qice": np.inf},
        {"mpor": [0.5]},
    ],
)
def test_material_rejects_invalid_fractions(kwargs):
    with pytest.raises(ValueError):
        amd.Material(**kwargs)


@pytest.mark.parametrize("refmed", [0.0, -1.0, np.nan, np.inf, [1.0]])
def test_material_rejects_invalid_refmed(refmed):
    with pytest.raises(ValueError):
        amd.Material(refmed=refmed)


def test_material_rejects_pure_vacuum_composition():
    with pytest.raises(ValueError, match="density must be positive"):
        amd.Material(qsil=0.0, qice=0.0, mpor=1.0)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"qsil": 1.0, "qice": 1.0, "mpor": 0.0},
        {"qsil": 0.0, "qice": 1.0, "mpor": 0.0},
        {"qsil": 1.0, "qice": 1.0, "mpor": 1.0},
        {"qsil": 0.0, "qice": 0.8, "mpor": 1.0},
    ],
)
def test_material_accepts_valid_edge_compositions(kwargs):
    matrl = amd.Material(**kwargs)

    assert np.isfinite(matrl.density)
    assert matrl.density > 0.0
