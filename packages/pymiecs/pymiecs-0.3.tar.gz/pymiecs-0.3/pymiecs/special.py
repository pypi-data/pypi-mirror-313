# special functions for Mie
# %%
import numpy as np
from scipy import special


def riccati_j_n(n, x):
    # riccati-bessel of the first kind and its derivative
    jn = special.spherical_jn(n, x)
    jnp = special.spherical_jn(n, x, derivative=True)
    return np.array([x * jn, jn + x * jnp])


def riccati_y_n(n, x):
    # riccati-bessel of the second kind and its derivative
    yn = special.spherical_yn(n, x)
    ynp = special.spherical_yn(n, x, derivative=True)

    return np.array([-1 * x * yn, -1 * (yn + x * ynp)])


def riccati_h1_n(n, x):
    # riccati-bessel for hankel function and its derivative
    # For the identity, see https://en.wikipedia.org/wiki/Bessel_function
    return riccati_j_n(n, x) - 1j * riccati_y_n(n, x)
