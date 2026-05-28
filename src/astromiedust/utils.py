import numpy as np
from astropy import units as u
from scipy.optimize import brentq
from .optics_core import calculate_spectral_radiance_bb


def calculate_color_temperature(I1, I2, lambda1, lambda2, Tmin=10*u.K, Tmax=2000*u.K):
    """
    Compute the color temperature from two surface-brightness measurements
    at different wavelengths.

    Parameters
    ----------
    I1, I2 : array-like
        Surface brightness values at lambda1 and lambda2 (units irrelevant).
    lambda1, lambda2 : astropy.Quantity
        Wavelengths (must be convertible to µm).
    Tmin, Tmax : astropy.Quantity
        Temperature bracketing interval.

    Returns
    -------
    astropy.Quantity
        Color temperature(s) with units of Kelvin.
    """

    # Convert wavelengths to floats in µm for the fast core
    lam1_um = lambda1.to(u.um).value
    lam2_um = lambda2.to(u.um).value

    # Convert temperature brackets to floats
    Tmin_f = Tmin.to(u.K).value
    Tmax_f = Tmax.to(u.K).value

    I1 = np.asarray(I1, float)
    I2 = np.asarray(I2, float)
    valid = (I1 > 0) & (I2 > 0) & np.isfinite(I1) & np.isfinite(I2)
    ratio = np.full_like(I1, np.nan, dtype=float)  # default = NaN
    ratio[valid] = I1[valid] / I2[valid]

    # Result array
    T_out = np.full_like(ratio, np.nan, dtype=float)

    # Flatten for iteration (root finding must be scalar)
    rflat = ratio.ravel()
    Tflat = T_out.ravel()
    vflat = valid.ravel()

    for idx, R in enumerate(rflat):
        if not np.isfinite(R) or not vflat[idx]:
            continue

        def f(T):
            # B_lambda at λ1 and λ2 from fast core (unitless floats)
            B1 = calculate_spectral_radiance_bb(lam1_um, T)
            B2 = calculate_spectral_radiance_bb(lam2_um, T)
            return B1 / B2 - R

        try:
            Tflat[idx] = brentq(f, Tmin_f, Tmax_f)

        except ValueError:
            pass # Root not bracketed; leave as T as NaN

    # Return Quantity in Kelvin
    return T_out * u.K
