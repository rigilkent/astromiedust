# Temperatures and Beta

Equilibrium temperatures require a stellar spectrum, particle absorption
efficiencies, and distances from the star.

```python
prtl.calculate_temperatures(star)
print(prtl.temps)  # K, shape (n_dists, n_diams)
```

Distances are in `au`; particle diameters are in `um`.

## Beta factors

Beta is the ratio of radiation pressure force to gravitational force. The code
computes a stellar-spectrum-averaged radiation-pressure efficiency and then uses
the star mass and luminosity to estimate beta as a function of particle size.

```python
prtl.calculate_beta_factors(star)

print(prtl.Qpr_star_avg)
print(prtl.betas)
```

`calculate_blowout_diameters(star)` estimates the diameter range where beta
exceeds a selected blowout threshold. The default threshold is `beta_blow=0.5`.

```python
lower_um, upper_um = prtl.calculate_blowout_diameters(star)
```

The return value is always an interval. If beta exceeds the threshold down to
the smallest sizes considered by the search, the lower value is `0`. If no
particles exceed the threshold, the result is `(None, None)`.

For a complete standard run, `calculate_all(star)` performs these calculations
and also fills `bnus`, the blackbody spectral radiance on the requested
wavelength, distance, and diameter grids.
