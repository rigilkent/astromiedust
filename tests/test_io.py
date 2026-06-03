from types import SimpleNamespace

import numpy as np
import pickle
import pytest

from astromiedust import OpticalModel, SystemResult


def test_save_beta_csv_defaults_to_existing_two_columns(tmp_path):
    prtl = SimpleNamespace(
        diams=np.array([1.0, 2.0]),
        betas=np.array([0.1, 0.2]),
        Qpr_star_avg=np.array([0.7, 0.8]),
    )
    file_name = tmp_path / "beta.csv"

    SystemResult(prtl=prtl).save_beta_csv(file_name)

    lines = file_name.read_text().splitlines()
    assert lines[0] == "# diameter_um, beta"
    assert lines[1] == "1.0000000e+00, 1.0000000e-01"
    assert [idx for idx, char in enumerate(lines[0]) if char == ","] == [
        idx for idx, char in enumerate(lines[1]) if char == ","
    ]
    assert np.loadtxt(file_name, delimiter=",", comments="#").shape == (2, 2)


def test_save_beta_csv_can_include_qpr_star_avg(tmp_path):
    prtl = SimpleNamespace(
        diams=np.array([1.0, 2.0]),
        betas=np.array([0.1, 0.2]),
        Qpr_star_avg=np.array([0.7, 0.8]),
    )
    file_name = tmp_path / "beta.csv"

    SystemResult(prtl=prtl).save_beta_csv(file_name, include_Qpr_star_avg=True)

    lines = file_name.read_text().splitlines()
    assert lines[0] == "# diameter_um, beta,          Qpr_star_avg"
    assert lines[1] == "1.0000000e+00, 1.0000000e-01, 7.0000000e-01"
    assert lines[0].split(",")[1].strip() == "beta"
    np.testing.assert_allclose(
        np.loadtxt(file_name, delimiter=",", comments="#"),
        np.array([[1.0, 0.1, 0.7], [2.0, 0.2, 0.8]]),
    )


def test_save_beta_csv_requires_qpr_star_avg_when_requested(tmp_path):
    prtl = SimpleNamespace(
        diams=np.array([1.0, 2.0]),
        betas=np.array([0.1, 0.2]),
    )

    with pytest.raises(ValueError, match="Qpr_star_avg is required"):
        SystemResult(prtl=prtl).save_beta_csv(
            tmp_path / "beta.csv",
            include_Qpr_star_avg=True,
        )


def test_optical_model_alias_remains_available():
    assert OpticalModel is SystemResult


def test_optical_model_pickle_name_remains_loadable():
    old_pickle = (
        b"castromiedust.io\n"
        b"OpticalModel\n"
        b"p0\n"
        b")\x81p1\n"
        b"(dp2\n"
        b"Vstar\n"
        b"p3\n"
        b"NsVprtl\n"
        b"p4\n"
        b"Nsb."
    )

    result = pickle.loads(old_pickle)

    assert isinstance(result, SystemResult)
    assert result.star is None
    assert result.prtl is None
