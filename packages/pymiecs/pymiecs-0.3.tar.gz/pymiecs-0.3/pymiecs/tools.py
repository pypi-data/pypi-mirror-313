# Mie observables
# %%
import warnings

import numpy as np


def get_plot_axis_existing_or_new():
    import matplotlib.pyplot as plt

    if len(plt.get_fignums()) == 0:
        show = True
        ax = plt.subplot()
    else:
        show = False
        ax = plt.gca()
    return ax, show


def get_truncution_criteroin_wiscombe(ka):
    # criterion for farfield series truncation for ka = k * r_outer
    #
    # Wiscombe, W. J.
    # "Improved Mie scattering algorithms."
    # Appl. Opt. 19.9, 1505–1509 (1980)
    #
    ka = np.max(ka)

    if ka <= 8:
        n_max = int(np.round(1 + ka + 4.0 * (ka ** (1 / 3))))
    elif 8 < ka < 4200:
        n_max = int(np.round(2 + ka + 4.05 * (ka ** (1 / 3))))
    else:
        n_max = int(np.round(2 + ka + 4.0 * (ka ** (1 / 3))))

    return n_max
