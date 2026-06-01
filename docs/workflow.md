# Core Workflow

Most scripts follow the same pattern:

1. Build a `Star`.
2. Build a `Material`.
3. Choose wavelength, particle-diameter, and distance grids.
4. Build `Particles`.
5. Run `Particles.calculate_all(star)`.
6. Save or plot the outputs.

```python
import numpy as np
import astromiedust as amd

star = amd.Star(name="A star", temp=8000, lum_suns=10.0, mass_suns=1.8)
matrl = amd.Material(qsil=0.4, qice=1.0, mpor=0.7)

prtl = amd.Particles(
    wavs=np.logspace(0, 4, 300),
    diams=np.logspace(0, 4, 41),
    dists=np.logspace(0, 3, 43),
    matrl=matrl,
)

prtl.calculate_all(star)
```

## What `calculate_all` fills

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
| `diams_blow` | beta = 0.5 blowout diameter range, in um | tuple |
| `bnus` | blackbody spectral radiance, default `Jy/sr` | `(n_dists, n_diams, n_wavs)` |

You can also run pieces of the workflow directly, such as
`calculate_scattering_properties`, `calculate_temperatures`,
`calculate_beta_factors`, and `calculate_blowout_diameters`.

## Plotting

The main classes include Matplotlib helpers:

```python
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
