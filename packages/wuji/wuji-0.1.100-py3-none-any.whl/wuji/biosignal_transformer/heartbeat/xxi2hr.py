#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   xxi2hr 
@Time        :   2024/8/27 17:24
@Author      :   Xuesong Chen
@Description :   
"""

import numpy as np
from scipy.interpolate import interp1d
from numpy.typing import NDArray
from hrvanalysis import get_nn_intervals
import pandas as pd


def interpolate_hr(hr: NDArray, duration: int, target_fs: int) -> NDArray:
    original_timestamps = np.linspace(0, duration, num=len(hr))
    target_interval = 1 / target_fs
    target_times = np.arange(0, duration, target_interval)
    interp_func = interp1d(original_timestamps, hr, kind='linear')
    interpolated_hr = interp_func(target_times)
    return interpolated_hr


def compute_hr_from_xxi(positions, xxis, sample_rate, n_samples, window_sec=3):
    xxis_ms = xxis / sample_rate * 1000
    filter_xxis_ms = get_nn_intervals(
        xxis_ms, verbose=False, ectopic_beats_removal_method='karlsson')
    filter_xxis_ms = np.array(list(map(lambda x: x / 1000, filter_xxis_ms)))
    ref = {'time': positions / sample_rate, 'iei': filter_xxis_ms}
    totalSec = int(n_samples / sample_rate)

    # Generate evaluation times
    stepSec = 1
    evalSec = np.arange(0, totalSec - window_sec + stepSec, stepSec)
    windows_start = evalSec[:, np.newaxis]
    windows_end = windows_start + window_sec

    # Create a mask for each window
    within_window = (ref['time'] > windows_start) & (ref['time'] <= windows_end)

    # Calculate heart rate for each window
    hr = 60 / np.array([np.mean(ref['iei'][mask]) if mask.any() else np.nan for mask in within_window])

    # Interpolation and NaN handling
    if len(hr) < totalSec:
        fill_length = totalSec - len(hr)
        left_fill_length = int((window_sec - 1) / 2)
        right_fill_length = fill_length - left_fill_length
        left_fill = np.full(left_fill_length, np.nan)
        right_fill = np.full(right_fill_length, np.nan)
        hr = np.concatenate((left_fill, hr, right_fill))

    # Convert to pandas Series and interpolate
    output_hr = pd.Series(hr).interpolate(method='linear').fillna(method='bfill')
    fs = 1 / stepSec
    return output_hr, fs