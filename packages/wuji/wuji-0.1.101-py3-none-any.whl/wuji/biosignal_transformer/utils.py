#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils 
@Time        :   2024/9/6 19:29
@Author      :   Xuesong Chen
@Description :   
"""

import neurokit2 as nk
import numpy as np


def get_normalized_timefrequency(
        sigal,
        fs,
        seg_duration=2,
        seg_overlap_ratio=0.5,
        min_frequency=0.3,
        max_frequency=35,
        log=False
):
    freq, time, power = nk.signal_timefrequency(
        sigal,
        window=seg_duration,
        overlap=fs * seg_duration * seg_overlap_ratio,
        min_frequency=min_frequency,
        max_frequency=max_frequency,
        sampling_rate=fs,
        show=False)
    if log:
        power = np.log(power + 1)
    norm_power = power / (np.sum(power, axis=0, keepdims=True) + 1e-8)
    # return power
    return norm_power  # freq * time
