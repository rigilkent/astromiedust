import numpy as np

import astrodust_optprops as opt


def test_precomputed_grid_covers_requested_wavelengths_below_default():
    wavs = np.array([0.05, 0.2])
    diams = np.array([1.0])
    matrl = opt.Material(qsil=0.5, qice=0.5, mpor=0.5)

    precomputed = opt.Particles(
        diams=diams,
        wavs=wavs,
        matrl=matrl,
        precompute_Qs=True,
        show_progress=False,
    )
    direct = opt.Particles(
        diams=diams,
        wavs=wavs,
        matrl=matrl,
        precompute_Qs=False,
        show_progress=False,
    )

    precomputed.calculate_scattering_properties()
    direct.calculate_scattering_properties()

    assert precomputed.precomputed_wavs[0] <= wavs.min()
    np.testing.assert_allclose(precomputed.Qabs, direct.Qabs, rtol=0.05)
    np.testing.assert_allclose(precomputed.Qpr, direct.Qpr, rtol=0.05)


def test_precomputed_grid_expands_for_hot_star_integration_wavelengths():
    wavs = np.array([0.2, 2.0])
    diams = np.array([1.0])
    dists = np.array([1.0])
    matrl = opt.Material(qsil=0.5, qice=0.5, mpor=0.5)
    star = opt.Star(name="HotStar", lum_suns=1.0, mass_suns=1.0, temp=50000.0)

    particles = opt.Particles(
        diams=diams,
        wavs=wavs,
        matrl=matrl,
        dists=dists,
        precompute_Qs=True,
        show_progress=False,
    )

    integration_wav_min = 289.8 / star.temp
    assert particles.precomputed_wavs[0] > integration_wav_min

    particles.calculate_temperatures(star)

    assert particles.precomputed_wavs[0] <= integration_wav_min
    assert np.all(np.isfinite(particles.temps))


def test_precomputed_diameter_extrapolation_falls_back_to_direct_calculation():
    wavs = np.array([0.2, 2.0])
    matrl = opt.Material(qsil=0.5, qice=0.5, mpor=0.5)

    precomputed = opt.Particles(
        diams=np.array([1.0, 1000.0]),
        wavs=wavs,
        matrl=matrl,
        precompute_Qs=True,
        show_progress=False,
    )
    direct = opt.Particles(
        diams=np.array([0.01]),
        wavs=wavs,
        matrl=matrl,
        precompute_Qs=False,
        show_progress=False,
    )

    qabs = precomputed.get_Q_interpolator(0.01, "abs")(wavs)
    direct.calculate_scattering_properties()

    np.testing.assert_allclose(qabs, direct.Qabs[0], rtol=0.05)


def test_precomputed_single_diameter_table_can_evaluate_other_diameters():
    wavs = np.array([0.2, 2.0])
    matrl = opt.Material(qsil=0.5, qice=0.5, mpor=0.5)

    particles = opt.Particles(
        diams=np.array([1.0]),
        wavs=wavs,
        matrl=matrl,
        precompute_Qs=True,
        show_progress=False,
    )

    qpr = particles.get_Q_interpolator(0.1, "pr")(wavs)

    assert np.all(np.isfinite(qpr))
    assert np.all(qpr >= 0)
