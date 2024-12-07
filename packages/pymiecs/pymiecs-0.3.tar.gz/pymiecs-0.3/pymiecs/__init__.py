# encoding=utf-8
#
# Copyright (C) 2024, P. R. Wiecha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
pymiecs - simple core-shell nano-sphere Mie solver
"""

__name__ = "pymiecs"
__version__ = "0.3"
__date__ = "12/06/2024"  # MM/DD/YYY
__license__ = "GPL3"
__status__ = "beta"

__copyright__ = "Copyright 2024, Peter R. Wiecha"
__author__ = "Peter R. Wiecha"
__maintainer__ = "Peter R. Wiecha"
__email__ = "pwiecha@laas.fr"
__credits__ = [
    "Christian Girard",
]

# --- populate namespace

# make some functions and classes available at top level
from .main import Q
from .main import angular
from .main import Q_scat_differential
from .main import S1_S2

# modules
from . import materials
from . import special
from . import mie_coeff
from . import t_matrix
