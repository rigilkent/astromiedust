# Particles

`Particles` holds the particle grids and calculated optical and thermal
properties.

```python
# Example
import numpy as np
import astromiedust as amd

wavs = np.logspace(-1, 4, 300)
diams = np.logspace(-1, 3, 60)
dists = np.logspace(0, 3, 40)

prtl = amd.Particles(
    diams=diams,  # particle diameters, um
    wavs=wavs,    # wavelengths, um
    dists=dists,  # distances from the star, au
    matrl=matrl,  # Material instance
)
```

`diams` may also be an `astropy` quantity convertible to `um`. Other grids are
plain arrays in the units shown above.

For the standard calculation order and result arrays, see
[Getting Started](getting_started.md).

## Mie resonance suppression

Set `suppress_mie_resonance=True` to average efficiency coefficients over nearby
particle sizes. This smooths out Mie ripples in the optical coefficients.
The `size_averaging_window` parameter controls the size range used for this
averaging (default: `2`, i.e. average over diameters from `diam / 2` to
`diam * 2`).

This option increases computation time because coefficients are evaluated on a
finer diameter grid before averaging.

```python
# Example
prtl = amd.Particles(
    diams=diams,
    wavs=wavs,
    dists=dists,
    matrl=matrl,
    suppress_mie_resonance=True,
    size_averaging_window=2,
)
```
