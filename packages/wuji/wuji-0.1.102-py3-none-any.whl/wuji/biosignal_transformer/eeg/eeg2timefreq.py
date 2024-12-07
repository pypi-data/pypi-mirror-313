#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   eeg2timefreq 
@Time        :   2024/9/20 19:04
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt

from wuji.biosignal_transformer.utils import get_normalized_timefrequency
from lspopt import spectrogram_lspopt
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import medfilt


def get_eeg_feature_old(
        sigal,
        fs,
        seg_duration=1,
        seg_overlap_ratio=0.5,
        min_frequency=0.3,
        max_frequency=35,
):
    return get_normalized_timefrequency(
        sigal,
        fs,
        seg_duration=seg_duration,
        seg_overlap_ratio=seg_overlap_ratio,
        min_frequency=min_frequency,
        max_frequency=max_frequency,
        log=True
    )


def get_eeg_feature(
    sigal,
    fs,
    seg_duration=10,
    seg_overlap_ratio=0.8,
    min_frequency=0.3,
    max_frequency=35,
    normalize=False,
):
    f, t, Sxx = spectrogram_lspopt(
        sigal,
        fs,
        nperseg=int(seg_duration * fs),
        noverlap=int(seg_duration * fs * seg_overlap_ratio),
    )
    Sxx = 10 * np.log10(Sxx + 1e-13)
    good_freqs = np.logical_and(f >= min_frequency, f <= max_frequency)
    good_f = f[good_freqs]
    Sxx = Sxx[good_freqs, :]

    if normalize:
        Sxx = (Sxx - np.mean(Sxx)) / np.std(Sxx)
    new_f = np.arange(min_frequency, max_frequency, 0.5)
    interp_func = interp1d(
            good_f, Sxx, axis=0, kind="linear", fill_value="extrapolate"
        )
    Sxx_interp = interp_func(new_f)
    assert not np.any(np.isnan(Sxx_interp)), "NAN value in result"
    Sxx_interp = medfilt(Sxx_interp, kernel_size=(3, 21))
    return Sxx_interp
