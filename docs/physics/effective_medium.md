# Effective Medium Theory

`Material` combines built-in optical constants for silicate, refractory
carbonaceous material, water ice, and vacuum.

Two effective medium options are implemented:

- Maxwell-Garnett: selected by `emt="maxwell-garnett"` or `emt="mg"`
- Bruggeman: selected by `emt="bruggeman"` or `emt="br"`

```python
import astromiedust as amd

mg = amd.Material(qsil=0.4, qice=1.0, mpor=0.7, emt="mg")
br = amd.Material(qsil=0.4, qice=1.0, mpor=0.7, emt="br")
```

For Maxwell-Garnett, the code follows the ordered mixing picture of
[Li & Greenberg (1997)](https://ui.adsabs.harvard.edu/abs/1997A%26A...323..566L/abstract):
it first forms a silicate-organic core-mantle grain material, then mixes grains
with ice when ice is present, then mixes the resulting solid component into
vacuum.

For Bruggeman, the code solves for an effective dielectric constant using the
absolute volume fractions of organic material, silicate, ice, and vacuum.

The final material stores a complex dielectric function `eps`, a wavelength grid
`wavs` in `um`, and an effective density in `g / cm^3`.
