# Mie observables
# %%
import warnings

import numpy as np
from pymiecs.mie_coeff import core_shell_ab
from pymiecs.mie_coeff import pi_tau
from pymiecs.tools import get_truncution_criteroin_wiscombe


def Q(
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
    k0 = np.atleast_1d(k0)
    if len(np.shape(k0)) == 1:
        k0 = k0[None, :]

    n_env = np.atleast_1d(n_env)
    if len(np.shape(n_env)) == 1:
        n_env = n_env[None, :]
    k = k0 * n_env

    if r_shell is None:
        r_shell = r_core

    if n_max == "auto":
        # criterion for farfield series truncation
        n_max = get_truncution_criteroin_wiscombe(r_shell * k)

    n = np.arange(1, n_max + 1)[:, None]

    a, b = core_shell_ab(
        k0=k0,
        r_core=r_core,
        n_core=n_core,
        r_shell=r_shell,
        n_shell=n_shell,
        mu_core=mu_core,
        mu_shell=mu_shell,
        n_env=n_env,
        mu_env=mu_env,
        n_max=n_max,
    )

    # --- scattering efficiencies
    cs_geo = np.pi * r_shell**2  # geometric cross section
    prefactor = 2 / (k**2 * r_shell**2)

    # separate multipole contributions
    qext_e = prefactor * (2 * n + 1) * (a.real)
    qsca_e = prefactor * (2 * n + 1) * (a.real**2 + a.imag**2)
    qext_m = prefactor * (2 * n + 1) * (b.real)
    qsca_m = prefactor * (2 * n + 1) * (b.real**2 + b.imag**2)
    qabs_e = qext_e - qsca_e
    qabs_m = qext_m - qsca_m

    # total efficiencies
    qext = np.sum(qext_e, axis=0) + np.sum(qext_m, axis=0)
    qsca = np.sum(qsca_e, axis=0) + np.sum(qsca_m, axis=0)
    qabs = qext - qsca

    # fw / bw scattering
    qback = np.sum(
        (prefactor / 2)
        * (np.abs(np.sum((2 * n + 1) * ((-1) ** n) * (a - b), axis=0)) ** 2),
        axis=0,
    )
    qfwd = np.sum(
        (prefactor / 2) * (np.abs(np.sum((2 * n + 1) * (a + b), axis=0)) ** 2), axis=0
    )

    qratio = qback / qfwd

    return dict(
        qext=qext,
        qsca=qsca,
        qabs=qabs,
        qext_e=qext_e,
        qsca_e=qsca_e,
        qabs_e=qabs_e,
        qext_m=qext_m,
        qsca_m=qsca_m,
        qabs_m=qabs_m,
        qfwd=qfwd,
        qback=qback,
        qratio=qratio,
        cs_geo=cs_geo,
    )


def S1_S2(
    k0,
    u,
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

    if len(np.shape(k)) == 0:
        k = np.array([k])
    if len(np.shape(k)) == 1:
        k = k[None, :]

    if n_max == "auto":
        # Wiscombe criterion for farfield
        n_max = get_truncution_criteroin_wiscombe(r_shell * k)

    n = np.arange(1, n_max + 1)[:, None]

    a, b = core_shell_ab(
        k0=k0,
        r_core=r_core,
        n_core=n_core,
        r_shell=r_shell,
        n_shell=n_shell,
        mu_core=mu_core,
        mu_shell=mu_shell,
        n_env=n_env,
        mu_env=mu_env,
        n_max=n_max,
    )

    pi_n, tau_n = pi_tau(u, n_max)
    n2 = (2 * n + 1) / (n * (n + 1))
    pi_n = pi_n[:, None] * n2
    tau_n = tau_n[:, None] * n2
    S1 = np.sum(a * np.conjugate(pi_n), axis=0) + np.sum(
        b * np.conjugate(tau_n), axis=0
    )
    S2 = np.sum(a * np.conjugate(tau_n), axis=0) + np.sum(
        b * np.conjugate(pi_n), axis=0
    )

    return S1, S2


def angular(
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
    angular_range=[0, np.pi],
    angular_steps=180,
):
    """return angular resolved scattered intensity

    I_scat = 1 / (r^2 k^2) |S|^2

    where S is either S1 (perpendicular, s polarization), S2 (parallel, p polarization) or
    the incoherent average of both (unpolarized).

    Args:
        k0 (_type_): _description_
        r_core (_type_): _description_
        n_core (_type_): _description_
        r_shell (_type_, optional): _description_. Defaults to None.
        n_shell (int, optional): _description_. Defaults to 1.
        mu_core (int, optional): _description_. Defaults to 1.
        mu_shell (int, optional): _description_. Defaults to 1.
        n_env (int, optional): _description_. Defaults to 1.
        mu_env (int, optional): _description_. Defaults to 1.
        n_max (str, optional): _description_. Defaults to "auto".
        angular_range (list, optional): _description_. Defaults to [0, np.pi].
        angular_steps (int, optional): _description_. Defaults to 180.

    Returns:
        tuple: angles, I_s, I_p, I_unpol
    """
    k = k0 * n_env

    if n_env != 1.0:
        warnings.warn("tested only for n_env=1 !!")

    if r_shell is None:
        r_shell = r_core

    if len(np.shape(k)) == 0:
        k = np.array([k])
    if len(np.shape(k)) == 1:
        k = k[:, None]

    theta = np.linspace(*angular_range, angular_steps)
    SL = np.zeros((k.shape[0], angular_steps))
    SR = np.zeros((k.shape[0], angular_steps))
    SU = np.zeros((k.shape[0], angular_steps))

    # TODO !! This could be vectorized !!
    for j in range(angular_steps):
        u = np.cos(theta[j])
        S1, S2 = S1_S2(
            k0,
            u,
            r_core,
            n_core,
            r_shell,
            n_shell,
            mu_core,
            mu_shell,
            n_env,
            mu_env,
            n_max,
        )
        SL[:, j] = (np.conjugate(S1) * S1).real
        SR[:, j] = (np.conjugate(S2) * S2).real

        SU[:, j] = (SR[:, j] + SL[:, j]) / 2

    I_s = SL / (k**2 * r_shell**2)
    I_p = SR / (k**2 * r_shell**2)
    I_unpol = SU / (k**2 * r_shell**2)

    return theta, I_s, I_p, I_unpol


def Q_scat_differential(
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
    angular_range=[0, np.pi],
    angular_steps=180,
):
    k = k0 * n_env

    if r_shell is None:
        r_shell = r_core

    theta, SL, SR, SU = angular(
        k0,
        r_core,
        n_core,
        r_shell,
        n_shell,
        mu_core=mu_core,
        mu_shell=mu_shell,
        n_env=n_env,
        mu_env=mu_env,
        n_max=n_max,
        angular_range=angular_range,
        angular_steps=angular_steps,
    )

    return dict(qsca=4 * SU.mean(axis=1))
