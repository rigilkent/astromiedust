# Materials

`Material` builds the composite dust dielectric function used by the scattering
calculations.

```python
# Example
import astromiedust as amd

matrl = amd.Material(
    qsil=0.4,
    qice=1.0,
    mpor=0.7,
    cryst=False,
    emt="maxwell-garnett",
)
```

## Composition Parameters

The material composition is parametrized by three volume fractions:

`qsil` is the volume fraction of silicate in the combined volume of silicate
and organic refractory material:
`qsil = V_silicate / (V_silicate + V_organic)`.

`mpor` is the matrix porosity: the fraction of the total composite volume that
is void space within the silicate-organic matrix. These voids can be empty or
partially filled with water ice.

`qice` is the fraction of that void volume filled with water ice:
`qice = V_ice / (V_ice + V_vacuum)`. If `qice=0`, the void volume is vacuum;
if `qice=1`, it is fully filled with ice.

These three knobs imply the absolute volume fractions:

- silicate: `qsil * (1 - mpor)`
- organic material: `(1 - qsil) * (1 - mpor)`
- water ice: `qice * mpor`
- vacuum: `(1 - qice) * mpor`

Each fraction parameter must be between 0 and 1. Pure-vacuum compositions
(`mpor=1`, `qice=0`) will raise an error.

## Other Parameters

`cryst` selects crystalline silicate when `True`; the default is amorphous
silicate.

`emt` selects the effective medium rule. Accepted values are
`"maxwell-garnett"` / `"mg"` or `"bruggeman"` / `"br"`.

`refmed` is the refractive index of the surrounding medium relative to vacuum.
It defaults to `1.0`.

## Computed attributes

After initialization, useful attributes include:

- `matrl.wavs`: material wavelength grid in `um`
- `matrl.eps`: complex effective dielectric function
- `matrl.density`: bulk density in `g / cm^3`
- `matrl.info`: short composition string
