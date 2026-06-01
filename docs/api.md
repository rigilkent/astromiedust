# API Reference

The preferred public API is imported from `astromiedust`.

::: astromiedust.Star
    options:
      members:
        - __init__
        - get_spectral_flux_density
        - plot_spectrum

::: astromiedust.Material
    options:
      members:
        - __init__
        - calculate_composite_material_props
        - interpolate_eps

::: astromiedust.Particles
    options:
      members:
        - __init__
        - calculate_all
        - calculate_scattering_properties
        - calculate_temperatures
        - calculate_Qpr_star_avg
        - calculate_beta_factors
        - calculate_blowout_diameters
        - calculate_spectral_radiance_bb
        - interpolate_temperatures
        - plot_Q
        - plot_g
        - plot_beta
        - plot_Qpr_star_avg
        - plot_temp

::: astromiedust.OpticalModel
    options:
      members:
        - __init__
        - save
        - load
        - save_hdf5
        - save_beta_csv
        - save_qabs_bnu_hdf5

::: astromiedust.utils
    options:
      members:
        - calculate_color_temperature
