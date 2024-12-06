# Copyright (c) 2020 Coronis Computing S.L. (Spain)
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Author: Ricard Campos (ricard.campos@coronis.es)

import math
import numpy as np
import scipy.special


def tension_spline_rbf(r, e):
    """Spline with tension.

    Definition of the spline with tension from [2]. You can also find a brief description of its behaviour in [1].
    Note that [1] suggests using a polynomial of degree 0 with this RBF.

    Args:
        r: value to evaluate.
        e: tension parameter.

    Returns:
        value of the RBF at r.

    References:
    [1] https://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/how-spline-works.htm
    [2] Mitas, L., and H. Mitasova. 1988. General Variational Approach to the Interpolation Problem. Comput. Math. Applic. Vol. 16. No. 12. pp. 983–992. Great Britain.
    """

    # Singularity at 0, scalar value
    if np.isscalar(r) and r < 1e-15:
        return 0

    Ce = 0.5772156649015328606065120900824  # Value of the euler constant
    fx = -(1/(2*math.pi*e*e))*(np.log(r*e/2)+Ce+scipy.special.kn(0, r*e))

    if not np.isscalar(r):
        fx[(r < 1e-15)] = 0

    return fx
