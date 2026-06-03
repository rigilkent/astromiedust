# Fomalhaut Example

The repository includes a complete Fomalhaut script at
`examples/Fomalhaut/fomalhaut_demo.py`.

It uses a custom stellar spectrum file, a porous composite material, logarithmic
wavelength, size, and distance grids, and the full `calculate_all` workflow.

```python
# Example
from pathlib import Path
import numpy as np
import astromiedust as amd

example_dir = Path("examples/Fomalhaut")

star = amd.Star(
    name="Fomalhaut",
    lum_suns=16.6,
    mass_suns=1.92,
    spectrum_file=example_dir / "fomalhaut_spectrum.txt",
)

matrl = amd.Material(qsil=0.4, qice=1.0, mpor=0.7, emt="maxwell-garnett")

wavs = np.logspace(0, 4, 300)
diams = np.logspace(0, 4, 41)
dists = np.logspace(0, 3, 43)

prtl = amd.Particles(
    diams=diams,
    wavs=wavs,
    dists=dists,
    matrl=matrl,
    suppress_mie_resonance=True,
)
prtl.calculate_all(star)

result = amd.SystemResult(star=star, prtl=prtl)
result.save(example_dir / "fomalhaut_results.pkl")
```

The same script also shows the plotting helpers for the stellar spectrum,
optical coefficients, beta factors, temperatures, and asymmetry factor.
