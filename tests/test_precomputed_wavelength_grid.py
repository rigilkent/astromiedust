import numpy as np

import astromiedust as amd


def test_precomputed_grid_covers_requested_wavelengths_below_default():
    wavs = np.array([0.05, 0.2])
    diams = np.array([1.0])
    matrl = amd.Material(qsil=0.5, qice=0.5, mpor=0.5)

    precomputed = amd.Particles(
        diams=diams,
        wavs=wavs,
        matrl=matrl,
        precompute_Qs=True,
        show_progress=False,
    )
    direct = amd.Particles(
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
    matrl = amd.Material(qsil=0.5, qice=0.5, mpor=0.5)
    star = amd.Star(name="HotStar", lum_suns=1.0, mass_suns=1.0, temp=50000.0)

    particles = amd.Particles(
        diams=diams,
        wavs=wavs,
        matrl=matrl,
        dists=dists,
        precompute_Qs=True,
        show_progress=False,
    )

    integration_wav_min = 289.8 / star.temp
    assert particles.precomputed_wavs is None

    particles.calculate_temperatures(star)

    assert particles.precomputed_wavs[0] <= integration_wav_min
    assert np.all(np.isfinite(particles.temps))


def test_precomputed_diameter_extrapolation_falls_back_to_direct_calculation():
    wavs = np.array([0.2, 2.0])
    matrl = amd.Material(qsil=0.5, qice=0.5, mpor=0.5)

    precomputed = amd.Particles(
        diams=np.array([1.0, 1000.0]),
        wavs=wavs,
        matrl=matrl,
        precompute_Qs=True,
        show_progress=False,
    )
    direct = amd.Particles(
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
    matrl = amd.Material(qsil=0.5, qice=0.5, mpor=0.5)

    particles = amd.Particles(
        diams=np.array([1.0]),
        wavs=wavs,
        matrl=matrl,
        precompute_Qs=True,
        show_progress=False,
    )

    qpr = particles.get_Q_interpolator(0.1, "pr")(wavs)

    assert np.all(np.isfinite(qpr))
    assert np.all(qpr >= 0)


def test_temperature_calculation_expands_precomputed_grid_once_for_cold_dust():
    wavs = np.array([1.0, 10.0])
    diams = np.array([1.0])
    dists = np.array([1000.0])
    matrl = amd.Material(qsil=0.5, qice=0.5, mpor=0.5)
    star = amd.Star(name="Solar", lum_suns=1.0, mass_suns=1.0, temp=5800.0)

    particles = amd.Particles(
        diams=diams,
        wavs=wavs,
        matrl=matrl,
        dists=dists,
        precompute_Qs=True,
        show_progress=False,
    )

    precompute_calls = []
    original_precompute = particles._precompute_coefficients

    def counted_precompute():
        precompute_calls.append(None)
        return original_precompute()

    particles._precompute_coefficients = counted_precompute

    particles.calculate_temperatures(star)

    assert len(precompute_calls) <= 1
    assert np.all(np.isfinite(particles.temps))


def test_calculate_all_precomputes_q_grid_once():
    wavs = np.array([1.0, 10.0])
    diams = np.array([1.0])
    dists = np.array([1000.0])
    matrl = amd.Material(qsil=0.5, qice=0.5, mpor=0.5)
    star = amd.Star(name="Solar", lum_suns=1.0, mass_suns=1.0, temp=5800.0)

    particles = amd.Particles(
        diams=diams,
        wavs=wavs,
        matrl=matrl,
        dists=dists,
        precompute_Qs=True,
        show_progress=False,
    )

    precompute_calls = []
    original_precompute = particles._precompute_coefficients

    def counted_precompute():
        precompute_calls.append(None)
        return original_precompute()

    particles._precompute_coefficients = counted_precompute

    particles.calculate_all(star)

    assert len(precompute_calls) == 1
    assert np.all(np.isfinite(particles.temps))
    assert np.all(np.isfinite(particles.Qabs))


def test_luminous_star_cold_grains_do_not_rebuild_temperature_q_grid():
    wavs = np.logspace(-1.5, 3.0, 60)
    diams = np.logspace(-1.0, 4.0, 8)
    dists = np.logspace(0.0, 3.0, 8)
    matrl = amd.Material(qsil=1.0, qice=1.0, mpor=1.0)
    star = amd.Star(name="VegaLike", lum_suns=46.5, mass_suns=2.15, temp=8902.0)

    particles = amd.Particles(
        diams=diams,
        wavs=wavs,
        matrl=matrl,
        dists=dists,
        precompute_Qs=True,
        show_progress=False,
    )

    precompute_calls = []
    original_precompute = particles._precompute_coefficients

    def counted_precompute():
        precompute_calls.append(None)
        return original_precompute()

    particles._precompute_coefficients = counted_precompute

    particles.calculate_all(star)

    assert len(precompute_calls) == 1
    assert np.all(np.isfinite(particles.temps))


def test_mie_resonance_suppression_floors_nonpositive_efficiencies():
    matrl = amd.Material(qsil=1.0, qice=1.0, mpor=1.0)
    particles = amd.Particles(
        diams=np.array([0.1]),
        wavs=np.array([9.0]),
        matrl=matrl,
        suppress_mie_resonance=True,
        show_progress=False,
    )
    particles.precomputed_wavs = np.array([9.0, 10.0])

    def fake_coefficients_for_diameters(diameters):
        n_diams = len(diameters)
        qabs = np.tile(np.array([-1e-8, 1e-6]), (n_diams, 1))
        qpr = np.tile(np.array([0.0, 1e-6]), (n_diams, 1))
        qsca = np.tile(np.array([1e-12, 1e-6]), (n_diams, 1))
        g = np.zeros_like(qabs)
        return qabs, qpr, qsca, g

    particles._compute_coefficients_for_diameters = fake_coefficients_for_diameters

    particles._precompute_coefficients()

    assert np.all(np.isfinite(particles.precomputed_Qabs[0.1]))
    assert np.all(np.isfinite(particles.precomputed_Qpr[0.1]))
    assert np.all(particles.precomputed_Qabs[0.1] > 0)
    assert np.all(particles.precomputed_Qpr[0.1] > 0)
