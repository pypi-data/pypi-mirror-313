#   Copyright 2024 Miguel Loureiro

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
This module contains functions to help users generate arrays of gaussian white noise.

Functions
---------
gen_noise_signal
    Generate an array of gaussian white noise values.
"""

import numpy as np

def gen_noise_signal(power: int | float, n_samples: int, seed: int=0) -> np.ndarray:
    """
    Generate white noise signals.

    This function can be used to generate an array of gaussian white noise values.
    It returns an array of shape (1, n_samples).

    Parameters
    ----------
    power : int | float
        Noise power.

    n_samples : int
        Length of the white noise signal.

    seed : int, default=0
        Random seed.

    Returns
    -------
    noise_array : np.ndarray
        An array of gaussian white noise values.
    """

    return np.random.default_rng(seed=seed).normal(scale=np.sqrt(power), size=(1, n_samples));