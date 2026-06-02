# Particles

`Particles` holds the particle grids and calculated optical and thermal
properties.

```python
import astromiedust as amd

prtl = amd.Particles(
    diams=diams,  # particle diameters, um
    wavs=wavs,    # wavelengths, um
    dists=dists,  # distances from the star, au
    matrl=matrl,  # Material instance
)
```

`diams` may also be an `astropy` quantity convertible to `um`. Other grids are
normally plain arrays in the units shown above.

For the standard calculation order and result arrays, see
[Getting Started](getting_started.md).

## Mie resonance suppression

Set `suppress_mie_resonance=True` to average efficiency coefficients over nearby
particle sizes. This can reduce narrow Mie ripples in the optical coefficients.
The `size_averaging_window` parameter controls the size range used for this
averaging.

```python
prtl = amd.Particles(
    diams=diams,
    wavs=wavs,
    dists=dists,
    matrl=matrl,
    suppress_mie_resonance=True,
    size_averaging_window=2,
)
```
