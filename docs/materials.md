# Materials

`Material` builds the composite dust dielectric function used by the scattering
calculations. The built-in material data combine silicate, refractory
carbonaceous material, water ice, and vacuum.

```python
import astromiedust as opt

matrl = opt.Material(
    qsil=0.4,
    qice=1.0,
    mpor=0.7,
    cryst=False,
    emt="maxwell-garnett",
)
```

## Parameters

`qsil` is the silicate volume fraction within the silicate plus organic
core-mantle grain material.

`qice` is the water-ice volume fraction within the ice plus vacuum part of the
matrix.

`mpor` is the matrix porosity: the total ice plus vacuum fraction of the final
composite.

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

The material fractions are validated to be finite scalars between 0 and 1.
Pure-vacuum compositions are not supported because the resulting material
density is not positive.
