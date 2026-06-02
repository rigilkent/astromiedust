# Getting Started

## Install

From a checkout of the repository:

```bash
python -m pip install -e .
```

## Workflow Overview

The package works with plain NumPy arrays for the main grids. Wavelengths and
particle diameters are in microns (`um`), distances are in astronomical units
(`au`), stellar luminosity and mass are in solar units, and temperatures are in
Kelvin.

Most scripts follow the same pattern:

1. Build a `Star`.
2. Build a `Material`.
3. Choose wavelength, particle-diameter, and distance grids.
4. Build `Particles`.
5. Run `Particles.calculate_all(star)`.
6. Save or plot the outputs.

```python
# Example
import astromiedust as amd

star = amd.Star(name="Sun")
matrl = amd.Material(qsil=0.5)
prtl = amd.Particles(diams=diams, wavs=wavs, dists=dists, matrl=matrl)
prtl.calculate_all(star)
```

For larger calculations, choose grids that cover the wavelengths, particle
sizes, and distances relevant to the system being modeled.

For a complete example, see the [Fomalhaut example](examples/fomalhaut.md).

## Main Objects

`Star` describes the illuminating star. It can use a blackbody temperature, a
two-column spectrum file, spectrum arrays with `astropy` units, or the built-in
Sun default.

`Material` builds a composite dielectric function from silicate, refractory
carbonaceous material, water ice, and vacuum.

`Particles` stores the requested particle size, wavelength, and distance grids
and performs the optical and thermal calculations.

`OpticalModel` is a lightweight container for saving and loading a completed
star plus particle calculation.

## What `calculate_all` Fills

After `calculate_all`, common result arrays are available on the `Particles`
object:

| Attribute | Meaning | Shape |
| --- | --- | --- |
| `Qabs` | absorption efficiency | `(n_diams, n_wavs)` |
| `Qsca` | scattering efficiency | `(n_diams, n_wavs)` |
| `Qpr` | radiation-pressure efficiency | `(n_diams, n_wavs)` |
| `g` | scattering asymmetry factor | `(n_diams, n_wavs)` |
| `temps` | equilibrium temperature in K | `(n_dists, n_diams)` |
| `Qpr_star_avg` | stellar-spectrum-averaged `Qpr` | `(n_diams,)` |
| `betas` | radiation pressure to gravity ratio | `(n_diams,)` |
| `diams_blow` | beta = 0.5 blowout diameter interval, in um | tuple `(lower, upper)` |
| `bnus` | blackbody spectral radiance, default `Jy/sr` | `(n_dists, n_diams, n_wavs)` |

`Particles.calculate_all(star)` runs the common full workflow: scattering
coefficients, equilibrium temperatures, beta factors, blowout diameters, and
blackbody spectral radiance on the requested wavelength grid.

`diams_blow` is a two-value interval because beta can exceed the blowout
threshold across a finite range of grain sizes. A lower value of `0` means the
blowout interval extends down to the smallest sizes considered by the search;
`(None, None)` means no blowout interval was found.

You can also run pieces of the workflow directly when you only need part of the
calculation:

```python
# Example
prtl.calculate_scattering_properties()
prtl.calculate_temperatures(star)
prtl.calculate_beta_factors(star)
prtl.calculate_blowout_diameters(star)
```

`calculate_temperatures` and `calculate_all` require `dists` to be set.

## Plotting

The main classes include Matplotlib helpers:

```python
# Example
star.plot_spectrum()
prtl.plot_Q(Q_type="abs")
prtl.plot_Q(Q_type="sca")
prtl.plot_Q(Q_type="pr")
prtl.plot_g()
prtl.plot_beta()
prtl.plot_temp()
```

These methods return the Matplotlib axes so scripts can adjust labels, limits,
or save figures.
