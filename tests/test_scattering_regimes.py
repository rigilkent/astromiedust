import numpy as np

import astrodust_optprops as opt
from astrodust_optprops import optics_core as core


def test_long_wavelength_large_grains_use_geometric_optics():
    matrl = opt.Material(qsil=0.5, qice=0.5, mpor=0.5)
    wavs = np.linspace(matrl.wavs[-1] * 1.01, 1.0e4, 8)
    diam = 1.0e7

    q = core.calculate_scatt_efficiency_coeffs(wavs, diam, matrl)

    for values in q.values():
        assert np.all(np.isfinite(values))

    assert not np.allclose(q["abs"], 1.0)
    assert not np.allclose(q["pr"], 1.0)
    assert not np.allclose(q["sca"], 1.0)
