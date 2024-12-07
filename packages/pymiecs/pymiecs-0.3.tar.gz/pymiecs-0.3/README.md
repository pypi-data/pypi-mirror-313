![logo](URL-to-png)

# pyMieCS
> Mie theory for core-shell nanoparticles

Simple Mie solver for core-shell particles supporting magnetic optical response of the materials (useful for effective medium fitting).

pyMieCS is fully numpy vectorized and therefore fast.


## Getting started

Simple example

```python
import pymiecs as mie

# - setup a core-shell sphere
wavelengths = np.linspace(400, 900, 100)  # wavelength in nm
k0 = 2 * np.pi / wavelengths

r_core = 120.0
r_shell = r_core + 10.0

n_env = 1
mat_core = mie.materials.MaterialDatabase("Si")
mat_shell = mie.materials.MaterialDatabase("Au")
n_core = mat_core.get_refindex(wavelength=wavelengths)
n_shell = mat_shell.get_refindex(wavelength=wavelengths)


# - calculate efficiencies
q_res = mie.Q(k0, r_core=r_core, n_core=n_core, r_shell=r_shell, n_shell=n_shell)

# - plot
plt.plot(wavelengths, q_res["qsca"], label="scat")
plt.plot(wavelengths, q_res["qabs"], label="abs.")
plt.plot(wavelengths, q_res["qext"], label="extinct")

plt.legend()
plt.xlabel("wavelength (nm)")
plt.ylabel(r"efficiency (1/$\sigma_{geo}$)")
plt.tight_layout()
plt.show()
#...
```


## Features

List of features

- internal and external Mie coefficients
- efficiencies
- differential scattering
- angular scattering
- core-shell t-matrix class for `smuthi`


## Installing / Requirements

Installation should work via pip from the [gitlab repository](https://gitlab.com/wiechapeter/pymiecs):

```shell
pip install pymiecs
```

Requirements:

- **scipy**
- **numpy**


## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.


## Links

- gitlab repository: https://gitlab.com/wiechapeter/pymiecs
- issue tracker: https://gitlab.com/wiechapeter/pymiecs/-/issues
  - in case of sensitive bugs you can also contact me directly at
    pwiecha|AT|laas|DOT|fr.
- related projects:
  - pyGDM2: https://homepages.laas.fr/pwiecha/pygdm_doc/
  - TorchGDM: https://gitlab.com/wiechapeter/torchgdm


## Licensing

The code in this project is licensed under the [GNU GPLv3](http://www.gnu.org/licenses/).
