import numpy as np
import pytest
import astropy.units as u

import astromiedust as opt


def test_custom_spectrum_flux_is_zero_outside_wavelength_range():
    star = opt.Star(
        name="PeakedSpectrum",
        lum_suns=1.0,
        mass_suns=1.0,
        spectrum_wavs=np.array([1.0, 2.0, 3.0]) * u.um,
        spectrum_flux=np.array([1e-20, 1.0, 1e-20]) * u.W / u.m**2 / u.um,
        verbose=False,
    )

    flux = star.get_spectral_flux_density(np.array([0.5, 2.0, 4.0]))

    assert flux[0] == pytest.approx(1e-50)
    assert flux[1] == pytest.approx(1.0)
    assert flux[2] == pytest.approx(1e-50)


def test_custom_spectrum_warns_when_edges_are_bright():
    with pytest.warns(UserWarning, match="may not cover the full luminosity"):
        opt.Star(
            name="TruncatedSpectrum",
            lum_suns=1.0,
            mass_suns=1.0,
            spectrum_wavs=np.array([1.0, 2.0, 3.0]) * u.um,
            spectrum_flux=np.array([1.0, 1.0, 1.0]) * u.W / u.m**2 / u.um,
            verbose=False,
        )
