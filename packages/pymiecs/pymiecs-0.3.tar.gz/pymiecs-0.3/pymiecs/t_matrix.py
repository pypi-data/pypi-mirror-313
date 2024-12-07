# core-shell Mie coefficients for magnetizable media
# %%
import warnings

import numpy as np
from pymiecs import mie_coeff

try:
    from smuthi.particles import Particle
    import smuthi.fields as flds
    import smuthi.utility.memoizing as memo
    tmatrix_available = True
except ImportError:
    warnings.warn(
        "Failed to import `smuthi`. T-matrix calculation is therefore not available."
    )
    tmatrix_available = False



if tmatrix_available:
    def t_matrix_coreshellsphere(
        k0,
        r_core,
        n_core,
        r_shell=None,
        n_shell=1,
        n_env=1,
        l_max=None,
        m_max=None,
    ):
        """T-matrix of a spherical scattering object.

        Args:
            l_max (int):                            Maximal multipole degree
            m_max (int):                            Maximal multipole order (constant for Mie)

        Returns:
            T-matrix as ndarray
        """
        an, bn = mie_coeff.core_shell_ab(
            k0=k0,
            r_core=r_core,
            n_core=n_core,
            r_shell=r_shell,
            n_shell=n_shell,
            mu_core=1,
            mu_shell=1,
            n_env=n_env,
            mu_env=1,
            n_max=l_max + 1,
        )
        t = np.zeros(
            (flds.blocksize(l_max, m_max), flds.blocksize(l_max, m_max)), dtype=complex
        )
        for m in range(-m_max, m_max + 1):
            for l in range(max(1, abs(m)), l_max + 1):
                # tau=0: electric coefficients
                # mie_coefficient(tau, l, k_medium, k_particle, radius)
                tau = 0
                n = flds.multi_to_single_index(tau, l, m, l_max, m_max)
                t[n, n] = an[l - 1, 0]

                # tau=1: magnetic coefficients
                tau = 1
                n = flds.multi_to_single_index(tau, l, m, l_max, m_max)
                t[n, n] = bn[l - 1, 0]

        return t


    class SphereCoreShell(Particle):
        """Particle subclass for core-shell spheres.

        Args:
            position (list):            Particle position in the format [x, y, z] (length unit)
            refractive_index (complex): Complex refractive index of particle
            radius (float):             Particle radius (length unit)
            l_max (int):                Maximal multipole degree used for the spherical wave expansion of incoming and
                                        scattered field
            m_max (int):                Maximal multipole order used for the spherical wave expansion of incoming and
                                        scattered field
        """

        def __init__(
            self,
            position=None,
            r_core=1,
            n_core=1,
            r_shell=None,
            n_shell=1,
            l_max=None,
            m_max=None,
        ):
            Particle.__init__(
                self,
                position=position,
                refractive_index=n_core,
                l_max=l_max,
                m_max=m_max,
            )
            if r_shell is None:
                r_shell = r_core

            self.r_core = r_core
            self.r_shell = r_shell
            self.n_core = n_core
            self.n_shell = n_shell

        def circumscribing_sphere_radius(self):
            return self.r_shell

        def is_inside(self, x, y, z):
            return (x - self.position[0]) ** 2 + (y - self.position[1]) ** 2 + (
                z - self.position[2]
            ) ** 2 <= self.r_shell**2

        def is_outside(self, x, y, z):
            return (x - self.position[0]) ** 2 + (y - self.position[1]) ** 2 + (
                z - self.position[2]
            ) ** 2 > self.r_shell**2

        def compute_t_matrix(self, vacuum_wavelength, n_medium):
            # By memoizing the call to compute_t_matrix through a wrapper,
            # you can efficiently reuse t-matricies when particles are the same type.
            # This method is done automatically, so no other changes in the linear system
            # are necessary to efficiently use memory and save computation time.

            return _compute_coreshellsphere_t_matrix(
                r_core=self.r_core,
                n_core=self.n_core,
                r_shell=self.r_shell,
                n_shell=self.n_shell,
                sphere_l_max=self.l_max,
                sphere_m_max=self.m_max,
                vacuum_wavelength=vacuum_wavelength,
                medium_refractive_index=n_medium,
            )


    @memo.Memoize
    def _compute_coreshellsphere_t_matrix(
        r_core,
        n_core,
        r_shell,
        n_shell,
        sphere_l_max,
        sphere_m_max,
        vacuum_wavelength,
        medium_refractive_index,
    ):
        k0 = 2 * np.pi / vacuum_wavelength
        t = t_matrix_coreshellsphere(
            k0=k0,
            r_core=r_core,
            n_core=n_core,
            r_shell=r_shell,
            n_shell=n_shell,
            n_env=medium_refractive_index,
            l_max=sphere_l_max,
            m_max=sphere_m_max,
        )

        return t
