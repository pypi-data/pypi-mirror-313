""" """
# -*- coding: utf-8 -*-
#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from findiff import FinDiff
import numpy as np


def dY_by_dX(current, volt, acc=4):
    """Calculate dI/dV."""

    if isinstance(volt, list) and len(volt) > 1:
        volt = np.array(volt)
    if isinstance(current, list) and len(current) > 1:
        current = np.array(current)

    # validate input
    if (
        not isinstance(current, np.ndarray)
        and not isinstance(volt, np.ndarray)
        and current.ndim != 1
        and volt.ndim != 1
        and current.size != volt.size
    ):
        raise ValueError(
            "Current and voltage are not 1D numpy arrays or not of same size."
        )

    if isinstance(volt, np.ndarray) and volt.ndim == 1 and volt.size > 1:
        dv = volt[1] - volt[0]
    else:
        raise ValueError("Voltage is not a list or 1D numpy array.")

    d_dV = FinDiff(0, dv, acc=acc)
    dI_dV = d_dV(current)

    return dI_dV
