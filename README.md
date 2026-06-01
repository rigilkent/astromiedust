# astromiedust
A tool to compute the optical properties of circumstellar dust particles 
as well as their resulting equilibrium temperatures and thermal emission.

> [!NOTE]
> This project was formerly named `astrodust_optprops`. The old import path
> remains available as a compatibility layer, but new code should use
> `import astromiedust`.


`astromiedust` first finds the optical constants of a composite material made up of 
silicate, refractory carbonaceous material, water ice, and vacuum
using effective medium theory.
It applies Mie theory, Rayleigh-Gans theory, or geometric optics
in the respective wavelength regimes to determine the particles' 
optical coefficients.
These can then be used to compute the distance- and size-dependent equilibrium temperatures
of particles around a given star, as well as their β-factors (the ratio of radiation pressure force to gravity), or their blowout sizes.

Optical constants of the composite may be computed using the Maxwell-Garnett rule,
treating dust as aggregates of core-mantle grains, following
[Li & Greenberg (1997)](https://ui.adsabs.harvard.edu/abs/1997A%26A...323..566L/abstract),
or using the Bruggeman rule.
`astromiedust` can also suppress Mie resonance ripples in the optical coefficients by averaging over nearby particle sizes.

## Usage

See the `examples` directory for more detailed usage examples.

The package provides several key classes for modeling the optical properties:

```python
import astromiedust as amd

# Create a star object
star = amd.Star(name='Fomalhaut', lum_suns=16.6, mass_suns=1.92, temp=8500)

# Create a material object
matrl = amd.Material(...)

# Define wavelengths, particles diameters, and their distances to the star
wavs = [...]
diams = [...]
dists = [...]

# Create a Particles instance and calculate all properties
prtl = amd.Particles(diams=diams, wavs=wavs, matrl=matrl, dists=dists)
prtl.calculate_all(star)

print('Particle Qabs:\n', prtl.Qabs)
print('Particle temperatures:\n', prtl.temps)
```

## Installation

```bash
git clone https://github.com/rigilkent/astromiedust.git
cd astromiedust
pip install .
```

## Documentation

To build the documentation locally:

```bash
python -m pip install -e ".[docs]"
mkdocs serve
mkdocs build --strict
```

Publishing the docs requires GitHub Pages to be enabled for the repository with
the source set to GitHub Actions. The docs workflow builds on pushes and pull
requests, but deploys only when manually run from GitHub Actions.
