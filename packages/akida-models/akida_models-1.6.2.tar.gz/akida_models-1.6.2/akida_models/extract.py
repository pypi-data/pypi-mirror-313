#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""Sample extraction from datasets"""

import numpy as np


def extract_samples(out_file, dataset, nb_samples=1024, dtype="uint8"):
    """Extracts samples from dataset and save them to a npz file.

    Args:
        out_file (str): name of output file
        dataset (numpy.ndarray or tf.data.Dataset): dataset for extract samples
        nb_samples (int, optional): number of samples. Defaults to 1024.
        dtype (str or np.dtype, optional): the dtype to cast the samples. Defaults to "uint8".
    """
    # The expected number of samples
    if isinstance(dataset, np.ndarray):
        if len(dataset) < nb_samples:
            raise ValueError("Not enough samples in the dataset.")
        samples_x = dataset[0:nb_samples]
    else:
        try:
            samples_x, _ = next(iter(dataset))
        except Exception:
            raise ValueError(f"{type(dataset)} dataset format not supported.")

    samples_x = np.array(samples_x, dtype=dtype)
    samples = {"data": samples_x}
    np.savez(out_file, **samples)
    print(f"Samples saved as {out_file}")
