# Physics Notes

These notes summarize how the package organizes the calculation. They are meant
as a guide to the code's model choices, not a replacement for the source or for
the literature behind a particular dust model.

The workflow has three broad steps:

1. Build an effective dielectric function for a composite material.
2. Compute absorption, scattering, radiation-pressure, and asymmetry
   coefficients for each particle diameter and wavelength.
3. Use those coefficients with a stellar spectrum to estimate temperatures,
   beta factors, and thermal emission.

See the topic pages for details on each step.
