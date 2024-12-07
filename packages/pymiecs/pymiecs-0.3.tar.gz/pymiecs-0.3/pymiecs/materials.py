# core-shell Mie coefficients for magnetizable media
# %%
import warnings
import importlib.resources as pkg_resources
import pathlib

import numpy as np
import pymiecs
from pymiecs.tools import get_plot_axis_existing_or_new


# --- get all available tabulated materials
DATA_FOLDER = "data/"
data_files = pkg_resources.files(pymiecs).joinpath(DATA_FOLDER).iterdir()

REFINDEX_DATA = {}
for f in data_files:
    f_n = pathlib.Path(f).name
    mat_name = f_n.split("_")[0]
    REFINDEX_DATA[mat_name.lower()] = [f, mat_name]


def list_available_materials(verbose=False):
    if verbose:
        for f in REFINDEX_DATA:
            print("{}: ".format(f, pathlib.Path(REFINDEX_DATA[f]).name))
    return [f for f in REFINDEX_DATA]


# --- internal helper
def _load_tabulated(dat_str):
    rows = dat_str["data"].split("\n")
    splitrows = [c.split() for c in rows]
    wl = []
    eps = []
    for s in splitrows:
        if len(s) > 0:
            wl.append(1000.0 * float(s[0]))  # microns --> nm
            _n = float(s[1])
            if len(s) > 2:
                _k = float(s[2])
            else:
                _k = 0.0
            eps.append((_n + 1j * _k) ** 2)
    return wl, eps


def _load_formula(dat_str):
    model_type = int((dat_str["type"].split())[1])
    coeff = [float(s) for s in dat_str["coefficients"].split()]
    for k in ["range", "wavelength_range"]:
        if k in dat_str:
            break
    # validity range (convert to nm)
    wl_range = [1e3 * float(dat_str[k].split()[0]), 1e3 * float(dat_str[k].split()[1])]

    return model_type, wl_range, coeff


# ----- material classes
class MaterialBaseClass:
    """base class for materials"""

    __name__ = "materials base class"

    def __init__(self):
        self.wl = np.array([0, 1e6])  # wavelength in nm
        self.n_real = np.ones(2)
        self.n_imag = np.ones(2)
        self.n_cplx = self.n_real + 1.0j * self.n_imag

    def get_refindex(self, wavelength):
        n_r = np.interp(wavelength, self.wl, self.n_real)
        n_i = np.interp(wavelength, self.wl, self.n_imag)
        n = n_r + 1j * n_i
        return n

    def get_epsilon(self, wavelength):
        n = self.get_refindex(wavelength)
        return n**2

    def plot_epsilon(self, wavelengths=np.linspace(400, 1400, 100)):
        import matplotlib.pyplot as plt

        eps = self.get_epsilon(wavelengths)

        # plot
        ax, show = get_plot_axis_existing_or_new()

        plt.title("epsilon of '{}'".format(self.__name__))
        plt.plot(wavelengths, eps.real, label=r"Re($\epsilon$)")
        plt.plot(wavelengths, eps.imag, label=r"Im($\epsilon$)")
        plt.legend()
        plt.xlabel("wavelength (nm)")
        plt.ylabel("permittivity")

        if show:
            plt.show()

    def plot_refractive_index(self, wavelengths=np.linspace(400, 1400, 100)):
        import matplotlib.pyplot as plt

        n_mat = self.get_refindex(wavelengths)

        # plot
        ax, show = get_plot_axis_existing_or_new()

        plt.title("ref. index of '{}'".format(self.__name__))
        plt.plot(wavelengths, n_mat.real, label="n")
        plt.plot(wavelengths, n_mat.imag, label="k")
        plt.legend()
        plt.xlabel("wavelength (nm)")
        plt.ylabel("refractive index")

        if show:
            plt.show()


class Constant(MaterialBaseClass):
    """constant ref. index material"""

    __name__ = "constant"

    def __init__(self, n=1.0):
        self.__name__ = f"constant (n={n})"
        self.wl = np.array([0, 1e6])  # wavelength in nm
        self.n_real = np.ones(2) * n.real
        self.n_imag = np.ones(2) * n.imag
        self.n_cplx = self.n_real + 1.0j * self.n_imag


# --- main interface classes
class MaterialDatabase(MaterialBaseClass):
    """dispersion from a database entry

    Use permittivity data from included database (data from https://refractiveindex.info/),
    or by loading a yaml file downloaded from https://refractiveindex.info/. Currently
    supported ref.index formats are tabulated n(k) data or Sellmeier model.

    Tabulated materials natively available in torchgdm can be
    printed via :func:`torchgdm.materials.list_available_materials()`

    Requires `pyyaml` (pip3 install pyyaml)

    Parameters
    ----------
    name : str
        name of database entry

    yaml_file : str, default: None
        optional filename of yaml refractiveindex data to load. In case a
        filename is provided, `name` will only be used as __name__ attribute
        for the class instance.

    """

    def __init__(
        self,
        name="",
        yaml_file=None,
        init_lookup_wavelengths=None,
    ):
        """Use tabulated dispersion"""
        import yaml

        super().__init__()

        if (name == "") and (yaml_file is None):
            print("No material specified. Available materials in database: ")
            for k in REFINDEX_DATA:
                print("     - '{}'".format(k))
            del self
            return
        if (yaml_file is None) and (name.lower() not in REFINDEX_DATA):
            raise ValueError(
                "'{}': Unknown material. Available materials in database: {}".format(
                    name, REFINDEX_DATA.keys()
                )
            )

        # load database entry from yaml
        if yaml_file is None:
            yaml_file = REFINDEX_DATA[name.lower()][0]
            self.__name__ = REFINDEX_DATA[name.lower()][1]
        else:
            if name:
                self.__name__ = name
            else:
                self.__name__ = pathlib.Path(yaml_file).stem

        with open(yaml_file, "r", encoding="utf8") as f:
            self.dset = yaml.load(f, Loader=yaml.BaseLoader)

        if len(self.dset["DATA"]) > 1:
            warnings.warn(
                "Several model entries in data-set for '{}' ({}). Using first entry.".format(
                    name, yaml_file
                )
            )
        dat = self.dset["DATA"][0]
        self.type = dat["type"]
        self.wl_dat = np.array([])
        self.eps_dat = np.array([])
        self.lookup_eps = {}

        # load refractive index model.
        # currently supported: tabulated data and Sellmeier model.
        # - tabulated data
        if self.type.split()[0] == "tabulated":
            wl_dat, eps_dat = _load_tabulated(dat)
            self.wl_dat = np.array(wl_dat)
            self.eps_dat = np.array(eps_dat)
            self.model_type = "data"
            self.coeff = []
            self.wl_range = [np.min(self.wl_dat), np.max(self.wl_dat)]

        # - Sellmeier
        elif self.type.split()[0] == "formula":
            self.model_type, self.wl_range, self.coeff = _load_formula(dat)
            if self.model_type == 1:
                self.model_type = "sellmeier"
        else:
            raise ValueError(
                "refractiveindex.info data type '{}' not implemented yet.".format(
                    self.type
                )
            )

        # optionally initialize wavelength lookup
        if init_lookup_wavelengths is not None:
            for wl in init_lookup_wavelengths:
                _eps = self._get_eps_single_wl(wl)

    def __repr__(self, verbose: bool = False):
        """description about material"""
        out_str = ' ----- Material "{}" ({}) -----'.format(
            self.__name__, self.model_type
        )
        if self.model_type == "data":
            out_str += "\n tabulated wavelength range: {:.1f}nm - {:.1f}nm".format(
                *self.wl_range
            )
        elif self.model_type == "sellmeier":
            out_str += "\n Sellmeier model validity range: {:.1f}nm - {:.1f}nm".format(
                *self.wl_range
            )
        return out_str

    def _eval(self, wavelength):
        """evaluate refractiveindex.info model"""

        # - tabulated, using bilinear interpolation
        if self.model_type == "data":
            # torch implementation of 1d interpolation:
            eps = np.interp(wavelength, self.wl_dat, self.eps_dat)

        # - Sellmeier
        elif self.model_type == "sellmeier":
            eps = 1 + self.coeff[0]

            def g(c1, c2, w):
                return c1 * (w**2) / (w**2 - c2**2)

            for i in range(1, len(self.coeff), 2):
                # wavelength factor 1/1000: nm --> microns
                wl_mu = wavelength / 1000.0
                eps += g(self.coeff[i], self.coeff[i + 1], wl_mu)

        else:
            raise ValueError(
                "Only formula '1' (Sellmeier) or 'data' models supported so far."
            )

        return eps

    def _get_refindex_single_wl(self, wavelength):
        # memoize evaluations
        wl_key = float(wavelength)

        if wl_key in self.lookup_eps:
            eps = self.lookup_eps[wl_key]
        else:
            eps = self._eval(wavelength)
            self.lookup_eps[wl_key] = eps

        return eps**0.5

    def get_refindex(self, wavelength):
        """return complex refractive index at `wavelength`"""
        wavelength = np.array(wavelength)

        # multiple wavelengths
        if len(np.array(wavelength).shape) == 1:
            n = np.stack(
                [self._get_refindex_single_wl(wl) for wl in wavelength], axis=0
            )
        else:
            n = self._get_refindex_single_wl(wavelength)

        return n


# --- wrapper to often used materials
class Gold(MaterialDatabase):
    """gold permittivity
    P. B. Johnson and R. W. Christy. Optical Constants of the Noble Metals,
    Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self):
        super().__init__(name="Au")
        self.__name__ = "Gold, Johnson/Christy"


class Silver(MaterialDatabase):
    """silver permittivity

    P. B. Johnson and R. W. Christy. Optical Constants of the Noble Metals,
    Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self):
        super().__init__(name="Ag")
        self.__name__ = "Silver, Johnson/Christy"


class Alu(MaterialDatabase):
    """aluminium permittivity

    A. D. Rakić, A. B. Djurišic, J. M. Elazar, and M. L. Majewski.
    Optical properties of metallic films for vertical-cavity optoelectronic
    devices, Appl. Opt. 37, 5271-5283 (1998)
    """

    def __init__(self):
        super().__init__(name="Al")
        self.__name__ = "Aluminium, Rakic"


class Silicon(MaterialDatabase):
    """silicon permittivity
    Edwards, D. F. in Handbook of Optical Constants of Solids
    (ed. Palik, E. D.) 547–569 (Academic Press, 1997).
    """

    def __init__(self):
        super().__init__(name="Si")
        self.__name__ = "Silicon, Palik"


class Germanium(MaterialDatabase):
    """germanium permittivity
    Nunley et al. **J. Vac. Sci. Technol. B** 34, 061205 (2016)
    """

    def __init__(self):
        super().__init__(name="Ge")
        self.__name__ = "Germanium, Nunley"


class MaxwellGarnettMixing(MaterialBaseClass):
    """Composite material ref. index using Maxwell Garnett Mixing"""

    __name__ = "Maxwell Garnett Mixing"

    def __init__(self, mat_particles, mat_host, c_vol):
        self.mat_particles = mat_particles
        self.mat_host = mat_host
        self.c_vol = c_vol

    def get_refindex(self, wavelength):
        eps_host = self.mat_host.get_epsilon(wavelength)
        eps_particles = self.mat_particles.get_epsilon(wavelength)

        eps_maxwellgarnett = eps_host * (
            1
            + 3
            * self.c_vol
            * (eps_particles - eps_host)
            / (eps_particles + 2 * eps_host - self.c_vol * (eps_particles - eps_host))
        )

        n_MG = eps_maxwellgarnett**0.5

        return n_MG
