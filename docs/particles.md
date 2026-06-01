# Particles

`Particles` holds the particle grids and calculated optical and thermal
properties.

```python
import numpy as np
import astromiedust as opt

matrl = opt.Material()

prtl = opt.Particles(
    diams=np.logspace(-1, 3, 60),  # um
    wavs=np.logspace(-1, 4, 300),  # um
    dists=np.logspace(0, 3, 40),   # au
    matrl=matrl,
    suppress_mie_resonance=True,
)
```

`diams` may also be an `astropy` quantity convertible to `um`. Other grids are
normally plain arrays in the units shown above.

## Calculation methods

For the standard full run:

```python
prtl.calculate_all(star)
```

For targeted runs:

```python
prtl.calculate_scattering_properties()
prtl.calculate_temperatures(star)
prtl.calculate_beta_factors(star)
prtl.calculate_blowout_diameters(star)
```

`calculate_temperatures` and `calculate_all` require `dists` to be set.

## Mie resonance suppression

Set `suppress_mie_resonance=True` to average efficiency coefficients over nearby
particle sizes. This can reduce narrow Mie ripples in the optical coefficients.
The `size_averaging_window` parameter controls the size range used for this
averaging.

```python
prtl = opt.Particles(
    diams=diams,
    wavs=wavs,
    dists=dists,
    matrl=matrl,
    suppress_mie_resonance=True,
    size_averaging_window=2,
)
```
