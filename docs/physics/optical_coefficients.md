# Optical Coefficients

`Particles.calculate_scattering_properties()` computes four wavelength-dependent
quantities for each particle diameter:

- `Qabs`: absorption efficiency
- `Qsca`: scattering efficiency
- `Qpr`: radiation-pressure efficiency
- `g`: scattering asymmetry factor

The arrays use shape `(n_diams, n_wavs)`.

```python
prtl.calculate_scattering_properties()

qabs_for_first_size = prtl.Qabs[0]
```

The lower-level routines choose between Mie theory, Rayleigh-Gans theory, and
geometric optics according to the wavelength, particle size, and material
properties. For user scripts, the main entry point is the `Particles` class
rather than the lower-level `optics_core` functions.

When `precompute_Qs=True`, coefficient tables are precomputed on a wavelength
grid and interpolated where needed for integrations. This is the default. It is
also required when Mie resonance averaging is enabled with
`suppress_mie_resonance=True`.
