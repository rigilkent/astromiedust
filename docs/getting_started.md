# Getting Started

## Install

From a checkout of the repository:

```bash
python -m pip install -e .
```

For local documentation work:

```bash
python -m pip install -e ".[docs]"
```

## Minimal example

The package works with plain NumPy arrays for the main grids. Wavelengths and
particle diameters are in microns (`um`), distances are in astronomical units
(`au`), stellar luminosity and mass are in solar units, and temperatures are in
Kelvin.

```python
import numpy as np
import astromiedust as opt

star = opt.Star(name="Sun", lum_suns=1.0, mass_suns=1.0)
matrl = opt.Material()

wavs = np.logspace(-1, 3, 120)
diams = np.logspace(-1, 2, 20)
dists = np.array([1.0, 10.0, 100.0])

prtl = opt.Particles(
    diams=diams,
    wavs=wavs,
    dists=dists,
    matrl=matrl,
    show_progress=False,
)
prtl.calculate_all(star)

print(prtl.Qabs)   # shape: (n_diams, n_wavs)
print(prtl.temps)  # shape: (n_dists, n_diams)
print(prtl.betas)  # shape: (n_diams,)
```

## Main objects

`Star` describes the illuminating star. It can use a blackbody temperature, a
two-column spectrum file, spectrum arrays with `astropy` units, or the built-in
Sun default.

`Material` builds a composite dielectric function from silicate, refractory
carbonaceous material, water ice, and vacuum.

`Particles` stores the requested particle size, wavelength, and distance grids
and performs the optical and thermal calculations.

`OpticalModel` is a lightweight container for saving and loading a completed
star plus particle calculation.
