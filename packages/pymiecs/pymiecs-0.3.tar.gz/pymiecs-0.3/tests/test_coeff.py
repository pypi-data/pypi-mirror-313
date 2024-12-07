# encoding=utf-8
# %%
import unittest

import numpy as np

from pymiecs.mie_coeff import core_shell_ab


class TestHomogeneous(unittest.TestCase):

    def setUp(self):
        self.verbose = True

        self.n_max = 5

        self.wavelengths = np.linspace(400, 900, 20)  # wavelength in nm
        self.n_env = 1

        self.r_core = 150.0
        self.n_core = 3.5

    def test_mie_coeff(self):
        # --- evaluate mie coefficients

        # pymiecs
        k0 = 2 * np.pi / self.wavelengths
        k = k0 * self.n_env

        a_n, b_n = core_shell_ab(
            k0=k0,
            r_core=self.r_core,
            n_core=self.n_core,
            n_env=self.n_env,
            n_max=self.n_max,
        )

        # reference: pymiescatt
        try:
            from PyMieScatt import Mie_ab
        except (ModuleNotFoundError, ImportError):
            print("`PyMieScatt` seems not to be installed. Skipping test.")
            return

        a_n_ref = []
        b_n_ref = []
        for wavelength in self.wavelengths:
            m = self.n_core / self.n_env
            x = 2 * np.pi * self.r_core * self.n_env / wavelength

            _an, _bn = Mie_ab(m=m, x=x)

            a_n_ref.append(_an[: self.n_max])
            b_n_ref.append(_bn[: self.n_max])

        a_n_ref = np.array(a_n_ref).T
        b_n_ref = np.array(b_n_ref).T

        np.testing.assert_allclose(a_n, a_n_ref)
        np.testing.assert_allclose(b_n, b_n_ref)


class TestCoreShell(unittest.TestCase):

    def setUp(self):
        self.verbose = True

        self.n_max = 5
        self.wavelengths = np.linspace(400, 900, 20)  # wavelength in nm

        self.test_cases = [
            dict(
                n_env=1,
                r_core=80.0,
                n_core=3,
                r_shell=120.0,
                n_shell=4,
            ),
            dict(
                n_env=1.5,
                r_core=90.0,
                n_core=2.5,
                r_shell=110.0,
                n_shell=0.05 + 3.5j,  # plasmonic material
            ),
            dict(
                n_env=1.25,
                r_core=70.0,
                n_core=0.05 + 3.5j,  # plasmonic material
                r_shell=110.0,
                n_shell=4.5 + 1j,  # lossy dielectric
            ),
        ]

    def test_mie_coeff(self):
        # --- evaluate mie coefficients
        for conf in self.test_cases:

            # pymiecs
            k0 = 2 * np.pi / self.wavelengths
            k = k0 * conf["n_env"]

            a_n, b_n = core_shell_ab(
                k0=k0,
                r_core=conf["r_core"],
                n_core=conf["n_core"],
                r_shell=conf["r_shell"],
                n_shell=conf["n_shell"],
                n_env=conf["n_env"],
                n_max=self.n_max,
            )

            # reference: pymiescatt
            try:
                from PyMieScatt.CoreShell import CoreShell_ab
            except (ModuleNotFoundError, ImportError):
                print("`PyMieScatt` seems not to be installed. Skipping test.")
                return

            a_n_ref = []
            b_n_ref = []
            for wavelength in self.wavelengths:
                mCore = conf["n_core"] / conf["n_env"]
                mShell = conf["n_shell"] / conf["n_env"]
                xCore = 2 * np.pi * conf["r_core"] * conf["n_env"] / wavelength
                xShell = 2 * np.pi * conf["r_shell"] * conf["n_env"] / wavelength

                _an, _bn = CoreShell_ab(
                    mCore=mCore, mShell=mShell, xCore=xCore, xShell=xShell
                )

                a_n_ref.append(_an[: self.n_max])
                b_n_ref.append(_bn[: self.n_max])

            a_n_ref = np.array(a_n_ref).T
            b_n_ref = np.array(b_n_ref).T

            np.testing.assert_allclose(a_n, a_n_ref)
            np.testing.assert_allclose(b_n, b_n_ref)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
