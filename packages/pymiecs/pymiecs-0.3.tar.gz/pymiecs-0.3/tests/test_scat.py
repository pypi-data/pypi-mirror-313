# encoding=utf-8
# %%
import unittest

import numpy as np

import pymiecs as mie


class TestCoreShell(unittest.TestCase):

    def setUp(self):
        self.verbose = True

        self.wavelengths = np.linspace(400, 900, 20)  # wavelength in nm

        self.test_cases = [
            dict(
                n_env=1.0,
                r_core=80.0,
                n_core=3 + 0.1j,  # some loss for Qabs testing
                r_shell=120.0,
                n_shell=4,
            ),
            dict(
                n_env=1.5,
                r_core=90.0,
                n_core=2.5 + 0.2j,
                r_shell=110.0,
                n_shell=0.05 + 3.5j,  # plasmonic material
            ),
            dict(
                n_env=1.25,
                r_core=70.0,
                n_core=0.05 + 3.5j,  # plasmonic material
                r_shell=110.0,
                n_shell=4.5,  # lossy dielectric
            ),
        ]

    def test_Q_scat(self):
        # --- evaluate mie coefficients
        for conf in self.test_cases:

            # pymiecs
            k0 = 2 * np.pi / self.wavelengths

            Q_dict = mie.Q(
                k0=k0,
                r_core=conf["r_core"],
                n_core=conf["n_core"],
                r_shell=conf["r_shell"],
                n_shell=conf["n_shell"],
                n_env=conf["n_env"],
            )

            # reference: pymiescatt
            try:
                from PyMieScatt import MieQCoreShell
            except (ModuleNotFoundError, ImportError):
                print("`PyMieScatt` seems not to be installed. Skipping test.")
                return

            q_sca = []
            q_abs = []
            for wavelength in self.wavelengths:

                Q_dict_ref = MieQCoreShell(
                    mCore=conf["n_core"],
                    mShell=conf["n_shell"],
                    wavelength=wavelength,
                    dCore=2 * conf["r_core"],
                    dShell=2 * conf["r_shell"],
                    nMedium=conf["n_env"],
                    asCrossSection=False,
                    asDict=True,
                )

                q_sca.append(Q_dict_ref["Qsca"])
                q_abs.append(Q_dict_ref["Qabs"])

            q_sca = np.array(q_sca)
            q_abs = np.array(q_abs)

            np.testing.assert_allclose(Q_dict["qsca"], q_sca)
            np.testing.assert_allclose(Q_dict["qabs"], q_abs)

    def test_Q_scat_differential(self):
        # --- evaluate test cases
        for conf in self.test_cases:
            k0 = 2 * np.pi / self.wavelengths

            # direct fwd/bwd
            Q_dict = mie.Q(
                k0=k0,
                r_core=conf["r_core"],
                n_core=conf["n_core"],
                r_shell=conf["r_shell"],
                n_shell=conf["n_shell"],
                n_env=conf["n_env"],
            )
            # differential + integration
            sca_diff_f = mie.Q_scat_differential(
                k0=k0,
                r_core=conf["r_core"],
                n_core=conf["n_core"],
                r_shell=conf["r_shell"],
                n_shell=conf["n_shell"],
                n_env=conf["n_env"],
                angular_range=[0, np.pi / 150],
                angular_steps=2,
            )
            sca_diff_b = mie.Q_scat_differential(
                k0=k0,
                r_core=conf["r_core"],
                n_core=conf["n_core"],
                r_shell=conf["r_shell"],
                n_shell=conf["n_shell"],
                n_env=conf["n_env"],
                angular_range=[149 * np.pi / 150, np.pi],
                angular_steps=2,
            )

            np.testing.assert_allclose(
                Q_dict["qfwd"], sca_diff_f["qsca"], rtol=1e-3, atol=1e-3
            )
            np.testing.assert_allclose(
                Q_dict["qback"], sca_diff_b["qsca"], rtol=1e-3, atol=1e-3
            )

    def test_scat_angular(self):
        for conf in self.test_cases:
            k0 = 2 * np.pi / self.wavelengths
            k_angular = k0[::4]  # check every 4th wavelength
            wl_angular = (2 * np.pi) / k_angular

            # - eval pymiecs
            theta, SL, SR, SU = mie.angular(
                k_angular,
                r_core=conf["r_core"],
                n_core=conf["n_core"],
                r_shell=conf["r_shell"],
                n_shell=conf["n_shell"],
                n_env=conf["n_env"],
            )

            # reference: pymiescatt
            try:
                from PyMieScatt import CoreShellScatteringFunction
            except (ModuleNotFoundError, ImportError):
                print("`PyMieScatt` seems not to be installed. Skipping test.")
                return

            # - angular spectrum helper
            def _pymiescatt_angular(
                n_core, n_shell, wavelengths, r_core, r_shell, n_env
            ):
                SL_all = []
                SR_all = []
                SU_all = []
                for wl in wavelengths:
                    theta, SL_ref, SR_ref, SU_ref = CoreShellScatteringFunction(
                        mCore=n_core,
                        mShell=n_shell,
                        wavelength=wl,
                        dCore=2 * r_core,
                        dShell=2 * r_shell,
                        nMedium=n_env,
                        minAngle=0,
                        maxAngle=180,
                        angularResolution=1,
                    )
                    # normalize pymiescatt to Bohren Huffmann convention
                    k = n_env * 2 * np.pi / wl
                    SL_all.append(SL_ref / (r_shell**2 * k**2))
                    SR_all.append(SR_ref / (r_shell**2 * k**2))
                    SU_all.append(SU_ref / (r_shell**2 * k**2))

                return (
                    np.array(theta),
                    np.array(SL_all),
                    np.array(SR_all),
                    np.array(SU_all),
                )

            # - eval pymiescatt
            theta_ref, SL_ref, SR_ref, SU_ref = _pymiescatt_angular(
                wavelengths=wl_angular,
                r_core=conf["r_core"],
                n_core=conf["n_core"],
                r_shell=conf["r_shell"],
                n_shell=conf["n_shell"],
                n_env=conf["n_env"],
            )

            np.testing.assert_allclose(SL, SL_ref)
            np.testing.assert_allclose(SR, SR_ref)
            np.testing.assert_allclose(SU, SU_ref)
            np.testing.assert_allclose(theta, theta_ref)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
