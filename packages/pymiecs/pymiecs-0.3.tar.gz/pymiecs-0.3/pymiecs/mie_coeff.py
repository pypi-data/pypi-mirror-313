# core-shell Mie coefficients for magnetizable media
# %%
import warnings

import numpy as np
from pymiecs import special
from pymiecs.tools import get_truncution_criteroin_wiscombe


def core_shell_ab(
    k0,
    r_core,
    n_core,
    r_shell=None,
    n_shell=1,
    mu_core=1,
    mu_shell=1,
    n_env=1,
    mu_env=1,
    n_max="auto",
):

    if r_shell is None:
        r_shell = r_core

    #  vectorize: adapt shapes for correct broadcasting
    k0 = np.atleast_1d(k0)
    if len(np.shape(k0)) == 1:
        k0 = k0[None, :]

    n_env = np.atleast_1d(n_env)
    if len(np.shape(n_env)) == 1:
        n_env = n_env[None, :]
    k = k0 * n_env
    
    n_core = np.atleast_1d(n_core)
    if len(np.shape(n_core)) == 1:
        n_core = n_core[None, :]

    n_shell = np.atleast_1d(n_shell)
    if len(np.shape(n_shell)) == 1:
        n_shell = n_shell[None, :]

    mu_core = np.atleast_1d(mu_core)
    if len(np.shape(mu_core)) == 1:
        mu_core = mu_core[None, :]

    mu_shell = np.atleast_1d(mu_shell)
    if len(np.shape(mu_shell)) == 1:
        mu_shell = mu_shell[None, :]

    # truncation criterion
    if n_max == "auto":
        warnings.warn("Automatically choosing max order (Wiscombe criterion).")
        n_max = get_truncution_criteroin_wiscombe(r_shell * k)

    assert type(n_max) == int
    n = np.arange(1, n_max + 1)[:, None]

    # - pre-evaluation
    n_rel_c = n_core / n_env
    n_rel_s = n_shell / n_env
    x = k * r_core
    y = k * r_shell

    rj1x = special.riccati_j_n(n, n_rel_c * x)
    rj2x = special.riccati_j_n(n, n_rel_s * x)
    rjy = special.riccati_j_n(n, y)
    rj2y = special.riccati_j_n(n, n_rel_s * y)

    ry2x = special.riccati_y_n(n, n_rel_s * x)
    ry2y = special.riccati_y_n(n, n_rel_s * y)

    rh1y = special.riccati_h1_n(n, y)

    # - subsitution
    m1 = n_rel_c
    m2 = n_rel_s
    mu1 = mu_core
    mu2 = mu_shell
    psin1x = rj1x[0]
    psibn1x = rj1x[1]
    psin2x = rj2x[0]
    psibn2x = rj2x[1]
    psiny = rjy[0]
    psibny = rjy[1]
    psin2y = rj2y[0]
    psibn2y = rj2y[1]
    chin2x = ry2x[0]
    chibn2x = ry2x[1]
    chin2y = ry2y[0]
    chibn2y = ry2y[1]
    xiny = rh1y[0]
    xibny = rh1y[1]

    # - eval. sympy-solved formulas
    an = (
        chibn2x * m1 * m2 * mu_env * mu2 * psibny * psin1x * psin2y
        - chibn2x * m1 * mu2**2 * psibn2y * psin1x * psiny
        + chibn2y * m1 * mu2**2 * psibn2x * psin1x * psiny
        - chibn2y * m2 * mu1 * mu2 * psibn1x * psin2x * psiny
        - chin2x * m2**2 * mu_env * mu1 * psibn1x * psibny * psin2y
        + chin2x * m2 * mu1 * mu2 * psibn1x * psibn2y * psiny
        - chin2y * m1 * m2 * mu_env * mu2 * psibn2x * psibny * psin1x
        + chin2y * m2**2 * mu_env * mu1 * psibn1x * psibny * psin2x
    ) / (
        chibn2x * m1 * m2 * mu_env * mu2 * psin1x * psin2y * xibny
        - chibn2x * m1 * mu2**2 * psibn2y * psin1x * xiny
        + chibn2y * m1 * mu2**2 * psibn2x * psin1x * xiny
        - chibn2y * m2 * mu1 * mu2 * psibn1x * psin2x * xiny
        - chin2x * m2**2 * mu_env * mu1 * psibn1x * psin2y * xibny
        + chin2x * m2 * mu1 * mu2 * psibn1x * psibn2y * xiny
        - chin2y * m1 * m2 * mu_env * mu2 * psibn2x * psin1x * xibny
        + chin2y * m2**2 * mu_env * mu1 * psibn1x * psin2x * xibny
    )

    bn = (
        chibn2x * m2**2 * mu_env * mu1 * psibn2y * psin1x * psiny
        - chibn2x * m2 * mu1 * mu2 * psibny * psin1x * psin2y
        + chibn2y * m1 * m2 * mu_env * mu2 * psibn1x * psin2x * psiny
        - chibn2y * m2**2 * mu_env * mu1 * psibn2x * psin1x * psiny
        - chin2x * m1 * m2 * mu_env * mu2 * psibn1x * psibn2y * psiny
        + chin2x * m1 * mu2**2 * psibn1x * psibny * psin2y
        - chin2y * m1 * mu2**2 * psibn1x * psibny * psin2x
        + chin2y * m2 * mu1 * mu2 * psibn2x * psibny * psin1x
    ) / (
        chibn2x * m2**2 * mu_env * mu1 * psibn2y * psin1x * xiny
        - chibn2x * m2 * mu1 * mu2 * psin1x * psin2y * xibny
        + chibn2y * m1 * m2 * mu_env * mu2 * psibn1x * psin2x * xiny
        - chibn2y * m2**2 * mu_env * mu1 * psibn2x * psin1x * xiny
        - chin2x * m1 * m2 * mu_env * mu2 * psibn1x * psibn2y * xiny
        + chin2x * m1 * mu2**2 * psibn1x * psin2y * xibny
        - chin2y * m1 * mu2**2 * psibn1x * psin2x * xibny
        + chin2y * m2 * mu1 * mu2 * psibn2x * psin1x * xibny
    )
    return an, bn


def core_shell_cd(
    k0,
    r_core,
    n_core,
    r_shell=None,
    n_shell=1,
    mu_core=1,
    mu_shell=1,
    n_env=1,
    mu_env=1,
    n_max="auto",
):
    k = k0 * n_env

    if r_shell is None:
        r_shell = r_core

    #  vectorize: adapt shapes for correct broadcasting
    if len(np.shape(k)) == 0:
        k = np.array([k])
    if len(np.shape(k)) == 1:
        k = k[None, :]

    if len(np.shape(n_core)) == 0:
        n_core = np.array([n_core])
    if len(np.shape(n_core)) == 1:
        n_core = n_core[None, :]

    if len(np.shape(n_shell)) == 0:
        n_shell = np.array([n_shell])
    if len(np.shape(n_shell)) == 1:
        n_shell = n_shell[None, :]

    if len(np.shape(mu_core)) == 0:
        mu_core = np.array([mu_core])
    if len(np.shape(mu_core)) == 1:
        mu_core = mu_core[None, :]

    if len(np.shape(mu_shell)) == 0:
        mu_shell = np.array([mu_shell])
    if len(np.shape(mu_shell)) == 1:
        mu_shell = mu_shell[None, :]

    # truncation criterion
    if n_max == "auto":
        warnings.warn("Automatically choosing max order (Wiscombe criterion).")
        n_max = get_truncution_criteroin_wiscombe(r_shell * k)
        
    assert type(n_max) == int
    n = np.arange(1, n_max + 1)[:, None]

    # - pre-evaluation
    n_rel_c = n_core / n_env
    n_rel_s = n_shell / n_env
    x = k * r_core
    y = k * r_shell

    rj1x = special.riccati_j_n(n, n_rel_c * x)
    rj2x = special.riccati_j_n(n, n_rel_s * x)
    rjy = special.riccati_j_n(n, y)
    rj2y = special.riccati_j_n(n, n_rel_s * y)

    ry2x = special.riccati_y_n(n, n_rel_s * x)
    ry2y = special.riccati_y_n(n, n_rel_s * y)

    rh1y = special.riccati_h1_n(n, y)

    # - subsitution
    m1 = n_rel_c
    m2 = n_rel_s
    mu1 = mu_core
    mu2 = mu_shell
    psin1x = rj1x[0]
    psibn1x = rj1x[1]
    psin2x = rj2x[0]
    psibn2x = rj2x[1]
    psiny = rjy[0]
    psibny = rjy[1]
    psin2y = rj2y[0]
    psibn2y = rj2y[1]
    chin2x = ry2x[0]
    chibn2x = ry2x[1]
    chin2y = ry2y[0]
    chibn2y = ry2y[1]
    xiny = rh1y[0]
    xibny = rh1y[1]

    # - eval. sympy-solved formulas
    cn = (
        chibn2x * m1 * m2 * mu1 * mu2 * psibny * psin2x * xiny
        - chibn2x * m1 * m2 * mu1 * mu2 * psin2x * psiny * xibny
        - chin2x * m1 * m2 * mu1 * mu2 * psibn2x * psibny * xiny
        + chin2x * m1 * m2 * mu1 * mu2 * psibn2x * psiny * xibny
    ) / (
        chibn2x * m2**2 * mu_env * mu1 * psibn2y * psin1x * xiny
        - chibn2x * m2 * mu1 * mu2 * psin1x * psin2y * xibny
        + chibn2y * m1 * m2 * mu_env * mu2 * psibn1x * psin2x * xiny
        - chibn2y * m2**2 * mu_env * mu1 * psibn2x * psin1x * xiny
        - chin2x * m1 * m2 * mu_env * mu2 * psibn1x * psibn2y * xiny
        + chin2x * m1 * mu2**2 * psibn1x * psin2y * xibny
        - chin2y * m1 * mu2**2 * psibn1x * psin2x * xibny
        + chin2y * m2 * mu1 * mu2 * psibn2x * psin1x * xibny
    )
    dn = (
        -chibn2x * m1 * m2 * mu1 * mu2 * psibny * psin2x * xiny
        + chibn2x * m1 * m2 * mu1 * mu2 * psin2x * psiny * xibny
        + chin2x * m1 * m2 * mu1 * mu2 * psibn2x * psibny * xiny
        - chin2x * m1 * m2 * mu1 * mu2 * psibn2x * psiny * xibny
    ) / (
        chibn2x * m1 * m2 * mu_env * mu2 * psin1x * psin2y * xibny
        - chibn2x * m1 * mu2**2 * psibn2y * psin1x * xiny
        + chibn2y * m1 * mu2**2 * psibn2x * psin1x * xiny
        - chibn2y * m2 * mu1 * mu2 * psibn1x * psin2x * xiny
        - chin2x * m2**2 * mu_env * mu1 * psibn1x * psin2y * xibny
        + chin2x * m2 * mu1 * mu2 * psibn1x * psibn2y * xiny
        - chin2y * m1 * m2 * mu_env * mu2 * psibn2x * psin1x * xibny
        + chin2y * m2**2 * mu_env * mu1 * psibn1x * psin2x * xibny
    )

    return cn, dn


def pi_tau(mu, n_max):
    # angular functions
    # see Bohren Huffmann, chapter 4.3.1
    # mu = cos(teta)
    p = np.zeros(int(n_max))
    t = np.zeros(int(n_max))
    p[0] = 1.0
    t[0] = mu
    p[1] = 3.0 * mu
    t[1] = 3.0 * np.cos(2 * np.arccos(mu))
    for n in range(2, int(n_max)):
        p[n] = ((2 * n + 1) * (mu * p[n - 1]) - (n + 1) * p[n - 2]) / n
        t[n] = (n + 1) * mu * p[n] - (n + 2) * p[n - 1]
    return p, t

