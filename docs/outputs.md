# Outputs and I/O

Use `OpticalModel` when you want to save a completed calculation.

```python
# Example
import astromiedust as amd

model = amd.OpticalModel(star=star, prtl=prtl)
model.save("model.pkl")
```

## Pickle round trip

```python
# Example
loaded = amd.OpticalModel.load("model.pkl")

star = loaded.star
prtl = loaded.prtl
matrl = loaded.prtl.matrl
```

`OpticalModel.save` writes the complete Python object with pickle. This is the
most direct way to continue a calculation later in Python.

## HDF5 export

```python
# Example
model.save_hdf5("model.h5")
```

`save_hdf5` exports common star, particle, and material arrays and metadata to
HDF5 for interoperability.

## Beta CSV

```python
# Example
model.save_beta_csv("beta.csv")
model.save_beta_csv("beta_with_qpr.csv", include_Qpr_star_avg=True)
```

The default CSV has:

- `diameter_um`
- `beta`

With `include_Qpr_star_avg=True`, it also includes the
stellar-spectrum-averaged radiation-pressure efficiency.

## Qabs times Bnu HDF5

```python
# Example
model.save_qabs_bnu_hdf5("qabs_bnu.h5")
```

`save_qabs_bnu_hdf5` writes `Qabs * Bnu` as a 3D array with dimensions
`(dists, diams, wavs)`. Axis datasets are stored with units:

- `dists`: `au`
- `diams`: `um`
- `wavs`: `um`

The `Qabs_Bnu` dataset has units `Jy/sr`, matching the default frequency-domain
output of the blackbody radiance helper.
