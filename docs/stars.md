# Stars

`Star` provides the stellar spectrum used for heating and radiation pressure.
Luminosity and mass are supplied in solar units with `lum_suns` and
`mass_suns`.

## Blackbody star

```python
# Example
import astromiedust as amd

star = amd.Star(name="Fomalhaut", temp=8500, lum_suns=16.6, mass_suns=1.92)
```

`temp` is in Kelvin.

## Sun shortcut

```python
star = amd.Star(name="Sun")
```

If the name is `Sun` and no spectrum source is supplied, the class uses a
5770 K blackbody.

## Spectrum file

```python
# Example
from pathlib import Path
import astromiedust as amd

star = amd.Star(
    name="Fomalhaut",
    lum_suns=16.6,
    mass_suns=1.92,
    spectrum_file=Path("examples/Fomalhaut/fomalhaut_spectrum.txt"),
)
```

Spectrum files are read as two columns after two header rows:

- wavelength in `um`
- spectral flux density in `W / m^2 / um`

The effective temperature is derived from the integrated spectrum.

## Spectrum arrays

Arrays can be passed with `astropy` units:

```python
# Example
import numpy as np
import astropy.units as u
import astromiedust as amd

wavs = np.array([0.5, 1.0, 2.0]) * u.um
flux = np.array([1.0e7, 2.0e6, 3.0e5]) * u.W / u.m**2 / u.um

star = amd.Star(
    name="custom",
    lum_suns=1.0,
    mass_suns=1.0,
    spectrum_wavs=wavs,
    spectrum_flux=flux,
)
```

The flux can be per wavelength or per frequency, provided it is convertible by
`astropy`.
